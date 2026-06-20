from builder.cli.command_router import CommandRouter


def main():
    print("🚀 Kairos Builder V1 Running")

    router = CommandRouter()

    while True:
        cmd = input("kairos> ")

        result = router.handle(cmd)

        if result == "exit":
            break

        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
