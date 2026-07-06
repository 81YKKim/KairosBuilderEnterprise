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


def test_command_router_generate_viewmodel(
    tmp_path: Path,
):
    service = TemporaryOutputBuilderService(tmp_path)
    router = CommandRouter(service)

    result = router.handle(
        "generate viewmodel DashboardViewModel"
    )

    assert result.exists()
    assert result.parent == tmp_path
    assert result.name == "dashboard_view_model.py"

    source = result.read_text(encoding="utf-8")

    assert "class DashboardViewModel" in source


def test_viewmodel_registry_uses_viewmodel_generator():
    service = BuilderService()

    generator = service.generator_registry.create("viewmodel")

    assert generator.__class__.__name__ == "ViewModelGenerator"