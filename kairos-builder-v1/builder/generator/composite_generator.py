from __future__ import annotations

from pathlib import Path
from typing import Any

from builder.generator.base_generator import BaseGenerator


class CompositeGenerator(BaseGenerator):
    """
    Base class for generators that orchestrate multiple child generators.
    """

    category = "composite"

    def create_project_root(
        self,
        output_root: str | Path,
        name: str,
    ) -> Path:
        project_root = Path(output_root) / name
        project_root.mkdir(parents=True, exist_ok=True)
        return project_root

    def create_folders(
        self,
        folders: list[str | Path],
    ) -> tuple[Path, ...]:
        created: list[Path] = []

        for folder in folders:
            created.append(self.ensure_directory(folder))

        return tuple(created)

    def run_generator(
        self,
        generator: Any,
        name: str,
        output_root: str | Path,
    ):
        """
        Execute a child generator.
        """
        return generator.generate(name, str(output_root))

    def run_generators(
        self,
        jobs: list[tuple[Any, str, str | Path]],
    ) -> tuple[Any, ...]:
        """
        Execute multiple generators sequentially.
        """
        results = []

        for generator, name, output_root in jobs:
            results.append(
                self.run_generator(
                    generator,
                    name,
                    output_root,
                )
            )

        return tuple(results)

    def collect_results(
        self,
        *results: Any,
    ) -> tuple[Any, ...]:
        """
        Flatten nested generator results.
        """
        collected = []

        for result in results:
            if result is None:
                continue

            if isinstance(result, (list, tuple)):
                collected.extend(result)
            else:
                collected.append(result)

        return tuple(collected)