from __future__ import annotations


class {{class_name}}:
    name = "{{widget_name}}"

    def render_state(self) -> dict[str, str]:
        return {
            "widget": self.name,
            "layer": "desktop.widget",
        }
