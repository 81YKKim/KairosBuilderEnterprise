from pathlib import Path

from builder.template.engine import TemplateEngine


class UnitTestGenerator:
    def __init__(self):
        self.engine = TemplateEngine()

    def generate(self, name: str, output_root: str = "output/tests") -> Path:
        output = Path(output_root)
        output.mkdir(parents=True, exist_ok=True)

        output_file = output / f"test_{name}.py"

        text = self.engine.render(
            "templates/test.tpl",
            {
                "entity_name": name,
            },
        )

        output_file.write_text(text, encoding="utf-8")

        return output_file
