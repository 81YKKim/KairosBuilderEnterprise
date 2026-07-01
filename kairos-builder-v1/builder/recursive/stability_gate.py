class StabilityGate:
    def check(self, improvement: dict) -> bool:
        return improvement["improvement"] == "none"