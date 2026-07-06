import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_table_runtime_selection_contract(
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

recommendations = [
    {
        "rank": 1,
        "symbol": "VSME",
        "score": 97,
        "signal": "BUY",
        "status": "Actionable",
    }
]

selected = []

widget.recommendation_selected.connect(
    lambda recommendation: selected.append(recommendation)
)

widget.set_recommendations(recommendations)

assert widget.table.rowCount() == 1

widget.table.cellClicked.emit(0, 0)

assert selected
assert selected[0]["symbol"] == "VSME"
assert selected[0]["score"] == 97

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
