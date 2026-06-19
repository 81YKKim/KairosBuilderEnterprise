from dataclasses import dataclass


@dataclass
class Project:
    name: str
    path: str
    language: str = "Python"
    branch: str = "main"
    manifest: str = "builder.manifest.json"
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "language": self.language,
            "branch": self.branch,
            "manifest": self.manifest,
            "enabled": self.enabled,
        }

    @staticmethod
    def from_dict(data: dict) -> "Project":
        return Project(
            name=data["name"],
            path=data["path"],
            language=data.get("language", "Python"),
            branch=data.get("branch", "main"),
            manifest=data.get("manifest", "builder.manifest.json"),
            enabled=data.get("enabled", True),
        )
