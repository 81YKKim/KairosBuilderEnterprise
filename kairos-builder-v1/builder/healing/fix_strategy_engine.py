class FixStrategyEngine:
    def generate(self, cause: str) -> dict:
        if cause == "contract_mismatch":
            return {"action": "align_contract"}
        return {"action": "unknown_fix"}