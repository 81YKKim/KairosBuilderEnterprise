from builder.application.builder_service import BuilderService
from builder.context.project_context import ProjectContext


def test_builder_service_has_project_context(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    service = BuilderService(context=context)

    assert service.context is context


def test_builder_service_project_version(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    service = BuilderService(context=context)

    assert service.project_version() == "1.0.0"


def test_builder_service_project_sprint(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    service = BuilderService(context=context)

    assert service.project_sprint() == 33
