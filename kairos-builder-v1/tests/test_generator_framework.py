from pathlib import Path

from builder.generator.base_generator import BaseGenerator
from builder.generator.composite_generator import CompositeGenerator
from builder.generator.file_generator import FileGenerator


def test_base_generator_writes_file(tmp_path: Path):
    generator = BaseGenerator()

    path = generator.write_file(tmp_path / "sample" / "file.txt", "hello")

    assert path.exists()
    assert path.read_text(encoding="utf-8") == "hello"


def test_base_generator_converts_class_name():
    generator = BaseGenerator()

    assert generator.to_class_name("kairos-desktop") == "KairosDesktop"
    assert generator.to_class_name("market_service") == "MarketService"


def test_file_generator_generates_file(tmp_path: Path):
    template = tmp_path / "template.tpl"
    template.write_text("class {{class_name}}:\n    pass\n", encoding="utf-8")

    output = tmp_path / "out" / "sample.py"

    result = FileGenerator().generate_file(
        str(template),
        output,
        {"class_name": "Sample"},
    )

    assert result.exists()
    assert "class Sample" in result.read_text(encoding="utf-8")


def test_composite_generator_creates_project_root_and_folders(tmp_path: Path):
    generator = CompositeGenerator()

    root = generator.create_project_root(tmp_path, "KairosDesktop")
    folders = generator.create_folders(
        [
            root / "src",
            root / "tests",
            root / "docs",
        ]
    )

    assert root.exists()
    assert len(folders) == 3
    assert (root / "src").exists()
    assert (root / "tests").exists()
    assert (root / "docs").exists()
