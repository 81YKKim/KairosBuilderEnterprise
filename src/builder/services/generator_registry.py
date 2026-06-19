from typing import Type

from builder.services.base_generator import BaseGenerator


class GeneratorRegistry:
    def __init__(self) -> None:
        self._generators: dict[str, Type[BaseGenerator]] = {}

    def register(self, generator_type: str, generator_class: Type[BaseGenerator]) -> None:
        self._generators[generator_type] = generator_class

    def get(self, generator_type: str) -> Type[BaseGenerator]:
        if generator_type not in self._generators:
            raise KeyError(f"Generator not registered: {generator_type}")

        return self._generators[generator_type]

    def list_types(self) -> list[str]:
        return sorted(self._generators.keys())
