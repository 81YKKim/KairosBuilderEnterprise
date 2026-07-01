from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DesktopGeneratorResult:
    project_name: str
    project_path: Path

    generated_pages: tuple[Path, ...] = field(default_factory=tuple)
    generated_widgets: tuple[Path, ...] = field(default_factory=tuple)
    generated_viewmodels: tuple[Path, ...] = field(default_factory=tuple)
    generated_services: tuple[Path, ...] = field(default_factory=tuple)
    generated_adapters: tuple[Path, ...] = field(default_factory=tuple)

    generated_files: tuple[Path, ...] = field(default_factory=tuple)

    @property
    def generated_count(self) -> int:
        return len(self.generated_files)

    @property
    def page_count(self) -> int:
        return len(self.generated_pages)

    @property
    def widget_count(self) -> int:
        return len(self.generated_widgets)

    @property
    def viewmodel_count(self) -> int:
        return len(self.generated_viewmodels)

    @property
    def service_count(self) -> int:
        return len(self.generated_services)

    @property
    def adapter_count(self) -> int:
        return len(self.generated_adapters)