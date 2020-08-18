import os
from slack import WebClient
from slack.errors import SlackApiError


class Slack:
    def __init__(self, config):
        self._config = config
        self._client = WebClient(os.environ['SLACK_TOKEN'])
        self._username = "Kube Janitor of {}".format(os.environ['CLUSTER_NAME'])
        self._channel = config['channel']

    def notify(self, message):
        self._post(message)

    def _post(self, msg):
        try:
            response = self._client.chat_postMessage(
                channel=self._channel,
                text=msg,
                as_user=False,
                username=self._username
            )
            assert response["message"]["text"] == msg
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
