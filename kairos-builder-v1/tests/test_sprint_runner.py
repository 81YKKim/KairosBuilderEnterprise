from builder.sprint.sprint_runner import SprintRunner
from builder.cli.command_router import CommandRouter


def test_sprint_runner_can_run():
    runner = SprintRunner()

    assert runner.create(34) == "Sprint #000034 create completed"
    assert runner.verify(34) == "Sprint #000034 verify completed"
    assert runner.commit(34) == "Sprint #000034 commit completed"
    assert runner.run(34) == "Sprint #000034 run completed"


def test_command_router_supports_sprint_run():
    result = CommandRouter().handle("sprint run 34")

    assert result == "Sprint #000034 run completed"
