class VersionController:
    def bump(self, applied: bool) -> str:
        return "v2.1.0" if applied else "v2.0.0-alpha"