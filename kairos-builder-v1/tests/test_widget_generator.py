from pathlib import Path

from builder.generator.widget_generator import WidgetGenerator


def test_widget_generator_creates_widget_file(tmp_path: Path):
    result = WidgetGenerator().generate("RecommendationTable", str(tmp_path))

    assert result.exists()
    assert result.name == "recommendation_table.py"
    assert "class RecommendationTable" in result.read_text(encoding="utf-8")
