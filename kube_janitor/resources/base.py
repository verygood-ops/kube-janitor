class Resource:
    resource = "not_implemented"

    def __init__(self, kube, config):
        self._kube = kube
        self._config = config['resources'][self.resource]

    def suggest_for_deletion(self):
        raise NotImplemented()