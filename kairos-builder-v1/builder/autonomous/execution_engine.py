class ExecutionEngine:
    def execute(self, task: dict) -> dict:
        return {
            "task": task["task"],
            "status": "completed"
        }