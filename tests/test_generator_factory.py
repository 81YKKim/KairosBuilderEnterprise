from builder.services.cli_generator import CLIGenerator
from builder.services.domain_generator import DomainGenerator
from builder.services.generator_factory import GeneratorFactory
from builder.services.service_generator import ServiceGenerator
from builder.services.test_generator import TestGenerator


def test_create_domain_generator():
    factory = GeneratorFactory()

    generator = factory.create("domain")

    assert isinstance(generator, DomainGenerator)


def test_create_service_generator():
    factory = GeneratorFactory()

    generator = factory.create("service")

    assert isinstance(generator, ServiceGenerator)


def test_create_cli_generator():
    factory = GeneratorFactory()

    generator = factory.create("cli")

    assert isinstance(generator, CLIGenerator)


def test_create_test_generator():
    factory = GeneratorFactory()

    generator = factory.create("test")

    assert isinstance(generator, TestGenerator)
