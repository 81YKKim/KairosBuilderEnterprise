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


def test_command_router_generate_page(
    tmp_path: Path,
):
    service = TemporaryOutputBuilderService(tmp_path)
    router = CommandRouter(service)

    result = router.handle(
        "generate page Dashboard"
    )

    assert result.exists()
    assert result.name == "dashboard.py"

    source = result.read_text(encoding="utf-8")

    assert "class Dashboard" in source


def test_page_registry_uses_page_generator():
    service = BuilderService()

    generator = service.generator_registry.create("page")

    assert generator.__class__.__name__ == "PageGenerator"