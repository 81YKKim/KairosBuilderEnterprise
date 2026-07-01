class GoalPlanner:
    def plan(self, goal: str) -> list[str]:
        goal = goal.lower()

        if "project" in goal:
            return ["new", "generate", "list", "verify"]

        if "build" in goal:
            return ["generate", "verify", "package"]

        if "release" in goal:
            return ["build", "package", "release"]

        return ["verify"]