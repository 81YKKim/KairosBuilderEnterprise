from builder.domain.generation_request import GenerationRequest
from builder.services.domain_generator import DomainGenerator
from builder.services.generator_service import GeneratorService


def add_generator_commands(subparsers) -> None:
    generate_parser = subparsers.add_parser("generate")
    generate_subparsers = generate_parser.add_subparsers(dest="generate_command")

    domain_parser = generate_subparsers.add_parser("domain")
    domain_parser.add_argument("--name", required=True)
    domain_parser.add_argument("--output-root", default="src/builder/domain")
    domain_parser.set_defaults(func=handle_generate_domain)

    file_parser = generate_subparsers.add_parser("file")
    file_parser.add_argument("--type", required=True)
    file_parser.add_argument("--name", required=True)
    file_parser.add_argument("--output", required=True)
    file_parser.set_defaults(func=handle_generate_file)


def handle_generate_domain(args) -> None:
    output_path = DomainGenerator().generate(
        name=args.name,
        output_root=args.output_root,
    )

    print(f"Generated domain: {output_path}")


def handle_generate_file(args) -> None:
    request = GenerationRequest(
        target_type=args.type,
        name=args.name,
        output_path=args.output,
    )

    result = GeneratorService().generate(request)

    if result.created:
        print(f"Generated {result.target_type}: {result.output_path}")
    else:
        print(f"Already exists: {result.output_path}")
