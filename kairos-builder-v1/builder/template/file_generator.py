from pathlib import Path

from builder.template.engine import TemplateEngine


class TemplateFileGenerator:
    def __init__(self):
        self.engine = TemplateEngine()

    def generate(self, template_path: str, output_path: str, context: dict):
        result = self.engine.render(template_path, context)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(result, encoding="utf-8")

        return str(output)
