import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_detail_missing_fields_runtime_contract(
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

detail.set_recommendation(
    {
        "symbol": "VSME",
    }
)

assert detail.symbol_label.text() == "VSME"
assert detail.score_label.text() == "-"
assert detail.signal_label.text() == "-"
assert detail.status_label.text() == "-"
assert detail.ai_score_label.text() == "-"
assert detail.entry_timing_label.text() == "-"
assert detail.entry_timing_label.objectName() == "entryTimingDefault"
assert detail.evidence_label.text() == "-"

detail.set_recommendation(None)

assert detail.symbol_label.text() == "-"
assert detail.score_label.text() == "-"
assert detail.signal_label.text() == "-"
assert detail.status_label.text() == "-"
assert detail.ai_score_label.text() == "-"
assert detail.entry_timing_label.text() == "-"
assert detail.entry_timing_label.objectName() == "entryTimingDefault"
assert detail.evidence_label.text() == "-"

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
