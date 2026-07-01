class ImprovementEngine:
    def suggest(self, analysis: dict) -> dict:
        if analysis["stable"]:
            return {"action": "no_change"}

        return {"action": "optimize"}