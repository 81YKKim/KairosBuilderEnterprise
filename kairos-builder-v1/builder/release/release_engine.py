from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import json


class ReleaseEngine:
    def build(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        return {
            "project": root.name,
            "status": "built",
            "version": "2.0.0-alpha",
        }

    def package(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        return {
            "project": root.name,
            "package": "release.zip",
            "status": "packaged",
        }

    def release(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        data = {
            "project": root.name,
            "version": "2.0.0-alpha",
            "state": "RELEASED",
            "released_at": datetime.now(UTC).isoformat(),
        }

        (root / "release.json").write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

        return data