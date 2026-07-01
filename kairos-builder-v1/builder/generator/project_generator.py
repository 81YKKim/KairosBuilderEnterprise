from pathlib import Path

from builder.generator.repository_generator import RepositoryGenerator


class ProjectGenerator:
    def __init__(self, repository_generator: RepositoryGenerator | None = None) -> None:
        self.repository_generator = repository_generator or RepositoryGenerator()

    def generate(self, name: str, output_root: str = "output/projects") -> Path:
        return self.repository_generator.generate(name, output_root)
