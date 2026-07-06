from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_desktop_generator_preserves_existing_user_modified_source(
    tmp_path: Path,
):
    generator = DesktopGenerator()

    first = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    dashboard_path = (
        first.project_path
        / "src"
        / "desktop"
        / "pages"
        / "dashboard.py"
    )

    original_source = dashboard_path.read_text(
        encoding="utf-8",
    )
    user_marker = "\n# USER CUSTOM SOURCE\n"

    dashboard_path.write_text(
        original_source + user_marker,
        encoding="utf-8",
    )

    generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    regenerated_source = dashboard_path.read_text(
        encoding="utf-8",
    )

    assert user_marker in regenerated_source


def test_desktop_generator_preserves_existing_foundation_source(
    tmp_path: Path,
):
    generator = DesktopGenerator()

    first = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    main_window_path = (
        first.project_path
        / "src"
        / "desktop"
        / "main_window.py"
    )

    original_source = main_window_path.read_text(
        encoding="utf-8",
    )
    user_marker = "\n# USER CUSTOM MAIN WINDOW\n"

    main_window_path.write_text(
        original_source + user_marker,
        encoding="utf-8",
    )

    generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    regenerated_source = main_window_path.read_text(
        encoding="utf-8",
    )

    assert user_marker in regenerated_source
