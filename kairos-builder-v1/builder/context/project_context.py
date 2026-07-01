from builder.project.project_state_manager import ProjectStateManager


class ProjectContext:
    def __init__(self, state_path: str = "builder/context/project.json") -> None:
        self.manager = ProjectStateManager(state_path)

    def current_sprint(self) -> int:
        return self.manager.current_sprint()

    def bump_sprint(self) -> int:
        return self.manager.bump_sprint()

    def version(self) -> str:
        return self.manager.load()["version"]

    def repository(self) -> str:
        return self.manager.load()["repository"]

    def last_commit(self) -> str:
        return self.manager.load()["last_commit"]

    def test_status(self) -> str:
        return self.manager.load()["test_status"]
