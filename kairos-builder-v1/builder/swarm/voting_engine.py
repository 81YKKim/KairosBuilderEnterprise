class VotingEngine:
    def decide(self, results: list) -> str:
        if len(results) >= 3:
            return "approved"
        return "rejected"