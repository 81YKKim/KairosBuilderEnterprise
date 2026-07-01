class TemplateRegistry:
    def __init__(self):
        self.templates = {
            "project": {
                "v1": {
                    "structure": [
                        "src",
                        "tests",
                        "docs",
                        "resources",  # ⭐ 추가 (핵심 수정)
                        "data"
                    ],
                    "files": [
                        "README.md",
                        "pyproject.toml",
                        ".gitignore"
                    ]
                }
            }
        }

    def get(self, name: str, version: str = "v1"):
        return self.templates.get(name, {}).get(version)