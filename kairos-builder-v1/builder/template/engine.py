from builder.template.loader import TemplateLoader
from builder.template.renderer import TemplateRenderer


class TemplateEngine:
    def __init__(self):
        self.loader = TemplateLoader()
        self.renderer = TemplateRenderer()

    def render(self, template_path: str, context: dict) -> str:
        template = self.loader.load(template_path)
        return self.renderer.render(template, context)
