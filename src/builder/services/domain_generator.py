from pathlib import Path

from builder.services.base_generator import BaseGenerator
from builder.services.template_loader import TemplateLoader
from builder.services.template_renderer import TemplateRenderer


class DomainGenerator(BaseGenerator):
    def __init__(
        self,
        template_loader: TemplateLoader | None = None,
        template_renderer: TemplateRenderer | None = None,
    ) -> None:
        self.template_loader = template_loader or TemplateLoader()
        self.template_renderer = template_renderer or TemplateRenderer()

    def generate(self, name: str, output_root: str = "src/builder/domain") -> Path:
        file_name = self._to_file_name(name)
        output_path = Path(output_root) / file_name

        if output_path.exists():
            return output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        template = self.template_loader.load(
            language="python",
            profile="standard",
            template="domain.tpl",
        )

        content = self.template_renderer.render(
            template,
            {
                "name": name,
                "name_lower": name.lower(),
            },
        )

        output_path.write_text(content, encoding="utf-8")
        return output_path

    def _to_file_name(self, name: str) -> str:
        result = ""

        for index, char in enumerate(name):
            if char.isupper() and index > 0:
                result += "_"

            result += char.lower()

        return f"{result}.py"
