from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from builder.repository.intelligence import (
    RepositoryIntelligence,
    RepositoryMetrics,
)
from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryTestFile,
)
from builder.repository.qa import RepositoryQA
from builder.repository.query import RepositoryQuery


@dataclass(frozen=True, slots=True)
class RepositoryIndex:
    packages_by_name: dict[str, PythonPackage]
    modules_by_name: dict[str, PythonModule]
    modules_by_package: dict[str, tuple[PythonModule, ...]]
    tests_by_module: dict[str, tuple[RepositoryTestFile, ...]]
    resources_by_suffix: dict[str, tuple[Path, ...]]

    def find_module(
        self,
        name: str,
    ) -> PythonModule | None:
        return self.modules_by_name.get(name)

    def find_package(
        self,
        name: str,
    ) -> PythonPackage | None:
        return self.packages_by_name.get(name)

    def modules_in_package(
        self,
        package: str,
    ) -> tuple[PythonModule, ...]:
        return self.modules_by_package.get(package, ())

    def tests_for_module(
        self,
        module: str,
    ) -> tuple[RepositoryTestFile, ...]:
        return self.tests_by_module.get(module, ())


@dataclass(frozen=True, slots=True)
class RepositoryCache:
    snapshot_id: str
    created_at: str
    index: RepositoryIndex
    metrics: RepositoryMetrics
    qa_summary: dict[str, int | bool | tuple[str, ...]]


def build_index(
    intelligence: RepositoryIntelligence,
    query: RepositoryQuery,
    qa: RepositoryQA,
) -> RepositoryIndex:
    packages = tuple(
        sorted(
            intelligence.packages(),
            key=lambda package: package.name,
        )
    )
    modules = tuple(
        sorted(
            intelligence.modules(),
            key=lambda module: module.name,
        )
    )

    return RepositoryIndex(
        packages_by_name={
            package.name: package for package in packages
        },
        modules_by_name={
            module.name: module for module in modules
        },
        modules_by_package=_build_modules_by_package(
            packages,
            modules,
        ),
        tests_by_module=_build_tests_by_module(
            modules,
            query,
        ),
        resources_by_suffix=_build_resources_by_suffix(
            intelligence.inventory.resource_files,
        ),
    )


def create_cache(
    intelligence: RepositoryIntelligence,
    query: RepositoryQuery,
    qa: RepositoryQA,
    created_at: str | None = None,
) -> RepositoryCache:
    index = build_index(
        intelligence,
        query,
        qa,
    )
    metrics = intelligence.repository_metrics()
    qa_result = qa.run_all()
    qa_summary = {
        "issue_count": qa_result.issue_count,
        "passed": qa_result.passed,
        "failed_checks": qa_result.failed_checks,
    }

    return RepositoryCache(
        snapshot_id=_build_snapshot_id(
            intelligence,
            metrics,
            qa_summary,
        ),
        created_at=created_at or datetime.now(UTC).isoformat(),
        index=index,
        metrics=metrics,
        qa_summary=qa_summary,
    )


def _build_modules_by_package(
    packages: tuple[PythonPackage, ...],
    modules: tuple[PythonModule, ...],
) -> dict[str, tuple[PythonModule, ...]]:
    return {
        package.name: tuple(
            module
            for module in modules
            if module.package == package.name
        )
        for package in packages
    }


def _build_tests_by_module(
    modules: tuple[PythonModule, ...],
    query: RepositoryQuery,
) -> dict[str, tuple[RepositoryTestFile, ...]]:
    return {
        module.name: tuple(query.tests_for_module(module.name).items)
        for module in modules
    }


def _build_resources_by_suffix(
    resource_files: tuple[Path, ...],
) -> dict[str, tuple[Path, ...]]:
    suffixes = sorted(
        {
            path.suffix for path in resource_files
        }
    )

    return {
        suffix: tuple(
            sorted(
                (
                    path
                    for path in resource_files
                    if path.suffix == suffix
                ),
                key=lambda path: path.as_posix(),
            )
        )
        for suffix in suffixes
    }


def _build_snapshot_id(
    intelligence: RepositoryIntelligence,
    metrics: RepositoryMetrics,
    qa_summary: dict[str, int | bool | tuple[str, ...]],
) -> str:
    parts = [
        str(intelligence.inventory.repository_root),
        str(metrics.total_files),
        str(metrics.python_files),
        str(metrics.package_count),
        str(metrics.module_count),
        str(metrics.test_count),
        str(metrics.resource_count),
        str(qa_summary["issue_count"]),
        str(qa_summary["passed"]),
        ",".join(qa_summary["failed_checks"]),
    ]
    digest = sha256("|".join(parts).encode("utf-8")).hexdigest()

    return digest[:16]
