class FeedbackEngine:
    def analyze(self, result: dict) -> dict:
        return {
            "success": result["status"] == "completed"
        }