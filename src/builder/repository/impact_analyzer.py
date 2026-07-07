from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from builder.repository.change_analyzer import RepositoryChangeAnalyzer
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryTestFile,
)
from builder.repository.qa import QAIssue, RepositoryQA
from builder.repository.query import RepositoryQuery


class QAProvider(Protocol):
    def issues(self) -> tuple[QAIssue, ...]:
        ...


@dataclass(frozen=True, slots=True)
class ImpactScope:
    source_files: tuple[Path, ...]
    changed_modules: tuple[PythonModule, ...]
    affected_modules: tuple[PythonModule, ...]
    affected_packages: tuple[PythonPackage, ...]
    affected_tests: tuple[RepositoryTestFile, ...]
    risk_level: str
    qa_required: bool


@dataclass(frozen=True, slots=True)
class RepositoryImpactAnalyzer:
    intelligence: RepositoryIntelligence
    query: RepositoryQuery
    qa: RepositoryQA | QAProvider
    change_analyzer: RepositoryChangeAnalyzer

    def analyze(
        self,
        paths: tuple[str | Path, ...],
    ) -> ImpactScope:
        change_set = self.change_analyzer.analyze_files(paths)
        source_files = change_set.changed_files
        affected_modules = self.affected_modules(paths)
        affected_tests = self.affected_tests(paths)
        affected_packages = self.affected_packages(paths)

        return ImpactScope(
            source_files=source_files,
            changed_modules=change_set.changed_modules,
            affected_modules=affected_modules,
            affected_packages=affected_packages,
            affected_tests=affected_tests,
            risk_level=self.risk_level(paths),
            qa_required=self._qa_required(source_files),
        )

    def affected_modules(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[PythonModule, ...]:
        return self.change_analyzer.affected_modules(paths)

    def affected_packages(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[PythonPackage, ...]:
        package_names = {
            module.package
            for module in self.affected_modules(paths)
            if module.package
        }
        package_names.update(
            self._changed_init_package_names(paths)
        )

        return tuple(
            package
            for package in self.intelligence.packages()
            if package.name in package_names
        )

    def affected_tests(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[RepositoryTestFile, ...]:
        return self.change_analyzer.affected_tests(paths)

    def risk_level(
        self,
        paths: tuple[str | Path, ...],
    ) -> str:
        normalized_paths = self._normalize_paths(paths)
        affected_modules = self.affected_modules(paths)
        affected_tests = self.affected_tests(paths)
        test_only_change = self._is_test_only_change(normalized_paths)

        if self._has_error_qa_issue():
            return "high"

        if self._has_core_module(affected_modules):
            return "high"

        if test_only_change:
            return "low"

        if len(affected_modules) > 1:
            return "high"

        if self._has_package_init_change(normalized_paths):
            return "medium"

        if affected_modules and not affected_tests:
            return "medium"

        return self.change_analyzer.risk_level(paths)

    def _qa_required(
        self,
        paths: tuple[Path, ...],
    ) -> bool:
        return bool(paths)

    def _has_error_qa_issue(self) -> bool:
        return any(
            issue.severity == "error" for issue in self.qa.issues()
        )

    def _has_core_module(
        self,
        modules: tuple[PythonModule, ...],
    ) -> bool:
        return any(
            module.name.startswith("builder.repository")
            for module in modules
        )

    def _has_package_init_change(
        self,
        paths: tuple[Path, ...],
    ) -> bool:
        return any(path.name == "__init__.py" for path in paths)

    def _changed_init_package_names(
        self,
        paths: tuple[str | Path, ...],
    ) -> set[str]:
        package_names: set[str] = set()

        for path in self._normalize_paths(paths):
            if path.name != "__init__.py":
                continue

            package_name = self._path_to_package_name(path.parent)

            if package_name:
                package_names.add(package_name)

        return package_names

    def _is_test_only_change(
        self,
        paths: tuple[Path, ...],
    ) -> bool:
        if not paths:
            return False

        return all(
            "tests" in path.parts and path.suffix == ".py"
            for path in paths
        )

    def _path_to_package_name(
        self,
        path: Path,
    ) -> str:
        parts = path.parts

        if parts and parts[0] == "src":
            parts = parts[1:]

        return ".".join(parts)

    def _normalize_paths(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[Path, ...]:
        return tuple(
            sorted(
                {
                    self._normalize_path(path) for path in paths
                },
                key=lambda path: path.as_posix(),
            )
        )

    def _normalize_path(
        self,
        path: str | Path,
    ) -> Path:
        path_text = str(path).replace("\\", "/").strip()
        root_text = str(
            self.intelligence.inventory.repository_root
        ).replace("\\", "/")

        if path_text.startswith(root_text):
            path_text = path_text[len(root_text):].lstrip("/")

        return Path(path_text)
