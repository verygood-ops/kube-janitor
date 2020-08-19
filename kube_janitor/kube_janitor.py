import kube_janitor.resources.ns


class Janitor:
    def __init__(self, kube, config):
        self._kube = kube
        self._config = config

    def suggest(self):
        resources = [
            kube_janitor.resources.ns.Namespace(self._kube, self._config)
        ]
        res = {r.resource: r.suggest_for_deletion() for r in resources}
        return res
