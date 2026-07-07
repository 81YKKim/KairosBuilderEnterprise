from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryDocumentation,
    RepositoryModel,
    RepositoryStatistics,
    RepositoryTestFile,
)


@dataclass(frozen=True, slots=True)
class RepositoryScanResult:
    repository_root: Path
    files: tuple[Path, ...]
    directories: tuple[Path, ...]
    python_files: tuple[Path, ...]
    model: RepositoryModel


class RepositoryScanner:
    DEFAULT_IGNORED_DIRECTORIES = frozenset(
        {
            ".git",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "__pycache__",
        }
    )

    DOCUMENTATION_SUFFIXES = frozenset(
        {
            ".md",
            ".rst",
            ".txt",
        }
    )

    def __init__(
        self,
        ignored_directories: frozenset[str] | None = None,
    ) -> None:
        self.ignored_directories = (
            ignored_directories or self.DEFAULT_IGNORED_DIRECTORIES
        )

    def scan(
        self,
        repository_root: str | Path,
        git_root: str | Path | None = None,
        branch: str = "Unknown",
        head_commit: str = "Unknown",
    ) -> RepositoryScanResult:
        root = Path(repository_root)
        resolved_git_root = Path(git_root) if git_root is not None else root

        directories = self._collect_directories(root)
        files = self._collect_files(root)
        python_files = tuple(
            path for path in files if path.suffix == ".py"
        )
        packages = self._build_packages(python_files)
        modules = self._build_modules(python_files)
        tests = self._build_tests(python_files)
        documentation = self._build_documentation(files)

        model = RepositoryModel(
            repository_root=root,
            git_root=resolved_git_root,
            branch=branch,
            head_commit=head_commit,
            python_modules=modules,
            packages=packages,
            tests=tests,
            documentation=documentation,
            statistics=RepositoryStatistics(
                directory_count=len(directories),
                file_count=len(files),
                python_file_count=len(python_files),
                test_file_count=len(tests),
                documentation_file_count=len(documentation),
                package_count=len(packages),
                module_count=len(modules),
            ),
        )

        return RepositoryScanResult(
            repository_root=root,
            files=files,
            directories=directories,
            python_files=python_files,
            model=model,
        )

    def _collect_directories(
        self,
        root: Path,
    ) -> tuple[Path, ...]:
        directories: list[Path] = []

        for path in root.rglob("*"):
            if not path.is_dir():
                continue

            relative_path = path.relative_to(root)

            if self._is_ignored(relative_path):
                continue

            directories.append(relative_path)

        return self._sort_paths(directories)

    def _collect_files(
        self,
        root: Path,
    ) -> tuple[Path, ...]:
        files: list[Path] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            relative_path = path.relative_to(root)

            if self._is_ignored(relative_path):
                continue

            files.append(relative_path)

        return self._sort_paths(files)

    def _build_packages(
        self,
        python_files: tuple[Path, ...],
    ) -> tuple[PythonPackage, ...]:
        packages: list[PythonPackage] = []

        for path in python_files:
            if path.name != "__init__.py":
                continue

            package_path = path.parent
            packages.append(
                PythonPackage(
                    name=self._path_to_module_name(package_path),
                    path=package_path,
                )
            )

        return tuple(
            sorted(
                packages,
                key=lambda package: package.name,
            )
        )

    def _build_modules(
        self,
        python_files: tuple[Path, ...],
    ) -> tuple[PythonModule, ...]:
        modules: list[PythonModule] = []

        for path in python_files:
            if path.name == "__init__.py":
                continue

            module_name = self._path_to_module_name(
                path.with_suffix("")
            )
            package_name = (
                self._path_to_module_name(path.parent)
                if path.parent != Path(".")
                else ""
            )
            modules.append(
                PythonModule(
                    name=module_name,
                    path=path,
                    package=package_name,
                )
            )

        return tuple(
            sorted(
                modules,
                key=lambda module: module.name,
            )
        )

    def _build_tests(
        self,
        python_files: tuple[Path, ...],
    ) -> tuple[RepositoryTestFile, ...]:
        tests: list[RepositoryTestFile] = []

        for path in python_files:
            if not self._is_test_file(path):
                continue

            tests.append(
                RepositoryTestFile(
                    name=path.stem,
                    path=path,
                )
            )

        return tuple(
            sorted(
                tests,
                key=lambda test_file: test_file.path.as_posix(),
            )
        )

    def _build_documentation(
        self,
        files: tuple[Path, ...],
    ) -> tuple[RepositoryDocumentation, ...]:
        documentation: list[RepositoryDocumentation] = []

        for path in files:
            if path.suffix.lower() not in self.DOCUMENTATION_SUFFIXES:
                continue

            documentation.append(
                RepositoryDocumentation(
                    title=path.stem,
                    path=path,
                )
            )

        return tuple(
            sorted(
                documentation,
                key=lambda document: document.path.as_posix(),
            )
        )

    def _is_test_file(
        self,
        path: Path,
    ) -> bool:
        return (
            "tests" in path.parts
            and path.name.startswith("test_")
            and path.suffix == ".py"
        )

    def _is_ignored(
        self,
        relative_path: Path,
    ) -> bool:
        return any(
            part in self.ignored_directories or part.startswith(".")
            for part in relative_path.parts
        )

    def _path_to_module_name(
        self,
        path: Path,
    ) -> str:
        parts = path.parts

        if parts and parts[0] == "src":
            parts = parts[1:]

        return ".".join(parts)

    def _sort_paths(
        self,
        paths: list[Path],
    ) -> tuple[Path, ...]:
        return tuple(
            sorted(
                paths,
                key=lambda path: path.as_posix(),
            )
        )
