from __future__ import annotations


def create_app() -> dict[str, str]:
    return {
        "project": "{{project_name}}",
        "desktop": "ready",
    }
