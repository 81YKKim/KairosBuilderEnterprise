class PredictionEngine:
    def predict(self, history: list[str]) -> str:
        if not history:
            return "verify"

        last = history[-1].split()[0]

        rules = {
            "new": "generate",
            "generate": "list",
            "list": "describe",
            "verify": "doctor",
            "inspect": "health",
            "health": "doctor",
            "doctor": "workflow verify"
        }

        return rules.get(last, "verify")