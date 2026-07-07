from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from builder.repository.graph import RepositoryGraph
from builder.repository.inventory import RepositoryInventory
from builder.repository.model import PythonModule, PythonPackage


@dataclass(frozen=True, slots=True)
class RepositoryMetrics:
    total_files: int
    python_files: int
    package_count: int
    module_count: int
    test_count: int
    resource_count: int


@dataclass(frozen=True, slots=True)
class PackageMetrics:
    package_name: str
    module_count: int
    child_package_count: int
    parent_package: str | None
    modules: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ModuleMetrics:
    module_name: str
    package_name: str
    path: Path


@dataclass(frozen=True, slots=True)
class RepositoryIntelligence:
    inventory: RepositoryInventory
    graph: RepositoryGraph

    def repository_summary(self) -> dict[str, int | str]:
        metrics = self.repository_metrics()

        return {
            "repository_root": str(self.inventory.repository_root),
            "total_files": metrics.total_files,
            "python_files": metrics.python_files,
            "package_count": metrics.package_count,
            "module_count": metrics.module_count,
            "test_count": metrics.test_count,
            "resource_count": metrics.resource_count,
        }

    def repository_metrics(self) -> RepositoryMetrics:
        return RepositoryMetrics(
            total_files=self.inventory.total_file_count,
            python_files=self.inventory.python_file_count,
            package_count=self.inventory.package_count,
            module_count=self.inventory.module_count,
            test_count=self.inventory.test_count,
            resource_count=self.inventory.resource_count,
        )

    def packages(self) -> tuple[PythonPackage, ...]:
        return self.graph.packages()

    def modules(self) -> tuple[PythonModule, ...]:
        return self.graph.modules()

    def find_package(
        self,
        package_name: str,
    ) -> PythonPackage | None:
        return self.graph.find_package(package_name)

    def find_module(
        self,
        module_name: str,
    ) -> PythonModule | None:
        return self.graph.find_module(module_name)

    def package_metrics(
        self,
        package_name: str,
    ) -> PackageMetrics | None:
        package = self.find_package(package_name)

        if package is None:
            return None

        modules = self.graph.modules_in_package(package.name)
        child_packages = self.graph.child_packages(package.name)
        parent_package = self.graph.parent_package(package.name)

        return PackageMetrics(
            package_name=package.name,
            module_count=len(modules),
            child_package_count=len(child_packages),
            parent_package=(
                parent_package.name if parent_package is not None else None
            ),
            modules=tuple(module.name for module in modules),
        )

    def module_metrics(
        self,
        module_name: str,
    ) -> ModuleMetrics | None:
        module = self.find_module(module_name)

        if module is None:
            return None

        return ModuleMetrics(
            module_name=module.name,
            package_name=module.package,
            path=module.path,
        )

    def largest_package(self) -> PackageMetrics | None:
        package_metrics = tuple(
            metrics
            for metrics in (
                self.package_metrics(package.name)
                for package in self.packages()
            )
            if metrics is not None
        )

        if not package_metrics:
            return None

        return sorted(
            package_metrics,
            key=lambda metrics: (
                -metrics.module_count,
                metrics.package_name,
            ),
        )[0]

    def empty_packages(self) -> tuple[PythonPackage, ...]:
        return tuple(
            package
            for package in self.packages()
            if not self.graph.modules_in_package(package.name)
        )
