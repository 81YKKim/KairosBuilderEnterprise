from pathlib import Path

from builder.services.base_generator import BaseGenerator
from builder.services.template_loader import TemplateLoader
from builder.services.template_renderer import TemplateRenderer


class TestGenerator(BaseGenerator):
    __test__ = False

    def __init__(
        self,
        template_loader: TemplateLoader | None = None,
        template_renderer: TemplateRenderer | None = None,
    ) -> None:
        self.template_loader = template_loader or TemplateLoader()
        self.template_renderer = template_renderer or TemplateRenderer()

    def generate(self, name: str, output_root: str = "tests") -> Path:
        file_name = f"test_{self._to_file_name(name)}"
        output_path = Path(output_root) / file_name

        if output_path.exists():
            return output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.build_content(name), encoding="utf-8")

        return output_path

    def build_content(self, name: str) -> str:
        template = self.template_loader.load(
            language="python",
            profile="standard",
            template="test.tpl",
        )

        return self.template_renderer.render(
            template,
            {
                "name": name,
                "name_lower": name.lower(),
            },
        )

    def _to_file_name(self, name: str) -> str:
        result = ""

        for index, char in enumerate(name):
            if char.isupper() and index > 0:
                result += "_"

            result += char.lower()

        return f"{result}.py"
