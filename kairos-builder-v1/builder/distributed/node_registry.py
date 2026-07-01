class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id: str, metadata: dict):
        self.nodes[node_id] = metadata

    def list_nodes(self):
        return self.nodes

    def get_node(self, node_id: str):
        return self.nodes.get(node_id)