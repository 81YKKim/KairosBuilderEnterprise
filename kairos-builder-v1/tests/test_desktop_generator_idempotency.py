from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_desktop_generator_is_idempotent(tmp_path: Path):
    generator = DesktopGenerator()

    first = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )
    second = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    assert first.project_path == second.project_path
    assert first.generated_count == second.generated_count == 13
    assert first.page_count == second.page_count == 1
    assert first.widget_count == second.widget_count == 3
    assert first.viewmodel_count == second.viewmodel_count == 1
    assert first.service_count == second.service_count == 1
    assert first.adapter_count == second.adapter_count == 1


def test_desktop_generator_idempotency_preserves_required_files(
    tmp_path: Path,
):
    generator = DesktopGenerator()

    generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )
    result = generator.generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    required_files = (
        desktop_root / "__init__.py",
        desktop_root / "app.py",
        desktop_root / "main.py",
        desktop_root / "main_window.py",
        desktop_root / "theme.py",
        desktop_root / "pages" / "dashboard.py",
        desktop_root / "widgets" / "sidebar.py",
        desktop_root / "widgets" / "recommendation_table.py",
        desktop_root / "widgets" / "recommendation_detail.py",
        desktop_root / "viewmodels" / "dashboard_view_model.py",
        desktop_root / "services" / "market_service.py",
        desktop_root / "adapters" / "replay_adapter.py",
        result.project_path / "tests" / "test_desktop_foundation.py",
        result.project_path / "desktop.manifest.json",
    )

    assert all(path.exists() for path in required_files)
    assert all(path.is_file() for path in required_files)
