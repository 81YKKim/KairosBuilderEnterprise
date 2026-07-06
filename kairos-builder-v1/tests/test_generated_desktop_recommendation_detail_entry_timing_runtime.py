import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_detail_entry_timing_style_contract(
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

cases = {
    "BUY NOW": "entryTimingBuyNow",
    "SPLIT BUY": "entryTimingSplitBuy",
    "WAIT PULLBACK": "entryTimingWaitPullback",
    "DO NOT CHASE": "entryTimingDoNotChase",
    "UNKNOWN": "entryTimingDefault",
}

for entry_timing, expected_object_name in cases.items():
    detail.set_recommendation(
        {
            "symbol": "VSME",
            "entry_timing": entry_timing,
        }
    )

    assert detail.entry_timing_label.text() == entry_timing
    assert detail.entry_timing_label.objectName() == expected_object_name

assert detail.entry_timing_label.font().bold() is False

detail.set_recommendation(
    {
        "symbol": "VSME",
        "entry_timing": "BUY NOW",
    }
)

assert detail.entry_timing_label.font().bold() is True

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
