from builder.generator.domain import DomainGenerator

class ProjectGenerator:

    def generate(self, name):

        return [DomainGenerator().generate(name)]