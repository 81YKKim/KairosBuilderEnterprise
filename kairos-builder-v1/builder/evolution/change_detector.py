class ChangeDetector:
    def detect(self, metrics: dict) -> bool:
        return metrics.get("status") != "ok"