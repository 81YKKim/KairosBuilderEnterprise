class CodeMutator:
    def mutate(self, decision: str) -> dict:
        if decision == "apply":
            return {"mutation": "applied_contract_patch"}
        return {"mutation": "no_change"}