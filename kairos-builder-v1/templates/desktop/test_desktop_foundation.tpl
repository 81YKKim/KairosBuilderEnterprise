from pathlib import Path


def test_generated_desktop_foundation_exists():
    project_root = Path(__file__).resolve().parents[1]
    desktop_root = project_root / "src" / "desktop"

    assert project_root.exists()
    assert desktop_root.exists()
    assert (desktop_root / "__init__.py").exists()
    assert (desktop_root / "app.py").exists()
    assert (desktop_root / "main.py").exists()
    assert (desktop_root / "main_window.py").exists()
    assert (desktop_root / "theme.py").exists()
    assert (desktop_root / "pages" / "dashboard.py").exists()
    assert (desktop_root / "widgets" / "sidebar.py").exists()
    assert (desktop_root / "widgets" / "recommendation_table.py").exists()
    assert (desktop_root / "widgets" / "recommendation_detail.py").exists()
    assert (desktop_root / "viewmodels" / "dashboard_view_model.py").exists()
    assert (desktop_root / "services" / "market_service.py").exists()
    assert (desktop_root / "adapters" / "replay_adapter.py").exists()
