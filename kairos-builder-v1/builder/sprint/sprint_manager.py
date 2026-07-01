import json
from pathlib import Path


class SprintManager:
    def __init__(self, context_path: str = "builder/context/sprint.json") -> None:
        self.context_path = Path(context_path)

    def initialize(self, current_sprint: int = 24) -> dict:
        data = {
            "current_sprint": current_sprint,
            "status": "ready",
            "last_commit": "#000023",
            "version": "1.0.0",
        }
        self.context_path.parent.mkdir(parents=True, exist_ok=True)
        self.context_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data

    def load(self) -> dict:
        if not self.context_path.exists():
            return self.initialize()
        return json.loads(self.context_path.read_text(encoding="utf-8"))

    def sprint_label(self) -> str:
        data = self.load()
        return f"#{data['current_sprint']:06d}"

    def build_commit_message(self, commit_type: str, scope: str, message: str) -> str:
        return f"{self.sprint_label()} {commit_type}({scope}): {message}"
