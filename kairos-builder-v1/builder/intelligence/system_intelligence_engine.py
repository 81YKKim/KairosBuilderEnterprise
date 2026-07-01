from __future__ import annotations

from pathlib import Path


class BuilderIntelligenceEngine:
    def inspect_project(self, path: str | Path = ".") -> dict:
        root = Path(path)

        return {
            "project_root": str(root),
            "structure": self._check_structure(root),
            "generators": self._check_generators(),
            "manifest": self._check_manifest(root),
        }

    def health(self, path: str | Path = ".") -> dict:
        report = self.inspect_project(path)

        score = 0
        total = 3

        if all(report["structure"].values()):
            score += 1

        if report["generators"]["count"] > 0:
            score += 1

        if report["manifest"]:
            score += 1

        return {
            "score": score,
            "status": "healthy" if score == total else "degraded",
            "details": report,
        }

    # -------------------------
    # internal checks
    # -------------------------
    def _check_structure(self, root: Path) -> dict:
        return {
            "src": (root / "src").exists(),
            "tests": (root / "tests").exists(),
            "docs": (root / "docs").exists(),
        }

    def _check_generators(self) -> dict:
        return {
            "count": 8,
            "status": "ok",
        }

    def _check_manifest(self, root: Path) -> bool:
        return (root / "builder.manifest.json").exists()