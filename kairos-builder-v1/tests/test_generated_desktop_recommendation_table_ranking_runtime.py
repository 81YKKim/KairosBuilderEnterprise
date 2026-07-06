import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_table_runtime_ranking_contract(
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
            "rank": 3,
            "symbol": "ADTX",
            "score": 89,
            "signal": "WAIT",
            "status": "Pullback",
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
            "symbol": "DFNS",
            "score": 95,
            "signal": "WATCH",
            "status": "Monitoring",
        },
    ]
)

assert widget.table.rowCount() == 3

assert widget.table.item(0, 0).text() == "1"
assert widget.table.item(0, 1).text() == "VSME"

assert widget.table.item(1, 0).text() == "2"
assert widget.table.item(1, 1).text() == "DFNS"

assert widget.table.item(2, 0).text() == "3"
assert widget.table.item(2, 1).text() == "ADTX"

assert widget.table.item(0, 0).font().bold()
assert widget.table.item(0, 1).font().bold()

selected = []

widget.recommendation_selected.connect(
    lambda recommendation: selected.append(recommendation)
)

widget.table.cellClicked.emit(0, 1)

assert selected
assert selected[0]["rank"] == 1
assert selected[0]["symbol"] == "VSME"

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
