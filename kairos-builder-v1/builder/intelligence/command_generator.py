class CommandGenerator:
    def generate_next(self, history: list[dict]) -> str:
        if not history:
            return "verify"

        last = history[-1]["command"]

        if "new" in last:
            return "generate domain core"

        if "generate" in last:
            return "verify"

        if "verify" in last:
            return "workflow commit auto evolution"

        return "inspect"