class FailureDetector:
    def detect(self, test_result: dict) -> bool:
        return test_result.get("status", "ok") != "ok"