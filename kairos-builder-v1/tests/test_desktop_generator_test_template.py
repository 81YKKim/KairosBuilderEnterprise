from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_desktop_generator_creates_foundation_test_file(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    test_path = (
        result.project_path
        / "tests"
        / "test_desktop_foundation.py"
    )

    assert test_path.exists()
    assert test_path.is_file()

    source = test_path.read_text(encoding="utf-8")

    assert "DesktopGenerator" in source
    assert "generated_count == 13" in source
