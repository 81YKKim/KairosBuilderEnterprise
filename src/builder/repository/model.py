from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PythonModule:
    name: str
    path: Path
    package: str


@dataclass(frozen=True, slots=True)
class PythonPackage:
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class RepositoryTestFile:
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class RepositoryDocumentation:
    title: str
    path: Path


@dataclass(frozen=True, slots=True)
class RepositoryStatistics:
    directory_count: int
    file_count: int
    python_file_count: int
    test_file_count: int
    documentation_file_count: int
    package_count: int
    module_count: int


@dataclass(frozen=True, slots=True)
class RepositoryModel:
    repository_root: Path
    git_root: Path
    branch: str
    head_commit: str
    python_modules: tuple[PythonModule, ...]
    packages: tuple[PythonPackage, ...]
    tests: tuple[RepositoryTestFile, ...]
    documentation: tuple[RepositoryDocumentation, ...]
    statistics: RepositoryStatistics
