from builder.application.builder_service import BuilderService
from builder.sprint.sprint_runner import SprintRunner


class CommandRouter:
    def __init__(self, service: BuilderService | None = None):
        self.service = service or BuilderService()

    def handle(self, command: str):
        parts = command.strip().split()

        if not parts:
            return None

        if parts[0] in ("exit", "quit"):
            return "exit"

        if parts == ["workflow", "verify"]:
            return self.service.workflow_verify()

        if len(parts) == 4 and parts[0] == "workflow" and parts[1] == "commit":
            return self.service.workflow_commit_message(parts[2], parts[3])

        if len(parts) == 3 and parts[0] == "generate":
            return self.service.generate(parts[1], parts[2])

        if len(parts) == 2 and parts[0] == "project":
            return self.service.create_project(parts[1])

        if len(parts) == 3 and parts[0] == "sprint" and parts[1] == "run":
            return SprintRunner().run(int(parts[2]))

        return f"Unknown command: {command}"
