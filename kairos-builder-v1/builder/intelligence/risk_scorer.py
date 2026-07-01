class RiskScorer:
    def score(self, decision: dict) -> float:
        base = decision.get("risk", 1.0)

        if decision["action"] == "unknown":
            return 1.0

        # simple adjustment logic
        return min(base + 0.1, 1.0)