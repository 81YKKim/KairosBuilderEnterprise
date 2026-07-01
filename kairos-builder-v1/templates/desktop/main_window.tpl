from __future__ import annotations


class {{class_name}}MainWindow:
    title = "{{project_name}}"

    def describe(self) -> dict[str, str]:
        return {
            "title": self.title,
            "architecture": "PySide6 MVVM Enterprise Desktop",
        }
