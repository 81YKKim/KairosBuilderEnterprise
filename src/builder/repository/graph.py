from __future__ import annotations

from dataclasses import dataclass

from builder.repository.inventory import RepositoryInventory
from builder.repository.model import PythonModule, PythonPackage


@dataclass(frozen=True, slots=True)
class RepositoryGraph:
    package_graph: tuple[PythonPackage, ...]
    module_graph: tuple[PythonModule, ...]
    package_modules: dict[str, tuple[PythonModule, ...]]
    parent_packages: dict[str, str | None]
    child_package_map: dict[str, tuple[PythonPackage, ...]]
    package_lookup: dict[str, PythonPackage]
    module_lookup: dict[str, PythonModule]

    @property
    def package_names(self) -> tuple[str, ...]:
        return tuple(package.name for package in self.package_graph)

    @property
    def module_names(self) -> tuple[str, ...]:
        return tuple(module.name for module in self.module_graph)

    def find_package(
        self,
        name: str,
    ) -> PythonPackage | None:
        return self.package_lookup.get(name)

    def find_module(
        self,
        name: str,
    ) -> PythonModule | None:
        return self.module_lookup.get(name)

    def modules_in_package(
        self,
        package_name: str,
    ) -> tuple[PythonModule, ...]:
        return self.package_modules.get(package_name, ())

    def packages(self) -> tuple[PythonPackage, ...]:
        return self.package_graph

    def modules(self) -> tuple[PythonModule, ...]:
        return self.module_graph

    def parent_package(
        self,
        package_name: str,
    ) -> PythonPackage | None:
        parent_name = self.parent_packages.get(package_name)

        if parent_name is None:
            return None

        return self.package_lookup.get(parent_name)

    def child_packages(
        self,
        package_name: str,
    ) -> tuple[PythonPackage, ...]:
        return self.child_package_map.get(package_name, ())


class RepositoryGraphBuilder:
    def build(
        self,
        inventory: RepositoryInventory,
    ) -> RepositoryGraph:
        packages = tuple(
            sorted(
                inventory.packages,
                key=lambda package: package.name,
            )
        )
        modules = tuple(
            sorted(
                inventory.modules,
                key=lambda module: module.name,
            )
        )
        package_lookup = {
            package.name: package for package in packages
        }
        module_lookup = {
            module.name: module for module in modules
        }
        package_modules = self._build_package_modules(
            packages,
            modules,
        )
        parent_packages = self._build_parent_packages(
            packages,
        )
        child_package_map = self._build_child_package_map(
            packages,
            parent_packages,
        )

        return RepositoryGraph(
            package_graph=packages,
            module_graph=modules,
            package_modules=package_modules,
            parent_packages=parent_packages,
            child_package_map=child_package_map,
            package_lookup=package_lookup,
            module_lookup=module_lookup,
        )

    def _build_package_modules(
        self,
        packages: tuple[PythonPackage, ...],
        modules: tuple[PythonModule, ...],
    ) -> dict[str, tuple[PythonModule, ...]]:
        package_modules: dict[str, tuple[PythonModule, ...]] = {}

        for package in packages:
            package_modules[package.name] = tuple(
                module
                for module in modules
                if module.package == package.name
            )

        return package_modules

    def _build_parent_packages(
        self,
        packages: tuple[PythonPackage, ...],
    ) -> dict[str, str | None]:
        package_names = {
            package.name for package in packages
        }
        parent_packages: dict[str, str | None] = {}

        for package in packages:
            parent_name = self._parent_name(package.name)
            parent_packages[package.name] = (
                parent_name if parent_name in package_names else None
            )

        return parent_packages

    def _build_child_package_map(
        self,
        packages: tuple[PythonPackage, ...],
        parent_packages: dict[str, str | None],
    ) -> dict[str, tuple[PythonPackage, ...]]:
        children: dict[str, list[PythonPackage]] = {
            package.name: [] for package in packages
        }

        for package in packages:
            parent_name = parent_packages[package.name]

            if parent_name is None:
                continue

            children[parent_name].append(package)

        return {
            package_name: tuple(
                sorted(
                    child_packages,
                    key=lambda package: package.name,
                )
            )
            for package_name, child_packages in children.items()
        }

    def _parent_name(
        self,
        package_name: str,
    ) -> str | None:
        if "." not in package_name:
            return None

        return package_name.rsplit(".", 1)[0]
