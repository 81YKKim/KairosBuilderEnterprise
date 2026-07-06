import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_market_service_invalid_recommendation_runtime_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from desktop.services.market_service import MarketService


class FakeAdapter:
    def __init__(self, data):
        self.data = data

    def load(self):
        return self.data


invalid_service = MarketService(
    adapter=FakeAdapter(
        {
            "status": "LIVE",
            "recommendations": "invalid",
        }
    )
)

assert invalid_service.get_market_status() == "LIVE"
assert invalid_service.get_recommendations() == []


mixed_service = MarketService(
    adapter=FakeAdapter(
        {
            "status": "PREMARKET",
            "recommendations": [
                {
                    "symbol": "VSME",
                    "rank": 1,
                },
                "INVALID",
                None,
                73,
                {
                    "symbol": "DFNS",
                    "rank": 2,
                },
            ],
        }
    )
)

recommendations = mixed_service.get_recommendations()

assert len(recommendations) == 2
assert recommendations[0]["symbol"] == "VSME"
assert recommendations[1]["symbol"] == "DFNS"
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
