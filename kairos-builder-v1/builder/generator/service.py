from pathlib import Path

from builder.generator.file_generator import FileGenerator


class ServiceGenerator(FileGenerator):
    category = "file"

    def generate(
        self,
        name: str,
        output_root: str = "output/service",
    ) -> Path:
        class_name = self.to_class_name(name)
        file_name = self.to_snake_name(name)

        return self.generate_file(
            "templates/service.tpl",
            Path(output_root) / f"{file_name}_service.py",
            {
                "class_name": class_name,
            },
        )