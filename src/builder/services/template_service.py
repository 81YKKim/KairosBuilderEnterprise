from pathlib import Path

from builder.domain.template_file import TemplateFile


class TemplateService:
    def write(self, template: TemplateFile) -> None:
        path = Path(template.path)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            template.content,
            encoding="utf-8",
        )

    def exists(self, path: str) -> bool:
        return Path(path).exists()
