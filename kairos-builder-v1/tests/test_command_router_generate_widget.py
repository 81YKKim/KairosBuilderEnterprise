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


def test_command_router_generate_widget(
    tmp_path: Path,
):
    service = TemporaryOutputBuilderService(tmp_path)
    router = CommandRouter(service)

    result = router.handle(
        "generate widget RecommendationTable"
    )

    assert result.exists()
    assert result.name == "recommendation_table.py"

    source = result.read_text(encoding="utf-8")

    assert "class RecommendationTable" in source


def test_widget_registry_uses_widget_generator():
    service = BuilderService()

    generator = service.generator_registry.create("widget")

    assert generator.__class__.__name__ == "WidgetGenerator"