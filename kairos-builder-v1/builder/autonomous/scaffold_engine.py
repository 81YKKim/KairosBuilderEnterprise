class ScaffoldEngine:
    def build(self, architecture: dict) -> list:
        files = []

        for layer in architecture["layers"]:
            files.append(f"{layer}/__init__.py")
            files.append(f"{layer}/core.py")

        return files