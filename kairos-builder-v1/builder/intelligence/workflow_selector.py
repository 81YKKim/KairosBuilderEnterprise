class WorkflowSelector:
    def select(self, decision: dict) -> str:
        if decision["risk"] > 0.7:
            return "safe_workflow"

        if decision["risk"] > 0.4:
            return "standard_workflow"

        return "fast_workflow"