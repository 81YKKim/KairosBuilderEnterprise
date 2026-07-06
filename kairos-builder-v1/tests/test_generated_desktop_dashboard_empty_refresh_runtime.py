import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_dashboard_empty_recommendation_refresh_runtime_contract(
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
from desktop.viewmodels.dashboard_view_model import DashboardViewModel


app = QApplication.instance() or QApplication([])

view_model = DashboardViewModel()
dashboard = Dashboard(view_model=view_model)

assert dashboard.recommendation_table.table.rowCount() > 0

dashboard.recommendation_table.table.cellClicked.emit(0, 0)

assert dashboard.recommendation_detail.symbol_label.text() != "-"

dashboard.recommendation_detail.clear()
view_model.set_recommendations([])

assert dashboard.recommendation_table.table.rowCount() == 0
assert dashboard.recommendation_detail.symbol_label.text() == "-"
assert dashboard.recommendation_detail.entry_timing_label.text() == "-"
assert (
    dashboard.recommendation_detail.entry_timing_label.objectName()
    == "entryTimingDefault"
)

view_model.set_status("NO CANDIDATES")

assert dashboard.status_label.text() == "Status: NO CANDIDATES"

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
