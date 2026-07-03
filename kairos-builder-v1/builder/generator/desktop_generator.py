from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from builder.generator.composite_generator import CompositeGenerator
from builder.generator.desktop_generator_result import DesktopGeneratorResult
from builder.generator.desktop_structure_validator import (
    DesktopStructureValidator,
)
from builder.manifest.desktop_manifest import DesktopManifest
from builder.manifest.desktop_manifest_writer import DesktopManifestWriter


class DesktopGenerator(CompositeGenerator):
    category = "desktop"

    def generate(
        self,
        name: str,
        output_root: str = "output/desktop",
    ) -> DesktopGeneratorResult:
        project_root = self.create_project_root(output_root, name)

        src_root = project_root / "src" / "desktop"
        tests_root = project_root / "tests"

        self.create_folders(
            [
                src_root,
                src_root / "pages",
                src_root / "widgets",
                src_root / "viewmodels",
                src_root / "services",
                src_root / "adapters",
                src_root / "themes",
                src_root / "resources",
                src_root / "assets",
                tests_root,
            ]
        )

        foundation_files = self._generate_desktop_foundation(
            project_name=name,
            src_root=src_root,
        )

        page = self._generate_template(
            src_root / "pages" / "dashboard.py",
            "dashboard.tpl",
        )
        sidebar = self._generate_template(
            src_root / "widgets" / "sidebar.py",
            "sidebar.tpl",
        )
        recommendation_table = self._generate_template(
            src_root / "widgets" / "recommendation_table.py",
            "recommendation_table.tpl",
        )
        recommendation_detail = self._generate_template(
            src_root / "widgets" / "recommendation_detail.py",
            "recommendation_detail.tpl",
        )
        viewmodel = self._generate_template(
            src_root / "viewmodels" / "dashboard_view_model.py",
            "dashboard_view_model.tpl",
        )
        service = self._generate_template(
            src_root / "services" / "market_service.py",
            "market_service.tpl",
        )
        adapter = self._generate_template(
            src_root / "adapters" / "replay_adapter.py",
            "replay_adapter.tpl",
        )

        generated = self.collect_results(
            foundation_files,
            page,
            sidebar,
            recommendation_table,
            recommendation_detail,
            viewmodel,
            service,
            adapter,
        )

        DesktopStructureValidator().validate(src_root)

        manifest = DesktopManifest(
            project_name=name,
            builder_version="2.0.0-alpha",
            generator="DesktopGenerator",
            architecture="MVVM",
            created_at=datetime.now(UTC).isoformat(),
            pages=1,
            widgets=3,
            viewmodels=1,
            services=1,
            adapters=1,
        )

        DesktopManifestWriter().write(
            manifest,
            project_root,
        )

        return DesktopGeneratorResult(
            project_name=name,
            project_path=project_root,
            generated_pages=(page,),
            generated_widgets=(
                sidebar,
                recommendation_table,
                recommendation_detail,
            ),
            generated_viewmodels=(viewmodel,),
            generated_services=(service,),
            generated_adapters=(adapter,),
            generated_files=generated,
        )

    def _generate_desktop_foundation(
        self,
        project_name: str,
        src_root: Path,
    ) -> tuple[Path, ...]:
        context = {
            "project_name": project_name,
            "class_name": self.to_class_name(project_name),
        }

        template_root = Path("templates") / "desktop"

        app_file = self.write_file(
            src_root / "app.py",
            self.render_template(
                str(template_root / "app.tpl"),
                context,
            ),
        )
        main_window_file = self.write_file(
            src_root / "main_window.py",
            self.render_template(
                str(template_root / "main_window.tpl"),
                context,
            ),
        )
        theme_file = self.write_file(
            src_root / "theme.py",
            self.render_template(
                str(template_root / "theme.tpl"),
                context,
            ),
        )
        main_file = self.write_file(
            src_root / "main.py",
            self._render_main_module(),
        )
        init_file = self.write_file(
            src_root / "__init__.py",
            self._render_package_init(),
        )

        return (
            app_file,
            main_file,
            main_window_file,
            theme_file,
            init_file,
        )

    def _generate_template(
        self,
        output_path: Path,
        template_name: str,
    ) -> Path:
        return self.write_file(
            output_path,
            self.render_template(
                str(
                    Path("templates")
                    / "desktop"
                    / template_name
                ),
                {},
            ),
        )

    @staticmethod
    def _render_main_module() -> str:
        return '''from __future__ import annotations

from desktop.app import create_app


def main() -> int:
    app = create_app()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
'''

    @staticmethod
    def _render_package_init() -> str:
        return '''"""
Kairos Enterprise Desktop package.
"""

from .app import create_app
from .main_window import MainWindow

__all__ = [
    "MainWindow",
    "create_app",
]
'''
