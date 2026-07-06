import json
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator
from builder.manifest.desktop_manifest import DesktopManifest
from builder.manifest.desktop_manifest_writer import DesktopManifestWriter


def test_desktop_manifest_to_dict():
    manifest = DesktopManifest(
        project_name="KairosDesktop",
        builder_version="2.0.0-alpha",
        generator="DesktopGenerator",
        architecture="MVVM",
        created_at="2026-07-01T00:00:00+00:00",
        pages=1,
        widgets=1,
        viewmodels=1,
        services=1,
        adapters=1,
    )

    data = manifest.to_dict()

    assert data["project_name"] == "KairosDesktop"
    assert data["generator"] == "DesktopGenerator"
    assert data["architecture"] == "MVVM"
    assert data["generated"]["pages"] == 1
    assert data["generated"]["adapters"] == 1


def test_desktop_manifest_writer_creates_manifest_file(tmp_path: Path):
    manifest = DesktopManifest(
        project_name="KairosDesktop",
        builder_version="2.0.0-alpha",
        generator="DesktopGenerator",
        architecture="MVVM",
        created_at="2026-07-01T00:00:00+00:00",
        pages=1,
        widgets=1,
        viewmodels=1,
        services=1,
        adapters=1,
    )

    path = DesktopManifestWriter().write(manifest, tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    assert path.name == "desktop.manifest.json"
    assert data["project_name"] == "KairosDesktop"
    assert data["generated"]["widgets"] == 1


def test_desktop_generator_creates_manifest_file(tmp_path: Path):
    result = DesktopGenerator().generate("KairosDesktop", str(tmp_path))

    manifest_path = result.project_path / "desktop.manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest_path.exists()
    assert data["project_name"] == "KairosDesktop"
    assert data["generator"] == "DesktopGenerator"
    assert data["architecture"] == "MVVM"
    assert data["generated"]["pages"] == result.page_count
    assert data["generated"]["widgets"] == result.widget_count
    assert data["generated"]["viewmodels"] == result.viewmodel_count
    assert data["generated"]["services"] == result.service_count
    assert data["generated"]["adapters"] == result.adapter_count


def test_desktop_manifest_writer_does_not_write_utf8_bom(tmp_path: Path):
    manifest = DesktopManifest(
        project_name="KairosDesktop",
        builder_version="2.0.0-alpha",
        generator="DesktopGenerator",
        architecture="MVVM",
        created_at="2026-07-01T00:00:00+00:00",
        pages=1,
        widgets=1,
        viewmodels=1,
        services=1,
        adapters=1,
    )

    path = DesktopManifestWriter().write(manifest, tmp_path)

    assert not path.read_bytes().startswith(b"\xef\xbb\xbf")