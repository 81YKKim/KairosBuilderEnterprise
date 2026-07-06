import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_foundation_test_executes_with_pytest(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_desktop_foundation.py",
            "-q",
        ],
        cwd=result.project_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, (
        completed.stdout + completed.stderr
    )
