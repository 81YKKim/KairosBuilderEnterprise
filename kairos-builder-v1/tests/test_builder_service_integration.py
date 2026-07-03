from builder.application.builder_service import BuilderService


def test_builder_service_generates_domain(tmp_path):
    service = BuilderService()

    result = service.generate(
        "domain",
        "User",
        tmp_path,
    )

    assert result is not None


def test_builder_service_generates_desktop(tmp_path):
    service = BuilderService()

    result = service.generate(
        "desktop",
        "KairosDesktop",
        tmp_path,
    )

    assert result.project_name == "KairosDesktop"
    assert result.generated_count == 12

    desktop_root = (
        result.project_path
        / "src"
        / "desktop"
    )

    assert (desktop_root / "app.py").exists()
    assert (desktop_root / "main.py").exists()
    assert (desktop_root / "main_window.py").exists()
    assert (desktop_root / "theme.py").exists()
    assert (desktop_root / "pages" / "dashboard.py").exists()
    assert (desktop_root / "widgets" / "sidebar.py").exists()
    assert (
        desktop_root
        / "widgets"
        / "recommendation_detail.py"
    ).exists()


def test_builder_service_workflow_verify():
    service = BuilderService()

    assert service.workflow_verify() == "pytest\ngit status"


def test_builder_service_workflow_commit_message():
    service = BuilderService()

    result = service.workflow_commit_message(
        "workflow",
        "service-integration",
    )

    assert result.startswith(
        "#000024 feat(workflow):"
    )
    assert "service-integration" in result