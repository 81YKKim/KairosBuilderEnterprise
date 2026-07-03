from __future__ import annotations

from pathlib import Path


class DesktopStructureValidator:
    REQUIRED_FILES = (
        "__init__.py",
        "app.py",
        "main.py",
        "main_window.py",
        "theme.py",
        "pages/dashboard.py",
        "widgets/sidebar.py",
        "widgets/recommendation_table.py",
        "widgets/recommendation_detail.py",
        "viewmodels/dashboard_view_model.py",
        "services/market_service.py",
        "adapters/replay_adapter.py",
    )

    REQUIRED_SOURCE_MARKERS = {
        "app.py": (
            "QApplication",
            "MainWindow",
        ),
        "main_window.py": (
            "QStackedWidget",
            "Sidebar",
            "Dashboard",
        ),
        "pages/dashboard.py": (
            "DashboardViewModel",
            "_bind_view_model",
            "status_changed.connect",
        ),
        "widgets/sidebar.py": (
            "class Sidebar(QWidget)",
            "dashboard_requested = Signal()",
        ),
        "widgets/recommendation_table.py": (
            "recommendation_selected = Signal(dict)",
            "recommendation_selected.emit",
        ),
        "widgets/recommendation_detail.py": (
            "class RecommendationDetail(QWidget)",
            "ENTRY_TIMING_STYLE_NAMES",
            "ai_score_label",
            "entry_timing_label",
        ),
        "viewmodels/dashboard_view_model.py": (
            "class DashboardViewModel(QObject)",
            "MarketService",
            "Property(str",
            "status_changed = Signal()",
        ),
        "services/market_service.py": (
            "ReplayAdapter",
            "self.adapter.load()",
        ),
        "adapters/replay_adapter.py": (
            "class ReplayAdapter",
            "Market Service Connected",
        ),
        "theme.py": (
            "DARK_THEME",
            "QWidget#sidebar",
            "QLabel#entryTimingDoNotChase",
        ),
    }

    def validate(
        self,
        desktop_root: Path,
    ) -> tuple[Path, ...]:
        root = Path(desktop_root)

        missing_files = self._find_missing_files(root)
        if missing_files:
            missing_text = ", ".join(missing_files)
            raise ValueError(
                "Generated desktop structure is incomplete. "
                f"Missing files: {missing_text}"
            )

        invalid_sources = self._find_invalid_sources(root)
        if invalid_sources:
            invalid_text = ", ".join(invalid_sources)
            raise ValueError(
                "Generated desktop architecture is invalid. "
                f"Missing source markers: {invalid_text}"
            )

        return tuple(
            root / relative_path
            for relative_path in self.REQUIRED_FILES
        )

    def _find_missing_files(
        self,
        desktop_root: Path,
    ) -> tuple[str, ...]:
        return tuple(
            relative_path
            for relative_path in self.REQUIRED_FILES
            if not (
                desktop_root / relative_path
            ).is_file()
        )

    def _find_invalid_sources(
        self,
        desktop_root: Path,
    ) -> tuple[str, ...]:
        invalid: list[str] = []

        for relative_path, markers in (
            self.REQUIRED_SOURCE_MARKERS.items()
        ):
            source = (
                desktop_root / relative_path
            ).read_text(encoding="utf-8")

            for marker in markers:
                if marker not in source:
                    invalid.append(
                        f"{relative_path}:{marker}"
                    )

        return tuple(invalid)