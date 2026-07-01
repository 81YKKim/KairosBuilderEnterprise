class SelfPatchEngine:
    def create_patch(self, suggestion: dict) -> dict:
        return {
            "patch": f"PATCH:{suggestion['action']}",
            "applied": False
        }