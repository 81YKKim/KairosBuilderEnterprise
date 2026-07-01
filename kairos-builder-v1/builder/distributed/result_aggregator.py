class ResultAggregator:
    def __init__(self):
        self.results = []

    def add_result(self, node: str, result: dict):
        self.results.append({
            "node": node,
            "result": result
        })

    def get_all(self):
        return self.results