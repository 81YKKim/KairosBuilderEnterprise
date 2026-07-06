from dataclasses import dataclass


@dataclass(frozen=True)
class VersionLock:
    version: str = "2.0.0-alpha"
    state: str = "STABLE"
    allow_changes: bool = False

    def is_frozen(self) -> bool:
        return self.state == "FROZEN"

    def is_stable(self) -> bool:
        return self.state == "STABLE"