import kubernetes
from kube_janitor import kube_janitor
from kube_janitor import slack
from confuse import Configuration

kubernetes.config.load_kube_config()
kube = kubernetes.client.CoreV1Api()
config = Configuration('kube-janitor', __name__)
slack_token = config['slack_token']


def main():
    suggestions = kube_janitor.Janitor(kube, config).suggest()

    kubectx = config['kube']['kubectx']
    kubectl = config['kube']['kubectl']
    context = config['kube']['context']
    del_cmd = "\n".join(f"{kubectl} delete {k} {v}" for k, v in suggestions.items())

    message = f"""
*{context}* I suggest to delete:
```
{kubectx} {context}
{del_cmd}
```
    """
    slack.Slack(config[slack]).notify(message)


if __name__ == "__main__":
    main()
