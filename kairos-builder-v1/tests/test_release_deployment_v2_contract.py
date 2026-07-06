from builder.release.package_builder import PackageBuilder
from builder.release.release_engine import ReleaseEngine
from builder.release.version_lock import VersionLock
from builder.deployment.deployment_engine import DeploymentEngine


def test_package_builder_uses_enterprise_v2_version(tmp_path):
    dist = PackageBuilder().build_package(tmp_path)

    package_json = (dist / "package.json").read_text(encoding="utf-8")

    assert '"version": "2.0.0-alpha"' in package_json


def test_release_engine_uses_enterprise_v2_version(tmp_path):
    engine = ReleaseEngine()

    build = engine.build(tmp_path)
    release = engine.release(tmp_path)

    assert build["version"] == "2.0.0-alpha"
    assert release["version"] == "2.0.0-alpha"


def test_version_lock_defaults_to_enterprise_v2_version():
    lock = VersionLock()

    assert lock.version == "2.0.0-alpha"
    assert lock.is_stable()


def test_deployment_engine_defaults_to_enterprise_v2_version():
    result = DeploymentEngine().deploy({})

    assert result["version"] == "2.0.0-alpha"
