from builder.generator.adapter_generator import AdapterGenerator
from builder.generator.desktop_generator import DesktopGenerator
from builder.generator.domain import DomainGenerator
from builder.generator.page_generator import PageGenerator
from builder.generator.project_generator import ProjectGenerator
from builder.generator.repository_generator import RepositoryGenerator
from builder.generator.service import ServiceGenerator
from builder.generator.unit_test import UnitTestGenerator
from builder.generator.viewmodel_generator import ViewModelGenerator
from builder.generator.widget_generator import WidgetGenerator


class GeneratorRegistry:
    def __init__(self):
        self._generators = {}

        self.register("desktop", DesktopGenerator)
        self.register("domain", DomainGenerator)
        self.register("service", ServiceGenerator)
        self.register("unit_test", UnitTestGenerator)
        self.register("project", ProjectGenerator)
        self.register("repository", RepositoryGenerator)

        self.register("page", PageGenerator)
        self.register("widget", WidgetGenerator)
        self.register("viewmodel", ViewModelGenerator)
        self.register("adapter", AdapterGenerator)

        self.register("view", ViewModelGenerator)

    def register(self, name: str, generator_cls):
        self._generators[name] = generator_cls

    def create(self, name: str):
        if name not in self._generators:
            raise ValueError(f"Unknown generator: {name}")

        return self._generators[name]()

    def names(self):
        return tuple(sorted(self._generators.keys()))

    def describe(self, name: str):
        if name not in self._generators:
            return {"error": "unknown generator"}

        cls = self._generators[name]

        return {
            "name": name,
            "class": cls.__name__,
            "module": cls.__module__,
        }


def default_registry():
    return GeneratorRegistry()