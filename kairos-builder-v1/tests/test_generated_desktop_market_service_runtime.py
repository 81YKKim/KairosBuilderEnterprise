import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_market_service_replay_adapter_runtime_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from desktop.services.market_service import MarketService
from desktop.adapters.replay_adapter import ReplayAdapter


adapter = ReplayAdapter()
service = MarketService(adapter=adapter)

status = service.get_market_status()
recommendations = service.get_recommendations()

assert status == "Market Service Connected"
assert len(recommendations) == 4

assert recommendations[0]["rank"] == 1
assert recommendations[0]["symbol"] == "KAIROS-A"
assert recommendations[0]["entry_timing"] == "BUY NOW"

assert recommendations[-1]["symbol"] == "KAIROS-D"
assert recommendations[-1]["entry_timing"] == "DO NOT CHASE"

for recommendation in recommendations:
    assert isinstance(recommendation, dict)
    assert "symbol" in recommendation
    assert "score" in recommendation
    assert "ai_score" in recommendation
    assert "entry_timing" in recommendation
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
