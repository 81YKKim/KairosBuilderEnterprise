class CodeRebuilder:
    def rebuild(self, plan: dict) -> dict:
        return {
            "status": "rebuilt",
            "modules": plan["targets"]
        }