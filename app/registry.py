from pathlib import Path
import yaml

class MetricRegistry:
    def __init__(self, path: str = "semantic/metrics.yml"):
        payload = yaml.safe_load(Path(path).read_text())
        self._metrics = {m["id"]: m for m in payload["metrics"]}

    def all(self):
        return list(self._metrics.values())

    def get(self, metric_id):
        return self._metrics.get(metric_id)
