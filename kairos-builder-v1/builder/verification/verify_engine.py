from __future__ import annotations

import subprocess
from pathlib import Path


class BuilderVerifyEngine:
    def run_pytest(self) -> str:
        result = subprocess.run(
            ["pytest", "-q"],
            capture_output=True,
            text=True,
        )
        return result.stdout + result.stderr

    def check_project_structure(self, path: str | Path) -> dict:
        root = Path(path)

        checks = {
            "src": (root / "src").exists(),
            "tests": (root / "tests").exists(),
            "docs": (root / "docs").exists(),
            "manifest": (root / "builder.manifest.json").exists(),
            "readme": (root / "README.md").exists(),
        }

        return checks

    def health_report(self, path: str | Path) -> dict:
        structure = self.check_project_structure(path)

        return {
            "structure": structure,
            "all_ok": all(structure.values()),
        }