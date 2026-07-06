import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_table_invalid_rank_runtime_contract(
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
            "rank": None,
            "symbol": "INVALID-NONE",
            "score": 70,
            "signal": "WAIT",
            "status": "Monitoring",
        },
        {
            "rank": 2,
            "symbol": "DFNS",
            "score": 95,
            "signal": "WATCH",
            "status": "Monitoring",
        },
        {
            "symbol": "INVALID-MISSING",
            "score": 60,
            "signal": "WAIT",
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
            "rank": "invalid",
            "symbol": "INVALID-TEXT",
            "score": 50,
            "signal": "WAIT",
            "status": "Monitoring",
        },
    ]
)

assert widget.table.rowCount() == 5

assert widget.table.item(0, 1).text() == "VSME"
assert widget.table.item(1, 1).text() == "DFNS"

trailing_symbols = {
    widget.table.item(row, 1).text()
    for row in range(2, 5)
}

assert trailing_symbols == {
    "INVALID-NONE",
    "INVALID-MISSING",
    "INVALID-TEXT",
}

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
