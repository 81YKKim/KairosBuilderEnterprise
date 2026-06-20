from builder.generator.factory import Factory


class CommandRouter:
    def __init__(self):
        self.factory = Factory()

    def handle(self, command: str):
        parts = command.strip().split()

        if not parts:
            return None

        if parts[0] in ("exit", "quit"):
            return "exit"

        if len(parts) == 3 and parts[0] == "generate":
            generator_type = parts[1]
            name = parts[2]
            gen = self.factory.create(generator_type)
            return gen.generate(name)

        if len(parts) == 2 and parts[0] == "project":
            name = parts[1]
            gen = self.factory.create("project")
            return gen.generate(name)

        return f"Unknown command: {command}"
