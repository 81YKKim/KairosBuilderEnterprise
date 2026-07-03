from __future__ import annotations

from builder.application.builder_service import BuilderService
from builder.sprint.sprint_runner import SprintRunner


class CommandRouter:
    def __init__(
        self,
        service: BuilderService | None = None,
    ) -> None:
        self.service = service or BuilderService()
        self.sprint_runner = SprintRunner()

    def handle(self, command: str):
        command = command.strip()
        parts = command.split()

        try:
            return self._route(command, parts)
        except ValueError as exc:
            return {
                "error": str(exc),
            }

    def _route(
        self,
        command: str,
        parts: list[str],
    ):
        if command == "scan all":
            return self.service.run_full_market_scan()

        if command == "run auto":
            return self.service.execute_top_scan(10000)

        if command == "run live":
            return self.service.start_live(10000)

        if command == "stop":
            return self.service.stop_trading()

        if len(parts) == 2 and parts[0] == "new":
            return self.service.create_project(parts[1])

        if len(parts) == 3 and parts[0] == "generate":
            return self.service.generate(
                parts[1],
                parts[2],
            )

        if command == "workflow verify":
            return self.service.workflow_verify()

        if (
            len(parts) >= 4
            and parts[:2] == ["workflow", "commit"]
        ):
            scope = parts[2]
            message = "-".join(parts[3:])

            return self.service.workflow_commit_message(
                scope,
                message,
            )

        if (
            len(parts) == 3
            and parts[:2] == ["sprint", "run"]
        ):
            return self.sprint_runner.run(
                int(parts[2])
            )

        return {
            "error": f"Unknown command: {command}",
        }