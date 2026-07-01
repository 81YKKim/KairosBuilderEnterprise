class TaskScheduler:
    def schedule(self, task: str) -> dict:
        return {
            "task": task,
            "status": "scheduled"
        }