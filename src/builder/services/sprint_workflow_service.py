from pathlib import Path

from builder.domain.sprint_plan import SprintPlan


class SprintWorkflowService:
    def __init__(self, docs_root: str = "docs") -> None:
        self.docs_root = Path(docs_root)

    def create(self, plan: SprintPlan) -> None:
        self._ensure_directories()

        sprint_file = (
            self.docs_root
            / "sprints"
            / f"Sprint_{plan.sprint_id}_{plan.normalized_name}.md"
        )

        if sprint_file.exists():
            return

        sprint_file.write_text(
            self._build_sprint_document(plan),
            encoding="utf-8",
        )

    def _ensure_directories(self) -> None:
        (self.docs_root / "sprints").mkdir(parents=True, exist_ok=True)

    def _build_sprint_document(self, plan: SprintPlan) -> str:
        return f"""# {plan.display_name}

## Goal

TODO

## Scope

TODO

## Definition of Done

- Implementation completed
- Tests passed
- Documentation updated
- Git committed
"""
