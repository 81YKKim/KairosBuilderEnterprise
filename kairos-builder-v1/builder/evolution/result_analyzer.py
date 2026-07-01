class ResultAnalyzer:
    def analyze(self, test_result: dict) -> dict:
        return {
            "status": test_result.get("pytest"),
            "stable": test_result.get("pytest") == "ok"
        }