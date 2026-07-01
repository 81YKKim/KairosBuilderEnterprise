class RiskEvaluator:
    def evaluate(self, patch: dict) -> float:
        if patch["action"] == "refactor_suggested":
            return 0.8
        return 0.2