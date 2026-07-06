class DeploymentEngine:
    def deploy(self, package: dict) -> dict:
        return {
            "status": "deployed",
            "version": package.get("version", "2.0.0-alpha"),
        }