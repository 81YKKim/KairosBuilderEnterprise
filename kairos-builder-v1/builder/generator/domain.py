from pathlib import Path
from builder.context.context import Context
from builder.template.renderer import TemplateRenderer

class DomainGenerator:

    def generate(self, name):

        ctx = Context().build(name)

        template = """
class {{class_name}}:
    def __init__(self):
        self.name = "{{name}}"
"""

        content = TemplateRenderer().render(template, ctx)

        path = Path("output/domain")
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / f"{name.lower()}_domain.py"
        file_path.write_text(content)

        return f"generated: {file_path}"