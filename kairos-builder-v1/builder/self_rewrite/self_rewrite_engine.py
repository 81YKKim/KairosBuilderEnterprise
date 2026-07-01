from builder.self_rewrite.snapshot_engine import SnapshotEngine
from builder.self_rewrite.codebase_analyzer import CodebaseAnalyzer
from builder.self_rewrite.rewrite_planner import RewritePlanner
from builder.self_rewrite.code_rebuilder import CodeRebuilder
from builder.self_rewrite.version_replacer import VersionReplacer


class SelfRewriteEngine:
    def __init__(self):
        self.snapshot = SnapshotEngine()
        self.analyzer = CodebaseAnalyzer()
        self.planner = RewritePlanner()
        self.rebuilder = CodeRebuilder()
        self.version = VersionReplacer()

    def run(self) -> dict:
        snap = self.snapshot.capture()
        analysis = self.analyzer.analyze(snap)
        plan = self.planner.plan(analysis)
        result = self.rebuilder.rebuild(plan)
        version = self.version.replace(result)

        return {
            "snapshot": snap,
            "analysis": analysis,
            "plan": plan,
            "result": result,
            "version": version
        }