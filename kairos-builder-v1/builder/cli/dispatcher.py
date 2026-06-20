from builder.generator.factory import Factory

class Dispatcher:

    def __init__(self):
        self.factory = Factory()

    def run(self, command, name):

        if command == "generate":
            gen = self.factory.create(name)
            return gen.generate(name)

        if command == "project":
            gen = self.factory.create("project")
            return gen.generate(name)

        return "Unknown command"