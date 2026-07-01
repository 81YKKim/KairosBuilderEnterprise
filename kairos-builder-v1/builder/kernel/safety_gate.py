class SafetyGate:
    def validate(self, mutation: dict) -> bool:
        return "kernel" in mutation.get("mutation", "")