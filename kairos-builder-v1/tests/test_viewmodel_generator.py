from pathlib import Path

from builder.generator.viewmodel_generator import ViewModelGenerator


def test_viewmodel_generator_creates_viewmodel_file(tmp_path: Path):
    result = ViewModelGenerator().generate("DashboardViewModel", str(tmp_path))

    assert result.exists()
    assert result.name == "dashboard_view_model.py"
    assert "class DashboardViewModel" in result.read_text(encoding="utf-8")
