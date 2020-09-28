import kube_janitor.resources.ns


class Janitor:
    def __init__(self, kube, config):
        self._kube = kube
        self._config = config

    def suggest(self):
        resources = [
            kube_janitor.resources.ns.Namespace(self._kube, self._config)
        ]
        suggestions = {}
        for r in resources:
            r_suggestions = r.suggest_for_deletion()
            if r_suggestions:
                suggestions[r.resource] = r_suggestions
        return suggestions
