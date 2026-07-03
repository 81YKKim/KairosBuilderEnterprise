from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from desktop.viewmodels.dashboard_view_model import DashboardViewModel
from desktop.widgets.recommendation_detail import RecommendationDetail
from desktop.widgets.recommendation_table import RecommendationTable


class Dashboard(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        view_model: DashboardViewModel | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("dashboard")

        self.view_model = view_model or DashboardViewModel(self)

        self.title_label = QLabel()
        self.title_label.setObjectName("desktopTitle")
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("desktopSubtitle")
        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label = QLabel()
        self.status_label.setObjectName("desktopStatus")
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.recommendation_table = RecommendationTable(self)
        self.recommendation_detail = RecommendationDetail(self)

        splitter = QSplitter(
            Qt.Orientation.Horizontal,
            self,
        )
        splitter.addWidget(self.recommendation_table)
        splitter.addWidget(self.recommendation_detail)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.status_label)
        layout.addWidget(splitter, 1)

        self._bind_view_model()
        self._refresh()

    def _bind_view_model(self) -> None:
        self.view_model.title_changed.connect(
            self._refresh_title
        )
        self.view_model.subtitle_changed.connect(
            self._refresh_subtitle
        )
        self.view_model.status_changed.connect(
            self._refresh_status
        )
        self.view_model.recommendations_changed.connect(
            self._refresh_recommendations
        )
        self.recommendation_table.recommendation_selected.connect(
            self.recommendation_detail.set_recommendation
        )

    def _refresh(self) -> None:
        self._refresh_title()
        self._refresh_subtitle()
        self._refresh_status()
        self._refresh_recommendations()

    def _refresh_title(self) -> None:
        self.title_label.setText(
            self.view_model.title
        )

    def _refresh_subtitle(self) -> None:
        self.subtitle_label.setText(
            self.view_model.subtitle
        )

    def _refresh_status(self) -> None:
        self.status_label.setText(
            f"Status: {self.view_model.status}"
        )

    def _refresh_recommendations(self) -> None:
        self.recommendation_table.set_recommendations(
            self.view_model.recommendations
        )