import json
from pathlib import Path


class ProjectStateManager:
    def __init__(self, state_path: str = "builder/context/project.json") -> None:
        self.state_path = Path(state_path)

    def initialize(self) -> dict:
        data = {
            "project": "Kairos Builder Enterprise V2",
            "version": "2.0.0-alpha",
            "current_sprint": 29,
            "last_commit": "#000028",
            "test_status": "PASS",
            "repository": "KairosBuilderEnterprise",
            "state": "development",
        }

        self.save(data)
        return data

    def load(self) -> dict:
        if not self.state_path.exists():
            return self.initialize()

        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def save(self, data: dict) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def current_sprint(self) -> int:
        return self.load()["current_sprint"]

    def bump_sprint(self) -> int:
        data = self.load()
        data["current_sprint"] += 1
        self.save(data)
        return data["current_sprint"]

    def set_last_commit(self, commit: str) -> None:
        data = self.load()
        data["last_commit"] = commit
        self.save(data)

    def set_test_status(self, status: str) -> None:
        data = self.load()
        data["test_status"] = status
        self.save(data)

    def set_repository(self, repository: str) -> None:
        data = self.load()
        data["repository"] = repository
        self.save(data)