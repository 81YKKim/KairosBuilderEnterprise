from pathlib import Path

from builder.domain.project import Project
from builder.infrastructure.registry_store import RegistryStore


class RegistryService:
    def __init__(self, store: RegistryStore | None = None) -> None:
        self.store = store or RegistryStore()

    def register(self, project: Project) -> None:
        projects = self.store.load()
        projects = [item for item in projects if item.name != project.name]
        projects.append(project)
        self.store.save(projects)

    def list_projects(self) -> list[Project]:
        return self.store.load()

    def find(self, name: str) -> Project | None:
        for project in self.store.load():
            if project.name == name:
                return project
        return None

    def remove(self, name: str) -> bool:
        projects = self.store.load()
        filtered = [project for project in projects if project.name != name]

        if len(filtered) == len(projects):
            return False

        self.store.save(filtered)
        return True

    def validate(self) -> list[dict]:
        results = []

        for project in self.store.load():
            project_path = Path(project.path)
            manifest_path = project_path / project.manifest

            results.append(
                {
                    "name": project.name,
                    "path_exists": project_path.exists(),
                    "manifest_exists": manifest_path.exists(),
                    "enabled": project.enabled,
                }
            )

        return results
