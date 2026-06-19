from builder.domain.generation_request import GenerationRequest
from builder.services.generator_service import GeneratorService


def add_generator_commands(subparsers) -> None:
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--type", required=True)
    generate_parser.add_argument("--name", required=True)
    generate_parser.add_argument("--output", required=True)
    generate_parser.set_defaults(func=handle_generate)


def handle_generate(args) -> None:
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
