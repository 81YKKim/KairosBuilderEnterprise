from __future__ import annotations

import json
from pathlib import Path

from builder.manifest.desktop_manifest import DesktopManifest


class DesktopManifestWriter:
    def write(
        self,
        manifest: DesktopManifest,
        output_directory: str | Path,
    ) -> Path:
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)

        manifest_path = output_directory / "desktop.manifest.json"

        if manifest_path.exists():
            return manifest_path

        manifest_path.write_text(
            json.dumps(
                manifest.to_dict(),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return manifest_path