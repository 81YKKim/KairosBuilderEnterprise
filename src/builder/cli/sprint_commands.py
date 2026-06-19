from builder.domain.sprint_plan import SprintPlan
from builder.services.sprint_workflow_service import SprintWorkflowService


def add_sprint_commands(subparsers) -> None:
    sprint_parser = subparsers.add_parser("sprint")
    sprint_subparsers = sprint_parser.add_subparsers(dest="sprint_command")

    create_parser = sprint_subparsers.add_parser("create")
    create_parser.add_argument("--number", required=True, type=int)
    create_parser.add_argument("--name", required=True)
    create_parser.set_defaults(func=handle_sprint_create)


def handle_sprint_create(args) -> None:
    plan = SprintPlan(number=args.number, name=args.name)
    service = SprintWorkflowService()
    service.create(plan)

    print(f"Created {plan.display_name}")
