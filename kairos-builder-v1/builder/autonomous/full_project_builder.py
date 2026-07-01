class FullProjectBuilder:
    def build(self, architecture: dict) -> dict:
        return {
            "project": "KairosAutoGen",
            "status": "generated",
            "layers": architecture["layers"]
        }