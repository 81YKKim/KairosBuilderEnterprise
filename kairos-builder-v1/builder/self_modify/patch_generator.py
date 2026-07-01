class PatchGenerator:
    def generate(self, analysis: dict) -> dict:
        if analysis["complexity"] > 20:
            return {
                "action": "refactor_suggested",
                "reason": "high complexity"
            }

        return {
            "action": "no_change",
            "reason": "acceptable complexity"
        }