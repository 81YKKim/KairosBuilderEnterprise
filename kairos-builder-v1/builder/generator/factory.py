from builder.generator.domain import DomainGenerator
from builder.generator.project import ProjectGenerator

class Factory:

    def create(self, name):

        if name == "domain":
            return DomainGenerator()

        if name == "project":
            return ProjectGenerator()

        raise Exception("Unknown generator")