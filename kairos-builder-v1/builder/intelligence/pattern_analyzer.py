class PatternAnalyzer:
    def analyze(self, logs: list[dict]):
        success = [l for l in logs if l["success"]]
        fail = [l for l in logs if not l["success"]]

        return {
            "success_rate": len(success) / len(logs) if logs else 0,
            "fail_rate": len(fail) / len(logs) if logs else 0
        }