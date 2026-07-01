from pathlib import Path

class TemplateEngine:
    def __init__(self, registry, validator):
        self.registry = registry
        self.validator = validator

    def render(self, name: str, version: str, output_root: str):
        template = self.registry.get(name, version)

        if not template:
            raise ValueError("Template not found")

        if not self.validator.validate(template):
            raise ValueError("Invalid template schema")

        base = Path(output_root) / name

        for folder in template["structure"]:
            (base / folder).mkdir(parents=True, exist_ok=True)

        for file in template["files"]:
            (base / file).write_text(f"# {name}")

        return base