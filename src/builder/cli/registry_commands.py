from builder.domain.project import Project
from builder.services.registry_service import RegistryService


def add_registry_commands(subparsers) -> None:
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--name", required=True)
    register_parser.add_argument("--path", required=True)
    register_parser.add_argument("--language", default="Python")
    register_parser.add_argument("--branch", default="main")
    register_parser.add_argument("--manifest", default="builder.manifest.json")
    register_parser.set_defaults(func=handle_register)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=handle_list)

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("name")
    show_parser.set_defaults(func=handle_show)

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("name")
    remove_parser.set_defaults(func=handle_remove)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.set_defaults(func=handle_validate)


def handle_register(args) -> None:
    service = RegistryService()
    project = Project(
        name=args.name,
        path=args.path,
        language=args.language,
        branch=args.branch,
        manifest=args.manifest,
    )
    service.register(project)
    print(f"Registered project: {project.name}")


def handle_list(args) -> None:
    service = RegistryService()
    projects = service.list_projects()

    if not projects:
        print("No registered projects.")
        return

    for project in projects:
        print(f"- {project.name} | {project.path} | {project.branch}")


def handle_show(args) -> None:
    service = RegistryService()
    project = service.find(args.name)

    if project is None:
        print(f"Project not found: {args.name}")
        return

    print(f"Name     : {project.name}")
    print(f"Path     : {project.path}")
    print(f"Language : {project.language}")
    print(f"Branch   : {project.branch}")
    print(f"Manifest : {project.manifest}")
    print(f"Enabled  : {project.enabled}")


def handle_remove(args) -> None:
    service = RegistryService()
    removed = service.remove(args.name)

    if removed:
        print(f"Removed project: {args.name}")
    else:
        print(f"Project not found: {args.name}")


def handle_validate(args) -> None:
    service = RegistryService()
    results = service.validate()

    if not results:
        print("No registered projects.")
        return

    for result in results:
        print(f"- {result['name']}")
        print(f"  path_exists     : {result['path_exists']}")
        print(f"  manifest_exists : {result['manifest_exists']}")
        print(f"  enabled         : {result['enabled']}")
