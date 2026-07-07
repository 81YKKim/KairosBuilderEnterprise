from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryTestFile,
)
from builder.repository.qa import RepositoryQA
from builder.repository.query import RepositoryQuery


@dataclass(frozen=True, slots=True)
class ChangeImpact:
    affected_packages: tuple[PythonPackage, ...]
    affected_modules: tuple[PythonModule, ...]
    affected_tests: tuple[RepositoryTestFile, ...]
    qa_required: bool
    risk_level: str


@dataclass(frozen=True, slots=True)
class ChangeSet:
    changed_files: tuple[Path, ...]
    changed_python_files: tuple[Path, ...]
    changed_test_files: tuple[Path, ...]
    changed_packages: tuple[PythonPackage, ...]
    changed_modules: tuple[PythonModule, ...]
    impact: ChangeImpact


@dataclass(frozen=True, slots=True)
class RepositoryChangeAnalyzer:
    intelligence: RepositoryIntelligence
    query: RepositoryQuery
    qa: RepositoryQA

    def analyze_files(
        self,
        paths: tuple[str | Path, ...],
    ) -> ChangeSet:
        changed_files = self._normalize_paths(paths)
        changed_python_files = tuple(
            path for path in changed_files if path.suffix == ".py"
        )
        changed_test_files = tuple(
            path for path in changed_python_files if "tests" in path.parts
        )
        changed_modules = self._modules_for_paths(changed_python_files)
        changed_packages = self._packages_for_modules(changed_modules)
        affected_modules = self.affected_modules(changed_files)
        affected_tests = self.affected_tests(changed_files)
        affected_packages = self._packages_for_modules(affected_modules)
        risk_level = self.risk_level(changed_files)
        impact = ChangeImpact(
            affected_packages=affected_packages,
            affected_modules=affected_modules,
            affected_tests=affected_tests,
            qa_required=bool(changed_python_files),
            risk_level=risk_level,
        )

        return ChangeSet(
            changed_files=changed_files,
            changed_python_files=changed_python_files,
            changed_test_files=changed_test_files,
            changed_packages=changed_packages,
            changed_modules=changed_modules,
            impact=impact,
        )

    def analyze_git_status(
        self,
        lines: tuple[str, ...],
    ) -> ChangeSet:
        return self.analyze_files(
            tuple(
                path
                for path in (
                    self._path_from_status_line(line)
                    for line in lines
                )
                if path is not None
            )
        )

    def affected_tests(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[RepositoryTestFile, ...]:
        modules = self.affected_modules(paths)
        tests: list[RepositoryTestFile] = []

        for module in modules:
            tests.extend(self.query.tests_for_module(module.name).items)

        direct_test_paths = set(
            path
            for path in self._normalize_paths(paths)
            if "tests" in path.parts and path.suffix == ".py"
        )
        tests.extend(
            test
            for test in self.intelligence.inventory.test_files
            if test.path in direct_test_paths
        )

        return self._sort_tests(tuple(tests))

    def affected_modules(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[PythonModule, ...]:
        python_paths = tuple(
            path
            for path in self._normalize_paths(paths)
            if path.suffix == ".py"
        )

        return self._modules_for_paths(python_paths)

    def risk_level(
        self,
        paths: tuple[str | Path, ...],
    ) -> str:
        normalized_paths = self._normalize_paths(paths)
        python_paths = tuple(
            path for path in normalized_paths if path.suffix == ".py"
        )

        if len(python_paths) >= 2:
            return "high"

        if python_paths:
            return "medium"

        return "low"

    def _modules_for_paths(
        self,
        paths: tuple[Path, ...],
    ) -> tuple[PythonModule, ...]:
        changed_path_set = set(paths)

        return tuple(
            module
            for module in self.intelligence.modules()
            if module.path in changed_path_set
        )

    def _packages_for_modules(
        self,
        modules: tuple[PythonModule, ...],
    ) -> tuple[PythonPackage, ...]:
        package_names = {
            module.package for module in modules if module.package
        }
        packages = tuple(
            package
            for package in self.intelligence.packages()
            if package.name in package_names
        )

        return self._sort_packages(packages)

    def _normalize_paths(
        self,
        paths: tuple[str | Path, ...],
    ) -> tuple[Path, ...]:
        normalized = {
            self._normalize_path(path) for path in paths
        }

        return tuple(
            sorted(
                normalized,
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

    def _path_from_status_line(
        self,
        line: str,
    ) -> str | None:
        stripped_line = line.strip()

        if not stripped_line:
            return None

        if " -> " in stripped_line:
            return stripped_line.rsplit(" -> ", 1)[-1]

        parts = stripped_line.split(maxsplit=1)

        if not parts:
            return None

        if len(parts) == 1:
            return parts[0]

        return parts[1]

    def _sort_packages(
        self,
        packages: tuple[PythonPackage, ...],
    ) -> tuple[PythonPackage, ...]:
        return tuple(
            sorted(
                packages,
                key=lambda package: package.name,
            )
        )

    def _sort_tests(
        self,
        tests: tuple[RepositoryTestFile, ...],
    ) -> tuple[RepositoryTestFile, ...]:
        unique_tests = {
            test.path: test for test in tests
        }

        return tuple(
            unique_tests[path]
            for path in sorted(
                unique_tests,
                key=lambda item: item.as_posix(),
            )
        )
