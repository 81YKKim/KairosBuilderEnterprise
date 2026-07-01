class EvolutionDecisionEngine:
    def decide(self, proposal: dict) -> str:
        if proposal["priority"] == "high":
            return "apply"
        return "ignore"