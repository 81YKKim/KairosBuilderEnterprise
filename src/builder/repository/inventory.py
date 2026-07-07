from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryTestFile,
)
from builder.repository.scanner import RepositoryScanner


@dataclass(frozen=True, slots=True)
class RepositoryInventory:
    repository_root: Path
    files: tuple[Path, ...]
    python_files: tuple[Path, ...]
    packages: tuple[PythonPackage, ...]
    modules: tuple[PythonModule, ...]
    test_files: tuple[RepositoryTestFile, ...]
    resource_files: tuple[Path, ...]
    package_count: int
    module_count: int
    python_file_count: int
    test_count: int
    resource_count: int
    total_file_count: int

    @property
    def summary(self) -> dict[str, int]:
        return {
            "package_count": self.package_count,
            "module_count": self.module_count,
            "python_file_count": self.python_file_count,
            "test_count": self.test_count,
            "resource_count": self.resource_count,
            "total_file_count": self.total_file_count,
        }


class RepositoryInventoryBuilder:
    def __init__(
        self,
        scanner: RepositoryScanner | None = None,
    ) -> None:
        self.scanner = scanner or RepositoryScanner()

    def build(
        self,
        repository_root: str | Path,
        git_root: str | Path | None = None,
        branch: str = "Unknown",
        head_commit: str = "Unknown",
    ) -> RepositoryInventory:
        scan_result = self.scanner.scan(
            repository_root,
            git_root=git_root,
            branch=branch,
            head_commit=head_commit,
        )
        model = scan_result.model
        resource_files = tuple(
            path for path in scan_result.files if path.suffix != ".py"
        )

        return RepositoryInventory(
            repository_root=scan_result.repository_root,
            files=scan_result.files,
            python_files=scan_result.python_files,
            packages=model.packages,
            modules=model.python_modules,
            test_files=model.tests,
            resource_files=resource_files,
            package_count=len(model.packages),
            module_count=len(model.python_modules),
            python_file_count=len(scan_result.python_files),
            test_count=len(model.tests),
            resource_count=len(resource_files),
            total_file_count=len(scan_result.files),
        )
