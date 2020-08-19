import os
import logging
import sys

import kubernetes
from kube_janitor import kube_janitor
from kube_janitor import slack
from confuse import Configuration

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    kubernetes.config.load_incluster_config()
except kubernetes.config.config_exception.ConfigException:
    kubernetes.config.load_kube_config()

kube = kubernetes.client.CoreV1Api()
config = Configuration('kube-janitor', __name__)
slack_token = config['slack_token']


def main():
    suggestions = kube_janitor.Janitor(kube, config).suggest()
    logger.info(f"Janitor suggests: {suggestions}")
    msg = _format_msg(suggestions)
    slack.Slack(config['slack']).notify(msg)


def _format_msg(suggestions):
    del_cmd = []
    for resource, names in suggestions.items():
        for name in names:
            del_cmd.append(f"kubectl delete {resource} {name}")
    del_cmd = "\n".join(del_cmd)
    cluster_name = os.environ['CLUSTER_NAME']

    message = f"""I suggest to clean this at `{cluster_name}`:
```
{del_cmd}
```
    """
    return message


if __name__ == "__main__":
    main()
