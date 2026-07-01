from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from builder.generator.adapter_generator import AdapterGenerator
from builder.generator.composite_generator import CompositeGenerator
from builder.generator.desktop_generator_result import DesktopGeneratorResult
from builder.generator.page_generator import PageGenerator
from builder.generator.service import ServiceGenerator
from builder.generator.viewmodel_generator import ViewModelGenerator
from builder.generator.widget_generator import WidgetGenerator
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
                tests_root,
            ]
        )

        page = self.run_generator(
            PageGenerator(),
            "Dashboard",
            src_root / "pages",
        )

        widget = self.run_generator(
            WidgetGenerator(),
            "RecommendationTable",
            src_root / "widgets",
        )

        viewmodel = self.run_generator(
            ViewModelGenerator(),
            "DashboardViewModel",
            src_root / "viewmodels",
        )

        service = self.run_generator(
            ServiceGenerator(),
            "Market",
            src_root / "services",
        )

        adapter = self.run_generator(
            AdapterGenerator(),
            "ReplayAdapter",
            src_root / "adapters",
        )

        generated = self.collect_results(
            page,
            widget,
            viewmodel,
            service,
            adapter,
        )

        manifest = DesktopManifest(
            project_name=name,
            builder_version="2.0.0-alpha",
            generator="DesktopGenerator",
            architecture="MVVM",
            created_at=datetime.now(UTC).isoformat(),
            pages=1,
            widgets=1,
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
            generated_widgets=(widget,),
            generated_viewmodels=(viewmodel,),
            generated_services=(service,),
            generated_adapters=(adapter,),
            generated_files=generated,
        )