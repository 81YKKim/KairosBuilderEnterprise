from builder.sprint.sprint_manager import SprintManager


def test_sprint_manager_initializes_v2_default_context(tmp_path):
    context_path = tmp_path / "sprint.json"

    manager = SprintManager(str(context_path))
    data = manager.initialize()

    assert data["current_sprint"] == 30
    assert data["status"] == "ready"
    assert data["last_commit"] == "#000029"
    assert data["version"] == "2.0.0-alpha"
    assert context_path.exists()


def test_sprint_manager_preserves_explicit_sprint_number(tmp_path):
    context_path = tmp_path / "sprint.json"

    manager = SprintManager(str(context_path))
    data = manager.initialize(24)

    assert data["current_sprint"] == 24


def test_sprint_manager_builds_commit_message(tmp_path):
    context_path = tmp_path / "sprint.json"

    manager = SprintManager(str(context_path))
    manager.initialize(24)

    assert (
        manager.build_commit_message(
            "feat",
            "builder",
            "add sprint commit manager",
        )
        == "#000024 feat(builder): add sprint commit manager"
    )
