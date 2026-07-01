class RefactorPlanner:
    def plan(self, architecture: dict) -> dict:
        return {
            "goal": "optimize_layer_separation",
            "changes": ["decouple_cli", "enhance_generator"]
        }