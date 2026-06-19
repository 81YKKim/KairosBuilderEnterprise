from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenerator(ABC):
    def generate(self, name: str, output_root: str) -> Path:
        file_name = self.to_file_name(name)
        output_path = Path(output_root) / file_name

        if output_path.exists():
            return output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            self.build_content(name),
            encoding="utf-8",
        )

        return output_path

    def to_file_name(self, name: str) -> str:
        result = ""

        for index, char in enumerate(name):
            if char.isupper() and index > 0:
                result += "_"

            result += char.lower()

        return f"{result}.py"

    @abstractmethod
    def build_content(self, name: str) -> str:
        pass
