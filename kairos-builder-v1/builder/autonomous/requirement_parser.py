class RequirementParser:
    def parse(self, text: str) -> dict:
        return {
            "raw": text,
            "type": "ai_project",
            "complexity": "medium"
        }