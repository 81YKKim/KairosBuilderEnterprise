class DeploymentSimulator:
    def deploy(self, project: dict) -> dict:
        return {
            "deployment": "success",
            "project": project["project"]
        }