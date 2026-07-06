import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_recommendation_table_empty_runtime_contract(
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

selected = []

widget.recommendation_selected.connect(
    lambda recommendation: selected.append(recommendation)
)

widget.set_recommendations([])

assert widget.table.rowCount() == 0
assert widget._recommendations == []

widget.table.cellClicked.emit(0, 0)

assert selected == []

widget.set_recommendations(
    [
        {
            "rank": 1,
            "symbol": "VSME",
            "score": 99,
            "signal": "BUY",
            "status": "Actionable",
        }
    ]
)

assert widget.table.rowCount() == 1

widget.set_recommendations([])

assert widget.table.rowCount() == 0
assert widget._recommendations == []

widget.table.cellClicked.emit(0, 0)

assert selected == []

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
