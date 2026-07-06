import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_main_window_runtime_structure(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from PySide6.QtWidgets import QApplication, QStackedWidget

from desktop.main_window import MainWindow
from desktop.pages.dashboard import Dashboard
from desktop.widgets.sidebar import Sidebar


app = QApplication.instance() or QApplication([])

window = MainWindow()

assert isinstance(window.sidebar, Sidebar)
assert isinstance(window.page_stack, QStackedWidget)
assert isinstance(window.dashboard, Dashboard)
assert window.page_stack.count() == 1
assert window.page_stack.widget(0) is window.dashboard
assert window.page_stack.currentWidget() is window.dashboard

window.close()
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
