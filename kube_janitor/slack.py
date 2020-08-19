import os
import logging
from slack import WebClient
from slack.errors import SlackApiError

logger = logging.getLogger(__name__)


class Slack:
    def __init__(self, config):
        self._config = config
        self._client = WebClient(os.environ['SLACK_TOKEN'])
        self._channel = config['channel'].get()

    def notify(self, message):
        logger.info(f"Posting to slack:\n{message}")
        self._post(message)

    def _post(self, msg):

        try:
            response = self._client.chat_postMessage(
                channel=self._channel,
                text=msg,
                as_user=True
            )
            assert response["message"]["text"] == msg
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            logger.error(f"Got an error: {e.response['error']}")
