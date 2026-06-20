import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from builder.template.file_generator import TemplateFileGenerator


def test_file_generator():
    generator = TemplateFileGenerator()

    output = generator.generate(
        "templates/domain.tpl",
        "output/generated_user.py",
        {
            "class_name": "User",
            "entity_name": "user",
        },
    )

    text = Path(output).read_text(encoding="utf-8")

    assert "class User" in text
    assert 'self.name = "user"' in text
