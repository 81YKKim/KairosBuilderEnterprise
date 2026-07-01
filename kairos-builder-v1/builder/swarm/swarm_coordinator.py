from builder.swarm.agents import PlannerAgent, BuilderAgent, ReviewerAgent
from builder.swarm.voting_engine import VotingEngine


class SwarmCoordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.builder = BuilderAgent()
        self.reviewer = ReviewerAgent()
        self.voter = VotingEngine()

    def execute(self, task: str) -> dict:
        plan = self.planner.run(task)
        build = self.builder.run(plan)
        review = self.reviewer.run(build)

        results = [plan, build, review]
        decision = self.voter.decide(results)

        return {
            "plan": plan,
            "build": build,
            "review": review,
            "decision": decision
        }