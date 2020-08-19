import logging
from kube_janitor.resources.base import Resource

loggger = logging.getLogger(__name__)


class Namespace(Resource):
    resource = "ns"

    def suggest_for_deletion(self):
        all_raw = self._kube.list_namespace().items

        all_ns = set(self._prettify(all_raw))
        annotated_ns = set(self._prettify(self._get_annotated_ns(all_raw)))
        whitelisted_ns = set(self._get_whitelisted_ns())
        loggger.info(f"All ns: {all_ns}")
        loggger.info(f"Annotated ns: {all_ns}")
        loggger.info(f"Whitelisted ns: {all_ns}")

        return all_ns - annotated_ns - whitelisted_ns

    def _get_annotated_ns(self, all_ns):
        annotated_ns = []
        for ns in all_ns:
            if not ns.metadata.annotations:
                continue
            for whitelisted in self._config['annotation_whitelist'].get():
                if any(whitelisted in key for key in ns.metadata.annotations):
                    annotated_ns.append(ns)
        return annotated_ns

    def _get_whitelisted_ns(self):
        return self._config['whitelist'].get()

    def _prettify(self, raw):
        return (r.metadata.name for r in raw)
