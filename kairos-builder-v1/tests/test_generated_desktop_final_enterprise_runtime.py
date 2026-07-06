import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_final_enterprise_runtime_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosUltimateEnterpriseXDesktop",
        str(tmp_path),
    )

    project_path = result.project_path
    src_root = project_path / "src"

    test_environment = os.environ.copy()
    test_environment["PYTHONPATH"] = str(src_root)
    test_environment["QT_QPA_PLATFORM"] = "offscreen"

    generated_tests = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
        ],
        cwd=project_path,
        env=test_environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert generated_tests.returncode == 0, (
        generated_tests.stdout
        + generated_tests.stderr
    )

    runtime_script = """
from PySide6.QtWidgets import QApplication, QStackedWidget

from desktop.app import create_app
from desktop.main_window import MainWindow
from desktop.pages.dashboard import Dashboard
from desktop.widgets.recommendation_detail import RecommendationDetail
from desktop.widgets.recommendation_table import RecommendationTable
from desktop.widgets.sidebar import Sidebar


app = create_app()

assert app is not None
assert isinstance(app.main_window, MainWindow)
assert isinstance(app.main_window.sidebar, Sidebar)
assert isinstance(app.main_window.page_stack, QStackedWidget)
assert isinstance(app.main_window.dashboard, Dashboard)

dashboard = app.main_window.dashboard

assert isinstance(
    dashboard.recommendation_table,
    RecommendationTable,
)
assert isinstance(
    dashboard.recommendation_detail,
    RecommendationDetail,
)

assert dashboard.recommendation_table.table.rowCount() > 0

dashboard.recommendation_table.table.cellClicked.emit(0, 0)

assert dashboard.recommendation_detail.symbol_label.text() != "-"
assert dashboard.recommendation_detail.ai_score_label.text() != "-"
assert dashboard.recommendation_detail.entry_timing_label.text() != "-"

dashboard.view_model.set_recommendations([])

assert dashboard.recommendation_table.table.rowCount() == 0
assert dashboard.recommendation_detail.symbol_label.text() == "-"
assert dashboard.recommendation_detail.entry_timing_label.text() == "-"
assert (
    dashboard.recommendation_detail.entry_timing_label.objectName()
    == "entryTimingDefault"
)

app.main_window.close()
app.quit()
"""

    runtime = subprocess.run(
        [
            sys.executable,
            "-c",
            runtime_script,
        ],
        cwd=project_path,
        env=test_environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert runtime.returncode == 0, (
        runtime.stdout + runtime.stderr
    )
