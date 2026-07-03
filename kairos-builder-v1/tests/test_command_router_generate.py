from pathlib import Path

from builder.application.builder_service import BuilderService
from builder.cli.command_router import CommandRouter


class TemporaryOutputBuilderService(BuilderService):
    def __init__(self, output_root: Path) -> None:
        super().__init__()
        self.output_root = output_root

    def generate(
        self,
        generator_type: str,
        name: str,
        output_root=None,
    ):
        return super().generate(
            generator_type,
            name,
            self.output_root,
        )


def test_command_router_generate_desktop(
    tmp_path: Path,
):
    service = TemporaryOutputBuilderService(tmp_path)
    router = CommandRouter(service)

    result = router.handle(
        "generate desktop KairosDesktop"
    )

    assert result.project_name == "KairosDesktop"

    desktop_root = (
        result.project_path
        / "src"
        / "desktop"
    )

    assert (desktop_root / "app.py").exists()
    assert (desktop_root / "main.py").exists()
    assert (desktop_root / "main_window.py").exists()
    assert (desktop_root / "theme.py").exists()


def test_command_router_unknown_generator():
    router = CommandRouter()

    result = router.handle(
        "generate unknown Example"
    )

    assert result == {
        "error": "Unknown generator: unknown",
    }