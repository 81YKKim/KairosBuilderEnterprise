from __future__ import annotations


class {{class_name}}:
    name = "{{adapter_name}}"

    def load(self) -> dict[str, str]:
        return {
            "adapter": self.name,
            "layer": "desktop.adapter",
        }
