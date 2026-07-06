import json
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_desktop_generator_preserves_existing_manifest_created_at(
    tmp_path: Path,
):
    generator = DesktopGenerator()

    first = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    manifest_path = (
        first.project_path
        / "desktop.manifest.json"
    )

    first_manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    original_created_at = first_manifest["created_at"]

    first_manifest["created_at"] = (
        "2026-07-01T00:00:00+00:00"
    )

    manifest_path.write_text(
        json.dumps(
            first_manifest,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    regenerated_manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    assert original_created_at
    assert (
        regenerated_manifest["created_at"]
        == "2026-07-01T00:00:00+00:00"
    )


def test_desktop_generator_preserves_existing_manifest_metadata(
    tmp_path: Path,
):
    generator = DesktopGenerator()

    first = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    manifest_path = (
        first.project_path
        / "desktop.manifest.json"
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    manifest["custom_metadata"] = {
        "owner": "enterprise-user",
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    regenerated_manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    assert regenerated_manifest["custom_metadata"] == {
        "owner": "enterprise-user",
    }
