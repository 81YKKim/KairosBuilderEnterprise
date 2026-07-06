from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_contains_recommendation_detail_chain(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    table_source = (
        desktop_root
        / "widgets"
        / "recommendation_table.py"
    ).read_text(encoding="utf-8")

    detail_source = (
        desktop_root
        / "widgets"
        / "recommendation_detail.py"
    ).read_text(encoding="utf-8")

    dashboard_source = (
        desktop_root
        / "pages"
        / "dashboard.py"
    ).read_text(encoding="utf-8")

    assert "recommendation_selected = Signal(dict)" in table_source
    assert "_handle_cell_clicked" in table_source
    assert "recommendation_selected.emit" in table_source

    assert "class RecommendationDetail(QWidget)" in detail_source
    assert "def set_recommendation" in detail_source

    assert "QSplitter" in dashboard_source
    assert "RecommendationDetail" in dashboard_source
    assert "recommendation_selected.connect" in dashboard_source


def test_desktop_generator_reports_three_widgets(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    assert result.generated_count == 13
    assert result.widget_count == 3
