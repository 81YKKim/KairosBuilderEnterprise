from pathlib import Path

from builder.generator.page_generator import PageGenerator


def test_page_generator_creates_page_file(tmp_path: Path):
    result = PageGenerator().generate("Dashboard", str(tmp_path))

    assert result.exists()
    assert result.name == "dashboard.py"
    assert "class Dashboard" in result.read_text(encoding="utf-8")
