from builder.healing.failure_detector import FailureDetector
from builder.healing.root_cause_analyzer import RootCauseAnalyzer
from builder.healing.fix_strategy_engine import FixStrategyEngine
from builder.healing.auto_patch_generator import AutoPatchGenerator


class RecoveryEngine:
    def __init__(self):
        self.detector = FailureDetector()
        self.analyzer = RootCauseAnalyzer()
        self.strategy = FixStrategyEngine()
        self.patcher = AutoPatchGenerator()

    def run(self, test_result: dict) -> dict:
        failed = self.detector.detect(test_result)
        cause = self.analyzer.analyze(test_result if failed else {})
        plan = self.strategy.generate(cause)
        patch = self.patcher.build(plan)

        return {
            "failed": failed,
            "cause": cause,
            "plan": plan,
            "patch": patch
        }