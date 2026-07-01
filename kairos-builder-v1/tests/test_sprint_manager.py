from builder.sprint.sprint_manager import SprintManager


def test_sprint_manager_initializes_context(tmp_path):
    context_path = tmp_path / "sprint.json"

    manager = SprintManager(str(context_path))
    data = manager.initialize(24)

    assert data["current_sprint"] == 24
    assert data["status"] == "ready"
    assert context_path.exists()


def test_sprint_manager_builds_commit_message(tmp_path):
    context_path = tmp_path / "sprint.json"

    manager = SprintManager(str(context_path))
    manager.initialize(24)

    assert (
        manager.build_commit_message("feat", "builder", "add sprint commit manager")
        == "#000024 feat(builder): add sprint commit manager"
    )
