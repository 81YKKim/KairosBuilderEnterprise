from __future__ import annotations


class Theme:
    name = "{{project_name}} Theme"

    def palette(self) -> dict[str, str]:
        return {
            "mode": "dark",
            "accent": "kairos",
        }
