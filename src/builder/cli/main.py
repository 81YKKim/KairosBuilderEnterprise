import argparse
import sys
from builder import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="builder", description="Kairos Builder Enterprise CLI")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("version", help="Show Builder version")
    sub.add_parser("info", help="Show Builder information")
    sub.add_parser("doctor", help="Check Builder environment")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print("Kairos Builder Enterprise v" + __version__)
        return 0

    if args.command == "info":
        print("Kairos Builder Enterprise")
        print("Mode: Enterprise AI Development Platform")
        print("Core: Python")
        return 0

    if args.command == "doctor":
        print("Doctor: OK")
        print("Python: " + sys.version.split()[0])
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
