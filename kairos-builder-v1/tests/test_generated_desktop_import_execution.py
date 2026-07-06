import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_modules_import_in_isolated_process(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
import desktop
import desktop.app
import desktop.main
import desktop.main_window
import desktop.theme
import desktop.pages.dashboard
import desktop.widgets.sidebar
import desktop.widgets.recommendation_table
import desktop.widgets.recommendation_detail
import desktop.viewmodels.dashboard_view_model
import desktop.services.market_service
import desktop.adapters.replay_adapter
"""

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(src_root)

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
