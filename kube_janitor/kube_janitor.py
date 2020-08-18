import kube_janitor.resources.ns


class Janitor:
    def __init__(self, kube, config):
        self._kube = kube
        self._config = config

    def suggest(self):
        cleaners = [
            kube_janitor.resources.ns.Namespace(self._kube, self._config)
        ]

        res = {c.resource: c.suggest_for_deletion() for c in cleaners}
        return res
