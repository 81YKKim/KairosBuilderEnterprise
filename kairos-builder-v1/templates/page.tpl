from __future__ import annotations


class {{class_name}}:
    title = "{{page_name}}"

    def describe(self) -> dict[str, str]:
        return {
            "page": self.title,
            "layer": "desktop.page",
        }
