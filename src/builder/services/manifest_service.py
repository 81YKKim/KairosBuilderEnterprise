from pathlib import Path
from builder.domain.manifest import Manifest
from builder.infrastructure.json.json_manifest_loader import JsonManifestLoader


class ManifestService:
    def __init__(self, loader: JsonManifestLoader | None = None) -> None:
        self.loader = loader or JsonManifestLoader()

    def load_manifest(self, path: str | Path = "builder.manifest.json") -> Manifest:
        return self.loader.load(path)
