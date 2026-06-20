from pathlib import Path

from builder.template.engine import TemplateEngine


class ServiceGenerator:
    def __init__(self):
        self.engine = TemplateEngine()

    def generate(self, name: str):
        class_name = name.capitalize()

        output = Path("output/service")
        output.mkdir(parents=True, exist_ok=True)

        output_file = output / f"{name}_service.py"

        text = self.engine.render(
            "templates/service.tpl",
            {
                "class_name": class_name,
            },
        )

        output_file.write_text(text, encoding="utf-8")

        return f"generated: {output_file}"
