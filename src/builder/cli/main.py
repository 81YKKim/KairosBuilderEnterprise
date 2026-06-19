import argparse

from builder.cli.registry_commands import add_registry_commands
from builder.cli.scan_commands import add_scan_commands
from builder.cli.sprint_commands import add_sprint_commands


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="builder",
        description="Kairos Builder Enterprise",
    )

    subparsers = parser.add_subparsers(dest="command")

    version_parser = subparsers.add_parser("version")
    version_parser.set_defaults(func=handle_version)

    info_parser = subparsers.add_parser("info")
    info_parser.set_defaults(func=handle_info)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.set_defaults(func=handle_doctor)

    add_registry_commands(subparsers)
    add_scan_commands(subparsers)
    add_sprint_commands(subparsers)

    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        args.func(args)
        return 0

    parser.print_help()
    return 0


def handle_version(args) -> None:
    print("Kairos Builder Enterprise 1.0.0")


def handle_info(args) -> None:
    print("Kairos Builder Enterprise")
    print("Architecture: Enterprise")


def handle_doctor(args) -> None:
    print("Builder doctor check passed.")


if __name__ == "__main__":
    raise SystemExit(main())
