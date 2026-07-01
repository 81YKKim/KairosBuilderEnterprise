from builder.sprint.sprint_manager import SprintManager
from builder.workflow.builder_workflow import BuilderWorkflow


def test_builder_workflow_creates_commit_plan(tmp_path):
    context_path = tmp_path / "sprint.json"
    sprint_manager = SprintManager(str(context_path))
    sprint_manager.initialize(25)

    workflow = BuilderWorkflow(sprint_manager)
    plan = workflow.plan_commit("feat", "workflow", "add builder workflow engine")

    assert plan["sprint"] == "#000025"
    assert (
        plan["commit_message"]
        == "#000025 feat(workflow): add builder workflow engine"
    )
    assert plan["steps"] == [
        "run_tests",
        "git_add",
        "git_commit",
        "git_push",
    ]


def test_builder_workflow_verify_plan():
    workflow = BuilderWorkflow()

    assert workflow.verify_plan() == [
        "pytest",
        "git status",
    ]
