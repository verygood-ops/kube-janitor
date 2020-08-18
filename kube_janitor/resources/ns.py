from kube_janitor.resources.base import Resource


class Namespace(Resource):
    resource = "ns"

    def suggest_for_deletion(self):
        all_raw = self._kube.list_namespace().items

        all_ns = set(self._prettify(all_raw))
        annotated_ns = set(self._prettify(self._get_annotated_ns(all_raw)))
        whitelisted_ns = set(self._get_whitelisted_ns())

        return all_ns - annotated_ns - whitelisted_ns

    def _get_annotated_ns(self, all_ns):
        annotation_whitelist = self._config['annotation_whitelist']
        annotated_ns = []
        for ns in all_ns:
            if not ns.metadata.annotations:
                continue
            for annotation in annotation_whitelist:
                if any(annotation in key for key in
                       ns.metadata.annotations.keys()):
                    annotated_ns.append(ns)
        return annotated_ns

    def _get_whitelisted_ns(self):
        return self._config['ns']['whitelist']

    def _prettify(self, raw):
        return [r.metadata.name for r in raw]
