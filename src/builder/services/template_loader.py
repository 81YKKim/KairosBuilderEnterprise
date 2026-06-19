from pathlib import Path


class TemplateLoader:
    def __init__(self, template_root: str = "templates") -> None:
        self.template_root = Path(template_root)

    def load(self, language: str, profile: str, template: str) -> str:
        template_path = self.template_root / language / profile / template

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        return template_path.read_text(encoding="utf-8")
