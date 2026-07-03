from builder.application.builder_service import BuilderService
from builder.cli.command_router import CommandRouter


def main():
    print("🚀 Kairos Builder V1 Running")

    service = BuilderService()
    router = CommandRouter(service)

    while True:
        try:
            cmd = input("kairos> ").strip()
        except EOFError:
            break

        if cmd in {"exit", "quit", "q"}:
            break

        if not cmd:
            continue

        print(router.handle(cmd))


if __name__ == "__main__":
    main()