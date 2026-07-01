class RewritePlanner:
    def plan(self, analysis: dict) -> dict:
        return {
            "strategy": "full_rewrite",
            "targets": analysis["modules"]
        }