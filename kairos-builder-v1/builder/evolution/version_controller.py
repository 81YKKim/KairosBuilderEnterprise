class VersionController:
    def bump(self, applied: bool) -> str:
        return "v1.1.0" if applied else "v1.0.0"