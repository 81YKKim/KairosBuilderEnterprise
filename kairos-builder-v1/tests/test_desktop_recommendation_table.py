from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_contains_recommendation_table_chain(
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

    dashboard_source = (
        desktop_root
        / "pages"
        / "dashboard.py"
    ).read_text(encoding="utf-8")

    viewmodel_source = (
        desktop_root
        / "viewmodels"
        / "dashboard_view_model.py"
    ).read_text(encoding="utf-8")

    service_source = (
        desktop_root
        / "services"
        / "market_service.py"
    ).read_text(encoding="utf-8")

    adapter_source = (
        desktop_root
        / "adapters"
        / "replay_adapter.py"
    ).read_text(encoding="utf-8")

    assert "class RecommendationTable(QWidget)" in widget_source
    assert "QTableWidget" in widget_source
    assert "def set_recommendations" in widget_source

    assert "RecommendationTable" in dashboard_source
    assert "_refresh_recommendations" in dashboard_source

    assert "recommendations_changed = Signal()" in viewmodel_source
    assert "get_recommendations()" in viewmodel_source

    assert "def get_recommendations" in service_source
    assert '"recommendations"' in adapter_source