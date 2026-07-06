from builder.cli.command_router import CommandRouter


def test_command_router_workflow_verify():
    router = CommandRouter()

    assert router.handle("workflow verify") == "pytest\ngit status"


def test_command_router_workflow_commit_message():
    router = CommandRouter()

    result = router.handle("workflow commit workflow connect-cli")

    assert result.startswith("#000030 feat(workflow):")
    assert "connect-cli" in result