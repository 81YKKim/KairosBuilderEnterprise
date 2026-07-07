from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.model import (
    PythonModule,
    PythonPackage,
)


@dataclass(frozen=True, slots=True)
class QueryResource:
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class QueryResult:
    items: tuple[Any, ...]
    count: int
    query: str
    filters: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class RepositoryQuery:
    intelligence: RepositoryIntelligence

    def packages(self) -> QueryResult:
        return self._result(
            query="packages",
            items=self.intelligence.packages(),
        )

    def modules(self) -> QueryResult:
        return self._result(
            query="modules",
            items=self.intelligence.modules(),
        )

    def find_package(
        self,
        name: str,
    ) -> QueryResult:
        package = self.intelligence.find_package(name)

        return self._result(
            query="find_package",
            items=self._optional_item(package),
            filters=(("name", name),),
        )

    def find_module(
        self,
        name: str,
    ) -> QueryResult:
        module = self.intelligence.find_module(name)

        return self._result(
            query="find_module",
            items=self._optional_item(module),
            filters=(("name", name),),
        )

    def find_tests(self) -> QueryResult:
        return self._result(
            query="find_tests",
            items=self.intelligence.inventory.test_files,
        )

    def tests_for_module(
        self,
        module_name: str,
    ) -> QueryResult:
        module_leaf_name = module_name.rsplit(".", 1)[-1]
        expected_test_name = f"test_{module_leaf_name}"
        tests = tuple(
            test
            for test in self.intelligence.inventory.test_files
            if test.name == expected_test_name
        )

        return self._result(
            query="tests_for_module",
            items=tests,
            filters=(("module", module_name),),
        )

    def find_by_name(
        self,
        name: str,
    ) -> QueryResult:
        items = tuple(
            item
            for item in self._queryable_items()
            if self._item_name(item) == name
        )

        return self._result(
            query="find_by_name",
            items=items,
            filters=(("name", name),),
        )

    def search(
        self,
        text: str,
    ) -> QueryResult:
        normalized_text = text.casefold()
        items = tuple(
            item
            for item in self._queryable_items()
            if normalized_text in self._search_text(item)
        )

        return self._result(
            query="search",
            items=items,
            filters=(("text", text),),
        )

    def where(
        self,
        source: str,
        predicate: Callable[[Any], bool],
    ) -> QueryResult:
        source_items = self._source_items(source)
        items = tuple(
            item for item in source_items if predicate(item)
        )

        return self._result(
            query="where",
            items=items,
            filters=(("source", source),),
        )

    def find_modules_in_package(
        self,
        package_name: str,
    ) -> QueryResult:
        items = self.intelligence.graph.modules_in_package(package_name)

        return self._result(
            query="find_modules_in_package",
            items=items,
            filters=(("package", package_name),),
        )

    def find_importers(
        self,
        module_name: str,
    ) -> QueryResult:
        return self._result(
            query="find_importers",
            items=(),
            filters=(("module", module_name),),
        )

    def find_dependents(
        self,
        module_name: str,
    ) -> QueryResult:
        return self._result(
            query="find_dependents",
            items=(),
            filters=(("module", module_name),),
        )

    def _queryable_items(self) -> tuple[Any, ...]:
        return (
            self.intelligence.packages()
            + self._non_test_modules()
            + self.intelligence.inventory.test_files
            + self._resource_items()
        )

    def _source_items(
        self,
        source: str,
    ) -> tuple[Any, ...]:
        if source == "packages":
            return self.intelligence.packages()

        if source == "modules":
            return self.intelligence.modules()

        if source == "tests":
            return self.intelligence.inventory.test_files

        if source == "resources":
            return self._resource_items()

        return ()

    def _non_test_modules(self) -> tuple[PythonModule, ...]:
        return tuple(
            module
            for module in self.intelligence.modules()
            if "tests" not in module.path.parts
        )

    def _resource_items(self) -> tuple[QueryResource, ...]:
        return tuple(
            QueryResource(
                name=path.stem,
                path=path,
            )
            for path in self.intelligence.inventory.resource_files
        )

    def _item_name(
        self,
        item: Any,
    ) -> str:
        return getattr(item, "name", "")

    def _search_text(
        self,
        item: Any,
    ) -> str:
        name = self._item_name(item)
        path = getattr(item, "path", "")
        resource_content = self._resource_content(item)

        return f"{name} {path} {resource_content}".casefold()

    def _resource_content(
        self,
        item: Any,
    ) -> str:
        if not isinstance(item, QueryResource):
            return ""

        path = self.intelligence.inventory.repository_root / item.path

        if not path.is_file():
            return ""

        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ""

    def _optional_item(
        self,
        item: PythonPackage | PythonModule | None,
    ) -> tuple[PythonPackage | PythonModule, ...]:
        if item is None:
            return ()

        return (item,)

    def _result(
        self,
        query: str,
        items: tuple[Any, ...],
        filters: tuple[tuple[str, str], ...] = (),
    ) -> QueryResult:
        return QueryResult(
            items=items,
            count=len(items),
            query=query,
            filters=filters,
        )
