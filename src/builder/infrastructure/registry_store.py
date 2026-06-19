import json
from pathlib import Path

from builder.domain.project import Project


class RegistryStore:
    def __init__(self, registry_path: str = "registry/projects.json") -> None:
        self.registry_path = Path(registry_path)

    def load(self) -> list[Project]:
        if not self.registry_path.exists():
            return []

        data = json.loads(self.registry_path.read_text(encoding="utf-8"))
        return [Project.from_dict(item) for item in data.get("projects", [])]

    def save(self, projects: list[Project]) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"projects": [project.to_dict() for project in projects]}
        self.registry_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
