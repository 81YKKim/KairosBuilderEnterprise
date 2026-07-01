from __future__ import annotations


class {{class_name}}:
    name = "{{viewmodel_name}}"

    def to_dict(self) -> dict[str, str]:
        return {
            "viewmodel": self.name,
            "layer": "desktop.viewmodel",
        }
