class ProcessManager:
    def execute(self, task: dict) -> dict:
        return {
            "task": task,
            "status": "executed"
        }