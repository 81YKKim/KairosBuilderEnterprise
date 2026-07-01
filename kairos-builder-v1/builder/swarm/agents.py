class PlannerAgent:
    def run(self, task: str) -> dict:
        return {"plan": f"plan for {task}"}


class BuilderAgent:
    def run(self, plan: dict) -> dict:
        return {"build": f"built from {plan['plan']}"}


class ReviewerAgent:
    def run(self, build: dict) -> dict:
        return {"review": f"approved {build['build']}"}