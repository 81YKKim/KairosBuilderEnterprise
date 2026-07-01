from builder.evolution.change_detector import ChangeDetector
from builder.evolution.improvement_proposer import ImprovementProposer
from builder.evolution.evolution_decision_engine import EvolutionDecisionEngine
from builder.evolution.code_mutator import CodeMutator
from builder.evolution.version_controller import VersionController


class AutoEvolutionLoop:
    def __init__(self):
        self.detector = ChangeDetector()
        self.proposer = ImprovementProposer()
        self.decision = EvolutionDecisionEngine()
        self.mutator = CodeMutator()
        self.version = VersionController()

    def run(self, metrics: dict) -> dict:
        changed = self.detector.detect(metrics)
        proposal = self.proposer.propose(metrics if changed else {})
        decision = self.decision.decide(proposal)
        mutation = self.mutator.mutate(decision)
        version = self.version.bump(decision == "apply")

        return {
            "changed": changed,
            "proposal": proposal,
            "decision": decision,
            "mutation": mutation,
            "version": version
        }