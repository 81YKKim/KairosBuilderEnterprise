class Improver:
    def improve(self, analysis: dict) -> dict:
        return {
            "improvement": "none" if analysis["drift"] is False else "optimize"
        }