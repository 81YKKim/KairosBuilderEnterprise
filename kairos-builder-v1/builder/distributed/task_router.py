class TaskRouter:
    def route(self, task: str) -> dict:
        return {
            "assigned_node": "node-A",
            "task": task
        }