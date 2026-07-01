from builder.context.project_context import ProjectContext


def test_project_context_version(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.version() == "1.0.0"


def test_project_context_repository(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.repository() == "Kairos-Builder-Enterprise-V1"


def test_project_context_commit(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.last_commit() == "#000032"


def test_project_context_test_status(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.test_status() == "PASS"


def test_project_context_sprint(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.current_sprint() == 33


def test_project_context_bump(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))

    context.manager.initialize()

    assert context.bump_sprint() == 34
