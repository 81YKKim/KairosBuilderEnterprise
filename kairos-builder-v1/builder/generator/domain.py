from pathlib import Path

from builder.template.engine import TemplateEngine


class DomainGenerator:
    def __init__(self):
        self.engine = TemplateEngine()

    def generate(self, name: str):
        class_name = name.capitalize()

        output = Path("output/domain")
        output.mkdir(parents=True, exist_ok=True)

        output_file = output / f"{name}_domain.py"

        text = self.engine.render(
            "templates/domain.tpl",
            {
                "class_name": class_name,
                "entity_name": name,
            },
        )

        output_file.write_text(text, encoding="utf-8")

        return f"generated: {output_file}"
