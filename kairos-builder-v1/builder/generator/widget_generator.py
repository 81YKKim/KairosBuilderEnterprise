from pathlib import Path

from builder.generator.file_generator import FileGenerator


class WidgetGenerator(FileGenerator):
    category = "file"

    def generate(self, name: str, output_root: str = "output/widget") -> Path:
        class_name = self.to_class_name(name)
        file_name = self.to_snake_name(name)

        return self.generate_file(
            "templates/widget.tpl",
            Path(output_root) / f"{file_name}.py",
            {
                "class_name": class_name,
                "widget_name": name,
            },
        )
