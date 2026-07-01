from dataclasses import dataclass


@dataclass(frozen=True)
class VersionLock:
    version: str = "1.0.0"
    state: str = "STABLE"  # STABLE | FROZEN
    allow_changes: bool = False

    def is_frozen(self) -> bool:
        return self.state == "FROZEN"

    def is_stable(self) -> bool:
        return self.state == "STABLE"