from builder.domain.sprint_plan import SprintPlan
from builder.services.sprint_workflow_service import SprintWorkflowService


def test_sprint_plan_formatting():
    plan = SprintPlan(number=9, name="Builder Workflow Engine")

    assert plan.sprint_id == "000009"
    assert plan.normalized_name == "Builder_Workflow_Engine"
    assert plan.display_name == "Sprint #000009 - Builder Workflow Engine"


def test_sprint_workflow_creates_sprint_document(tmp_path):
    service = SprintWorkflowService(docs_root=str(tmp_path))
    plan = SprintPlan(number=9, name="Builder Workflow Engine")

    service.create(plan)

    sprint_file = tmp_path / "sprints" / "Sprint_000009_Builder_Workflow_Engine.md"

    assert sprint_file.exists()
    assert "Sprint #000009 - Builder Workflow Engine" in sprint_file.read_text(encoding="utf-8")
