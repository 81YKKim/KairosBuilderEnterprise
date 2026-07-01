from builder.evolution.result_analyzer import ResultAnalyzer
from builder.evolution.pattern_detector import PatternDetector
from builder.evolution.improvement_engine import ImprovementEngine
from builder.evolution.self_patch_engine import SelfPatchEngine


class EvolutionLoop:
    def __init__(self):
        self.analyzer = ResultAnalyzer()
        self.detector = PatternDetector()
        self.engine = ImprovementEngine()
        self.patcher = SelfPatchEngine()

    def run(self, test_result: dict) -> dict:
        analysis = self.analyzer.analyze(test_result)
        pattern = self.detector.detect([])
        suggestion = self.engine.suggest(analysis)
        patch = self.patcher.create_patch(suggestion)

        return {
            "analysis": analysis,
            "pattern": pattern,
            "suggestion": suggestion,
            "patch": patch
        }