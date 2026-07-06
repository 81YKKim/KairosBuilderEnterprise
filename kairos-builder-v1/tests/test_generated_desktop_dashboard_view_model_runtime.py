import os
import subprocess
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_dashboard_view_model_runtime_service_refresh_contract(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"

    script = """
from desktop.viewmodels.dashboard_view_model import DashboardViewModel


class FakeMarketService:
    def __init__(self):
        self.status = "PREMARKET"
        self.recommendations = [
            {
                "rank": 1,
                "symbol": "VSME",
                "score": 97,
                "signal": "BUY",
                "status": "Actionable",
                "ai_score": 99,
                "entry_timing": "BUY NOW",
                "evidence": "initial runtime data",
            }
        ]

    def get_market_status(self):
        return self.status

    def get_recommendations(self):
        return list(self.recommendations)


service = FakeMarketService()
view_model = DashboardViewModel(
    market_service=service,
)

status_changes = []
recommendation_changes = []

view_model.status_changed.connect(
    lambda: status_changes.append(view_model.status)
)
view_model.recommendations_changed.connect(
    lambda: recommendation_changes.append(
        view_model.recommendations
    )
)

service.status = "REGULAR"
service.recommendations = [
    {
        "rank": 1,
        "symbol": "DFNS",
        "score": 98,
        "signal": "BUY",
        "status": "Actionable",
        "ai_score": 99,
        "entry_timing": "BUY NOW",
        "evidence": "refreshed runtime data",
    },
    {
        "rank": 2,
        "symbol": "ADTX",
        "score": 91,
        "signal": "WATCH",
        "status": "Monitoring",
        "ai_score": 93,
        "entry_timing": "SPLIT BUY",
        "evidence": "secondary runtime data",
    },
]

view_model.refresh()

assert view_model.status == "REGULAR"
assert len(view_model.recommendations) == 2
assert view_model.recommendations[0]["symbol"] == "DFNS"
assert view_model.recommendations[1]["symbol"] == "ADTX"

assert status_changes == ["REGULAR"]
assert len(recommendation_changes) == 1
assert recommendation_changes[0][0]["symbol"] == "DFNS"
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
