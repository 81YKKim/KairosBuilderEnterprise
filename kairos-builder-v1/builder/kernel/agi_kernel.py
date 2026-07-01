from builder.kernel.architecture_analyzer import ArchitectureAnalyzer
from builder.kernel.refactor_planner import RefactorPlanner
from builder.kernel.mutation_engine import MutationEngine
from builder.kernel.safety_gate import SafetyGate


class AGIKernel:
    def __init__(self):
        self.analyzer = ArchitectureAnalyzer()
        self.planner = RefactorPlanner()
        self.mutator = MutationEngine()
        self.safety = SafetyGate()

    def run(self) -> dict:
        architecture = self.analyzer.analyze()
        plan = self.planner.plan(architecture)
        mutation = self.mutator.mutate(plan)

        if not self.safety.validate(mutation):
            return {"status": "blocked"}

        return {
            "architecture": architecture,
            "plan": plan,
            "mutation": mutation,
            "status": "applied"
        }