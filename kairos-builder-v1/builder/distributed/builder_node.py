class BuilderNode:
    def __init__(self, node_id: str):
        self.node_id = node_id

    def execute(self, task: dict) -> dict:
        return {
            "node": self.node_id,
            "task": task,
            "result": f"processed by {self.node_id}"
        }