from builder.services.manifest_service import ManifestService


def test_manifest_loader():
    manifest = ManifestService().load_manifest("builder.manifest.json")
    assert manifest.project_name == "Kairos Builder Enterprise"
    assert manifest.project_version == "1.0.0"
    assert manifest.language == "Python"
    assert manifest.architecture == "Enterprise"
