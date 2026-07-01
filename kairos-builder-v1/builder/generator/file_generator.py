from pathlib import Path

from builder.generator.base_generator import BaseGenerator


class FileGenerator(BaseGenerator):
    category = "file"

    def generate_file(
        self,
        template_path: str,
        output_path: str | Path,
        context: dict,
    ) -> Path:
        content = self.render_template(template_path, context)
        return self.write_file(output_path, content)
