"""
Sprint Runner Foundation
Sprint #000034
"""


class SprintRunner:
    """Runs a single Builder sprint workflow."""

    def create(self, sprint_number: int) -> str:
        return f"Sprint #{sprint_number:06d} create completed"

    def verify(self, sprint_number: int) -> str:
        return f"Sprint #{sprint_number:06d} verify completed"

    def commit(self, sprint_number: int) -> str:
        return f"Sprint #{sprint_number:06d} commit completed"

    def run(self, sprint_number: int) -> str:
        steps = (
            self.create,
            self.verify,
            self.commit,
        )

        for step in steps:
            step(sprint_number)

        return f"Sprint #{sprint_number:06d} run completed"
