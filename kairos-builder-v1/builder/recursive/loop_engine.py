from builder.recursive.snapshot import Snapshot
from builder.recursive.analyzer import Analyzer
from builder.recursive.improver import Improver
from builder.recursive.stability_gate import StabilityGate


class RecursiveLoopEngine:
    def __init__(self):
        self.snapshot = Snapshot()
        self.analyzer = Analyzer()
        self.improver = Improver()
        self.gate = StabilityGate()

    def run(self, iterations: int = 3) -> dict:
        history = []

        for _ in range(iterations):
            snap = self.snapshot.capture()
            analysis = self.analyzer.analyze(snap)
            improvement = self.improver.improve(analysis)
            stable = self.gate.check(improvement)

            history.append({
                "snapshot": snap,
                "analysis": analysis,
                "improvement": improvement,
                "stable": stable
            })

            if stable:
                break

        return {
            "iterations": len(history),
            "history": history
        }