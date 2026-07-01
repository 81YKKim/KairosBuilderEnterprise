from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DesktopManifest:
    project_name: str
    builder_version: str
    generator: str
    architecture: str
    created_at: str

    pages: int
    widgets: int
    viewmodels: int
    services: int
    adapters: int

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "builder_version": self.builder_version,
            "generator": self.generator,
            "architecture": self.architecture,
            "created_at": self.created_at,
            "generated": {
                "pages": self.pages,
                "widgets": self.widgets,
                "viewmodels": self.viewmodels,
                "services": self.services,
                "adapters": self.adapters,
            },
        }
