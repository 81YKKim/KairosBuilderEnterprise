from builder.services.base_generator import BaseGenerator
from builder.services.template_renderer import TemplateRenderer


class DomainGenerator(BaseGenerator):
    def __init__(self, renderer: TemplateRenderer | None = None) -> None:
        self.renderer = renderer or TemplateRenderer()

    def build_content(self, name: str) -> str:
        template = """from dataclasses import dataclass


@dataclass
class {{ name }}:
    name: str
"""
        return self.renderer.render(
            template,
            {"name": name},
        )
