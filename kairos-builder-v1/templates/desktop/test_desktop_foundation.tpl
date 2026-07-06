from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_foundation_exists(tmp_path: Path):
    result = DesktopGenerator().generate("{{project_name}}", str(tmp_path))

    assert result.generated_count == 12
    assert result.project_path.exists()
    assert (result.project_path / "src" / "desktop" / "app.py").exists()
    assert (result.project_path / "src" / "desktop" / "main_window.py").exists()
    assert (result.project_path / "src" / "desktop" / "theme.py").exists()