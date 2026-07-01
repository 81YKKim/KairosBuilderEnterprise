from pathlib import Path


class WorkspaceManager:
    def __init__(self, base_path: str = "workspaces"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def create_workspace(self, name: str) -> Path:
        path = self.base_path / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def list_workspaces(self):
        return [p.name for p in self.base_path.iterdir() if p.is_dir()]