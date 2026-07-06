import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_detail_runtime_binding_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from PySide6.QtWidgets import QApplication

from desktop.widgets.recommendation_detail import RecommendationDetail


app = QApplication.instance() or QApplication([])

detail = RecommendationDetail()

recommendation = {
    "symbol": "VSME",
    "score": 94,
    "signal": "BUY",
    "status": "Actionable",
    "ai_score": 97,
    "entry_timing": "BUY NOW",
    "evidence": "volume spike",
}

detail.set_recommendation(recommendation)

assert detail.symbol_label.text() == "VSME"
assert detail.score_label.text() == "94"
assert detail.signal_label.text() == "BUY"
assert detail.status_label.text() == "Actionable"
assert detail.ai_score_label.text() == "97"
assert detail.entry_timing_label.text() == "BUY NOW"
assert detail.entry_timing_label.objectName() == "entryTimingBuyNow"
assert detail.entry_timing_label.font().bold()
assert detail.evidence_label.text() == "volume spike"

detail.clear()

assert detail.symbol_label.text() == "-"
assert detail.entry_timing_label.objectName() == "entryTimingDefault"

detail.close()
app.quit()
"""

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(src_root)
    environment["QT_QPA_PLATFORM"] = "offscreen"

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
        ],
        cwd=result.project_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, (
        completed.stdout + completed.stderr
    )
