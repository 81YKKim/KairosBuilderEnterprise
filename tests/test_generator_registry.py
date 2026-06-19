from builder.services.domain_generator import DomainGenerator
from builder.services.generator_registry import GeneratorRegistry


def test_register_and_get_generator():
    registry = GeneratorRegistry()

    registry.register("domain", DomainGenerator)

    assert registry.get("domain") is DomainGenerator


def test_list_registered_generator_types():
    registry = GeneratorRegistry()

    registry.register("domain", DomainGenerator)

    assert registry.list_types() == ["domain"]
