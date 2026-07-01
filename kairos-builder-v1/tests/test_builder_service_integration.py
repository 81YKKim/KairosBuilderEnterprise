from builder.application.builder_service import BuilderService


def test_builder_service_generates_domain(tmp_path):
    service = BuilderService()

    result = service.generate("domain", "User")

    assert result is not None


def test_builder_service_workflow_verify():
    service = BuilderService()

    assert service.workflow_verify() == "pytest\ngit status"


def test_builder_service_workflow_commit_message():
    service = BuilderService()

    result = service.workflow_commit_message("workflow", "service-integration")

    assert result.startswith("#000024 feat(workflow):")
    assert "service-integration" in result
