from pathlib import Path
import json
import shutil


class PackageBuilder:
    def build_package(self, project_path: str | Path) -> Path:
        root = Path(project_path)
        dist = root / "dist"

        dist.mkdir(exist_ok=True)

        package_info = {
            "name": root.name,
            "version": "2.0.0-alpha",
            "type": "builder-cli-package",
        }

        (dist / "package.json").write_text(
            json.dumps(package_info, indent=4),
            encoding="utf-8",
        )

        return dist

    def create_bundle(self, project_path: str | Path) -> Path:
        root = Path(project_path)
        bundle_path = root / "builder_bundle.zip"

        shutil.make_archive(
            str(bundle_path).replace(".zip", ""),
            "zip",
            root_dir=root,
        )

        return Path(bundle_path)