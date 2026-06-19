import json
from pathlib import Path
from builder.domain.manifest import Manifest


class JsonManifestLoader:
    def load(self, path: str | Path) -> Manifest:
        manifest_path = Path(path)
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        return Manifest(
            schema=data["schema"],
            builder_minimum_version=data["builder"]["minimum_version"],
            project_name=data["project"]["name"],
            project_version=data["project"]["version"],
            language=data["project"]["language"],
            architecture=data["project"]["architecture"],
        )
