from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".venv",
    "venv",
}


@dataclass(frozen=True, slots=True)
class CurrentState:
    repository_path: Path
    analyzed_at: str
    repository_health: Mapping[str, str]
    architecture_health: Mapping[str, str]
    testing_health: Mapping[str, str]
    release_health: Mapping[str, str]
    implemented_features: tuple[str, ...]
    implemented_modules: tuple[str, ...]
    implemented_tests: tuple[str, ...]
    implemented_packages: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "repository_path",
            Path(self.repository_path),
        )
        object.__setattr__(
            self,
            "repository_health",
            MappingProxyType(dict(self.repository_health)),
        )
        object.__setattr__(
            self,
            "architecture_health",
            MappingProxyType(dict(self.architecture_health)),
        )
        object.__setattr__(
            self,
            "testing_health",
            MappingProxyType(dict(self.testing_health)),
        )
        object.__setattr__(
            self,
            "release_health",
            MappingProxyType(dict(self.release_health)),
        )
        object.__setattr__(
            self,
            "implemented_features",
            tuple(sorted(self.implemented_features)),
        )
        object.__setattr__(
            self,
            "implemented_modules",
            tuple(sorted(self.implemented_modules)),
        )
        object.__setattr__(
            self,
            "implemented_tests",
            tuple(sorted(self.implemented_tests)),
        )
        object.__setattr__(
            self,
            "implemented_packages",
            tuple(sorted(self.implemented_packages)),
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(slots=True)
class CurrentBuilder:
    current_state: CurrentState | None = None

    def build(
        self,
        repository_path: str | Path,
    ) -> CurrentState:
        root = Path(repository_path)
        inventory = _CurrentInventory.from_repository(root)
        state = CurrentState(
            repository_path=root,
            analyzed_at=_analyzed_at(),
            repository_health={
                "exists": _bool_text(root.exists()),
                "python_module_count": str(len(inventory.modules)),
                "package_count": str(len(inventory.packages)),
                "file_count": str(len(inventory.files)),
            },
            architecture_health={
                "status": "available" if root.exists() else "missing",
                "package_count": str(len(inventory.packages)),
            },
            testing_health={
                "status": "available" if inventory.tests else "missing",
                "test_count": str(len(inventory.tests)),
            },
            release_health={
                "status": "unknown",
            },
            implemented_features=(),
            implemented_modules=inventory.modules,
            implemented_tests=inventory.tests,
            implemented_packages=inventory.packages,
            metadata={
                "engine": "ultimate-current",
                "scope": "foundation",
            },
        )
        self.current_state = state

        return state

    def load(
        self,
        state: CurrentState,
    ) -> CurrentBuilder:
        self.current_state = state

        return self

    def summary(self) -> dict[str, Mapping[str, str]]:
        if self.current_state is None:
            raise ValueError("Current state is not loaded.")

        state = self.current_state

        return {
            "Repository": {
                "path": str(state.repository_path),
                **state.repository_health,
            },
            "Architecture": dict(state.architecture_health),
            "Tests": dict(state.testing_health),
            "Modules": {
                "count": str(len(state.implemented_modules)),
                "items": ",".join(state.implemented_modules),
            },
            "Packages": {
                "count": str(len(state.implemented_packages)),
                "items": ",".join(state.implemented_packages),
            },
            "Release": dict(state.release_health),
        }


@dataclass(frozen=True, slots=True)
class _CurrentInventory:
    files: tuple[Path, ...]
    modules: tuple[str, ...]
    packages: tuple[str, ...]
    tests: tuple[str, ...]

    @classmethod
    def from_repository(
        cls,
        root: Path,
    ) -> _CurrentInventory:
        if not root.exists() or not root.is_dir():
            return cls(
                files=(),
                modules=(),
                packages=(),
                tests=(),
            )

        files = _python_files(root)

        return cls(
            files=files,
            modules=tuple(
                sorted(
                    _module_name(path)
                    for path in files
                    if path.name != "__init__.py"
                    and not _is_test_file(path)
                )
            ),
            packages=tuple(
                sorted(
                    _package_name(path.parent)
                    for path in files
                    if path.name == "__init__.py"
                )
            ),
            tests=tuple(
                sorted(
                    path.as_posix()
                    for path in files
                    if _is_test_file(path)
                )
            ),
        )


def _python_files(
    root: Path,
) -> tuple[Path, ...]:
    paths: list[Path] = []

    for path in root.rglob("*.py"):
        relative_path = path.relative_to(root)

        if _is_ignored(relative_path):
            continue

        paths.append(relative_path)

    return tuple(
        sorted(
            paths,
            key=lambda item: item.as_posix(),
        )
    )


def _is_ignored(
    path: Path,
) -> bool:
    return any(
        part in IGNORED_DIRECTORIES or part.startswith(".")
        for part in path.parts
    )


def _is_test_file(
    path: Path,
) -> bool:
    return (
        "tests" in path.parts
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
    )


def _module_name(
    path: Path,
) -> str:
    parts = _source_parts(path.with_suffix(""))

    return ".".join(parts)


def _package_name(
    path: Path,
) -> str:
    parts = _source_parts(path)

    return ".".join(parts)


def _source_parts(
    path: Path,
) -> tuple[str, ...]:
    parts = path.parts

    if parts and parts[0] == "src":
        return tuple(parts[1:])

    return tuple(parts)


def _analyzed_at() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _bool_text(
    value: bool,
) -> str:
    return "true" if value else "false"
