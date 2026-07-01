from builder.application.builder_service import BuilderService


def test_builder_service_creates_project(tmp_path):
    service = BuilderService()

    result = service.create_project("sample_project", tmp_path)

    assert result.exists()
    assert (result / "src").exists()
    assert (result / "tests").exists()
    assert (result / "docs").exists()
    assert (result / "README.md").exists()
