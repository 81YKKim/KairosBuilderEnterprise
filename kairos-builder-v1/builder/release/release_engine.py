from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime


class ReleaseEngine:
    def build(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        return {
            "project": root.name,
            "status": "built",
            "version": "1.0.0"
        }

    def package(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        return {
            "project": root.name,
            "package": "release.zip",
            "status": "packaged"
        }

    def release(self, project_path: str | Path) -> dict:
        root = Path(project_path)

        data = {
            "project": root.name,
            "version": "1.0.0",
            "state": "RELEASED",
            "released_at": datetime.utcnow().isoformat()
        }

        (root / "release.json").write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return data