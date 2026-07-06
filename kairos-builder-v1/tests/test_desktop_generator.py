from pathlib import Path

import pytest

from builder.generator.desktop_generator import DesktopGenerator
from builder.generator.desktop_structure_validator import (
    DesktopStructureValidator,
)
from builder.generator.registry import default_registry


def test_desktop_generator_creates_enterprise_desktop_foundation(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    assert result.project_name == "KairosDesktop"
    assert result.generated_count == 13

    assert result.page_count == 1
    assert result.widget_count == 3
    assert result.viewmodel_count == 1
    assert result.service_count == 1
    assert result.adapter_count == 1

    desktop_root = result.project_path / "src" / "desktop"

    assert (desktop_root / "__init__.py").exists()
    assert (desktop_root / "app.py").exists()
    assert (desktop_root / "main.py").exists()
    assert (desktop_root / "main_window.py").exists()
    assert (desktop_root / "theme.py").exists()

    assert (
        desktop_root / "pages" / "dashboard.py"
    ).exists()

    assert (
        desktop_root / "widgets" / "sidebar.py"
    ).exists()

    assert (
        desktop_root
        / "widgets"
        / "recommendation_table.py"
    ).exists()

    assert (
        desktop_root
        / "widgets"
        / "recommendation_detail.py"
    ).exists()

    assert (
        desktop_root
        / "viewmodels"
        / "dashboard_view_model.py"
    ).exists()

    assert (
        desktop_root
        / "services"
        / "market_service.py"
    ).exists()

    assert (
        desktop_root
        / "adapters"
        / "replay_adapter.py"
    ).exists()

    assert (
        result.project_path
        / "tests"
        / "test_desktop_foundation.py"
    ).exists()


def test_generated_desktop_contains_service_adapter_mvvm_chain(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

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

    assert "MarketService" in viewmodel_source
    assert (
        "market_service.get_market_status()"
        in viewmodel_source
    )

    assert "ReplayAdapter" in service_source
    assert "self.adapter.load()" in service_source

    assert "class ReplayAdapter" in adapter_source
    assert "Market Service Connected" in adapter_source


def test_generated_desktop_foundation_contains_mvvm_binding(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    dashboard_source = (
        desktop_root / "pages" / "dashboard.py"
    ).read_text(encoding="utf-8")

    viewmodel_source = (
        desktop_root
        / "viewmodels"
        / "dashboard_view_model.py"
    ).read_text(encoding="utf-8")

    assert "DashboardViewModel" in dashboard_source
    assert "_bind_view_model" in dashboard_source
    assert "status_changed.connect" in dashboard_source

    assert (
        "class DashboardViewModel(QObject)"
        in viewmodel_source
    )
    assert "Property(str" in viewmodel_source
    assert "status_changed = Signal()" in viewmodel_source
    assert "def set_status" in viewmodel_source


def test_generated_desktop_foundation_contains_pyside6_bootstrap(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    app_source = (
        desktop_root / "app.py"
    ).read_text(encoding="utf-8")

    main_window_source = (
        desktop_root / "main_window.py"
    ).read_text(encoding="utf-8")

    sidebar_source = (
        desktop_root / "widgets" / "sidebar.py"
    ).read_text(encoding="utf-8")

    theme_source = (
        desktop_root / "theme.py"
    ).read_text(encoding="utf-8")

    assert "QApplication" in app_source
    assert "MainWindow" in app_source
    assert "QStackedWidget" in main_window_source
    assert "Sidebar" in main_window_source
    assert "Dashboard" in main_window_source
    assert "class Sidebar(QWidget)" in sidebar_source
    assert (
        "dashboard_requested = Signal()"
        in sidebar_source
    )
    assert "DARK_THEME" in theme_source
    assert "QWidget#sidebar" in theme_source


def test_generated_desktop_passes_structure_validation(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    validated_files = DesktopStructureValidator().validate(
        desktop_root
    )

    assert len(validated_files) == 12


def test_desktop_structure_validator_detects_missing_file(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    missing_file = (
        desktop_root
        / "services"
        / "market_service.py"
    )
    missing_file.unlink()

    with pytest.raises(
        ValueError,
        match="Missing files",
    ):
        DesktopStructureValidator().validate(desktop_root)


def test_desktop_structure_validator_detects_invalid_architecture(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    adapter_file = (
        desktop_root
        / "adapters"
        / "replay_adapter.py"
    )
    adapter_file.write_text(
        "class BrokenAdapter:\n    pass\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Missing source markers",
    ):
        DesktopStructureValidator().validate(desktop_root)


def test_default_registry_supports_desktop_generator():
    registry = default_registry()

    assert "desktop" in registry.names()

    assert isinstance(
        registry.create("desktop"),
        DesktopGenerator,
    )
