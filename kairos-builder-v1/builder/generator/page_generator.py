from pathlib import Path

from builder.generator.file_generator import FileGenerator


class PageGenerator(FileGenerator):
    category = "file"

    def generate(self, name: str, output_root: str = "output/page") -> Path:
        class_name = self.to_class_name(name)
        file_name = self.to_snake_name(name)

        return self.generate_file(
            "templates/page.tpl",
            Path(output_root) / f"{file_name}.py",
            {
                "class_name": class_name,
                "page_name": name,
            },
        )
