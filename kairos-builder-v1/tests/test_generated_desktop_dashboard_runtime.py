import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_dashboard_runtime_integration_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from PySide6.QtWidgets import QApplication

from desktop.pages.dashboard import Dashboard


app = QApplication.instance() or QApplication([])

dashboard = Dashboard()

assert dashboard.title_label.text() == "Kairos Dashboard"
assert dashboard.subtitle_label.text() == "Enterprise MVVM Desktop"
assert dashboard.status_label.text().startswith("Status: ")
assert dashboard.recommendation_table.table.rowCount() > 0

dashboard.recommendation_table.table.cellClicked.emit(0, 0)

assert dashboard.recommendation_detail.symbol_label.text() != "-"
assert dashboard.recommendation_detail.entry_timing_label.text() != "-"

dashboard.close()
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
