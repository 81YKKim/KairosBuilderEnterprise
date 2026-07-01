import pytest
from builder.generator.domain import DomainGenerator
from builder.generator.project_generator import ProjectGenerator
from builder.generator.repository_generator import RepositoryGenerator
from builder.generator.service import ServiceGenerator
from builder.generator.unit_test import UnitTestGenerator
from builder.generator.registry import GeneratorRegistry, default_registry


def test_generator_registry_registers_and_creates_generator():
    registry = GeneratorRegistry()

    registry.register("domain", DomainGenerator)

    generator = registry.create("domain")

    assert isinstance(generator, DomainGenerator)


def test_default_registry_creates_project_generator():
    registry = default_registry()

    generator = registry.create("project")

    assert isinstance(generator, ProjectGenerator)


def test_default_registry_creates_all_v1_generators():
    registry = default_registry()

    assert isinstance(registry.create("domain"), DomainGenerator)
    assert isinstance(registry.create("service"), ServiceGenerator)
    assert isinstance(registry.create("unit_test"), UnitTestGenerator)
    assert isinstance(registry.create("project"), ProjectGenerator)
    assert isinstance(registry.create("repository"), RepositoryGenerator)


def test_generator_registry_unknown_generator():
    registry = GeneratorRegistry()

    with pytest.raises(ValueError, match="Unknown generator"):
        registry.create("unknown")
