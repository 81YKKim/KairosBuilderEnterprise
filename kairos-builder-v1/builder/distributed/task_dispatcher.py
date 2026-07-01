class TaskDispatcher:
    def dispatch(self, node_registry, task: str):
        nodes = node_registry.list_nodes()

        if not nodes:
            return {"error": "NO_NODES_AVAILABLE"}

        node_id = list(nodes.keys())[0]

        return {
            "node": node_id,
            "task": task,
            "status": "dispatched"
        }