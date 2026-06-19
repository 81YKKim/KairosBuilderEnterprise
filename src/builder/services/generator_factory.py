from builder.services.base_generator import BaseGenerator
from builder.services.cli_generator import CLIGenerator
from builder.services.domain_generator import DomainGenerator
from builder.services.generator_registry import GeneratorRegistry
from builder.services.service_generator import ServiceGenerator
from builder.services.test_generator import TestGenerator


class GeneratorFactory:
    def __init__(self, registry: GeneratorRegistry | None = None) -> None:
        self.registry = registry or self._default_registry()

    def create(self, generator_type: str) -> BaseGenerator:
        generator_class = self.registry.get(generator_type)
        return generator_class()

    def _default_registry(self) -> GeneratorRegistry:
        registry = GeneratorRegistry()
        registry.register("domain", DomainGenerator)
        registry.register("service", ServiceGenerator)
        registry.register("cli", CLIGenerator)
        registry.register("test", TestGenerator)
        return registry
