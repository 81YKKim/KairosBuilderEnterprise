from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_recommendation_table_contains_priority_rendering(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    widget_source = (
        desktop_root
        / "widgets"
        / "recommendation_table.py"
    ).read_text(encoding="utf-8")

    assert "SIGNAL_COLORS" in widget_source
    assert "STATUS_COLORS" in widget_source
    assert "_apply_top_rank_style" in widget_source
    assert "_apply_signal_style" in widget_source
    assert "_apply_status_style" in widget_source
    assert "sorted(" in widget_source
    assert "rank == 1" in widget_source


def test_generated_theme_contains_recommendation_table_style(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    theme_source = (
        desktop_root
        / "theme.py"
    ).read_text(encoding="utf-8")

    assert "recommendationTableGrid" in theme_source
    assert "QHeaderView::section" in theme_source
    assert "selection-background-color" in theme_source