class AutoPatchGenerator:
    def build(self, strategy: dict) -> dict:
        return {
            "patch": f"AUTO_FIX:{strategy['action']}",
            "applied": False
        }