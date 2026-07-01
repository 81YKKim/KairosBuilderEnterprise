from pathlib import Path

from builder.application.builder_service import BuilderService
from builder.cli.command_router import CommandRouter


def test_builder_new_command_creates_project(tmp_path: Path):
    service = BuilderService()
    router = CommandRouter(service)

    # override output root via direct service call
    result = service.create_project("KairosDesktop", str(tmp_path))

    assert result.exists()
    assert (result / "src").exists()
    assert (result / "tests").exists()
    assert (result / "docs").exists()
    assert (result / "README.md").exists()
    assert (result / "pyproject.toml").exists()
    assert (result / ".gitignore").exists()


def test_command_router_new_command(tmp_path: Path):
    service = BuilderService()
    router = CommandRouter(service)

    result = router.handle("new KairosDesktop")

    assert result is not None