import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_table_duplicate_rank_runtime_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from PySide6.QtWidgets import QApplication

from desktop.widgets.recommendation_table import RecommendationTable


app = QApplication.instance() or QApplication([])

widget = RecommendationTable()

widget.set_recommendations(
    [
        {
            "rank": 2,
            "symbol": "DFNS",
            "score": 95,
            "signal": "WATCH",
            "status": "Monitoring",
        },
        {
            "rank": 1,
            "symbol": "VSME",
            "score": 99,
            "signal": "BUY",
            "status": "Actionable",
        },
        {
            "rank": 2,
            "symbol": "ADTX",
            "score": 93,
            "signal": "WATCH",
            "status": "Monitoring",
        },
        {
            "rank": 1,
            "symbol": "CPOP",
            "score": 98,
            "signal": "BUY",
            "status": "Actionable",
        },
    ]
)

assert widget.table.rowCount() == 4

symbols = [
    widget.table.item(row, 1).text()
    for row in range(4)
]

assert symbols == [
    "VSME",
    "CPOP",
    "DFNS",
    "ADTX",
]

assert widget.table.item(0, 0).font().bold()
assert widget.table.item(1, 0).font().bold()

widget.close()
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
