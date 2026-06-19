from dataclasses import dataclass


@dataclass
class SprintPlan:
    number: int
    name: str

    @property
    def sprint_id(self) -> str:
        return f"{self.number:06d}"

    @property
    def normalized_name(self) -> str:
        return self.name.replace(" ", "_").replace("-", "_")

    @property
    def display_name(self) -> str:
        return f"Sprint #{self.sprint_id} - {self.name}"
