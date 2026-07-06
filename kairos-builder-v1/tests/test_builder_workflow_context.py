from builder.context.project_context import ProjectContext
from builder.workflow.builder_workflow import BuilderWorkflow


def test_builder_workflow_has_context(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    workflow = BuilderWorkflow(context=context)

    assert workflow.context is context


def test_builder_workflow_current_sprint(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    workflow = BuilderWorkflow(context=context)

    assert workflow.current_sprint() == 29


def test_builder_workflow_project_version(tmp_path):
    context = ProjectContext(str(tmp_path / "project.json"))
    context.manager.initialize()

    workflow = BuilderWorkflow(context=context)

    assert workflow.project_version() == "2.0.0-alpha"
