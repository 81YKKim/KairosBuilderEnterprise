from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator
from builder.generator.registry import default_registry


def test_desktop_generator_creates_enterprise_desktop_foundation(tmp_path: Path):
    result = DesktopGenerator().generate("KairosDesktop", str(tmp_path))

    assert result.project_name == "KairosDesktop"
    assert result.generated_count == 5

    assert result.page_count == 1
    assert result.widget_count == 1
    assert result.viewmodel_count == 1
    assert result.service_count == 1
    assert result.adapter_count == 1

    assert (result.project_path / "src" / "desktop" / "pages" / "dashboard.py").exists()
    assert (result.project_path / "src" / "desktop" / "widgets" / "recommendation_table.py").exists()
    assert (result.project_path / "src" / "desktop" / "viewmodels" / "dashboard_view_model.py").exists()
    assert (result.project_path / "src" / "desktop" / "services" / "market_service.py").exists()
    assert (result.project_path / "src" / "desktop" / "adapters" / "replay_adapter.py").exists()


def test_default_registry_supports_desktop_generator():
    registry = default_registry()

    assert "desktop" in registry.names()
    assert isinstance(registry.create("desktop"), DesktopGenerator)
