class ContractRegistry:
    def __init__(self):
        self.contracts = {
            "create_project": {
                "return_type": "Path",
                "must_have": ["src", "tests", "docs", "resources", "data"]
            },
            "workflow_commit_message": {
                "prefix": "#000024 feat(workflow):"
            },
            "sprint_run": {
                "format": "Sprint #0000X run completed"
            }
        }

    def get(self, name: str):
        return self.contracts.get(name)