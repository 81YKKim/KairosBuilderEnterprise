class SafetyController:
    def approve(self, test_result: dict) -> bool:
        return test_result.get("pytest") == "ok"