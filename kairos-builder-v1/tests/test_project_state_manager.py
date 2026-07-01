from builder.project.project_state_manager import ProjectStateManager


def test_project_state_manager_initializes(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    data = manager.initialize()

    assert data["project"] == "Kairos Builder Enterprise V1"
    assert data["current_sprint"] == 33
    assert data["test_status"] == "PASS"


def test_project_state_manager_load(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    manager.initialize()

    data = manager.load()

    assert data["repository"] == "Kairos-Builder-Enterprise-V1"
    assert data["state"] == "development"


def test_bump_sprint(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    manager.initialize()

    assert manager.bump_sprint() == 34
    assert manager.current_sprint() == 34


def test_set_last_commit(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    manager.initialize()
    manager.set_last_commit("#000033")

    assert manager.load()["last_commit"] == "#000033"


def test_set_test_status(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    manager.initialize()
    manager.set_test_status("SUCCESS")

    assert manager.load()["test_status"] == "SUCCESS"


def test_set_repository(tmp_path):
    manager = ProjectStateManager(str(tmp_path / "project.json"))

    manager.initialize()
    manager.set_repository("kairos-builder")

    assert manager.load()["repository"] == "kairos-builder"
