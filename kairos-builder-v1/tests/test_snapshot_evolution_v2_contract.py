from builder.recursive.snapshot import Snapshot
from builder.evolution.version_controller import VersionController


def test_snapshot_uses_enterprise_v2_version():
    snapshot = Snapshot().capture()

    assert snapshot["state"] == "stable"
    assert snapshot["version"] == "2.0.0-alpha"


def test_version_controller_uses_enterprise_v2_versions():
    controller = VersionController()

    assert controller.bump(False) == "v2.0.0-alpha"
    assert controller.bump(True) == "v2.1.0"
