from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RecommendationTable(QWidget):
    recommendation_selected = Signal(dict)

    HEADERS = (
        "Rank",
        "Symbol",
        "Score",
        "Signal",
        "Status",
    )

    SIGNAL_COLORS = {
        "BUY": QColor("#22C55E"),
        "WATCH": QColor("#F59E0B"),
        "WAIT": QColor("#94A3B8"),
    }

    STATUS_COLORS = {
        "Actionable": QColor("#22C55E"),
        "Monitoring": QColor("#38BDF8"),
        "Pullback": QColor("#F59E0B"),
    }

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("recommendationTable")
        self._recommendations: list[dict[str, object]] = []

        self.table = QTableWidget(
            0,
            len(self.HEADERS),
            self,
        )
        self.table.setObjectName("recommendationTableGrid")
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setShowGrid(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.cellClicked.connect(
            self._handle_cell_clicked
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)

    def set_recommendations(
        self,
        recommendations: list[dict[str, object]],
    ) -> None:
        self._recommendations = sorted(
            recommendations,
            key=self._rank_value,
        )

        self.table.clearContents()
        self.table.setRowCount(len(self._recommendations))

        for row, recommendation in enumerate(
            self._recommendations
        ):
            self._render_row(
                row,
                recommendation,
            )

    def _render_row(
        self,
        row: int,
        recommendation: dict[str, object],
    ) -> None:
        values = (
            recommendation.get("rank", ""),
            recommendation.get("symbol", ""),
            recommendation.get("score", ""),
            recommendation.get("signal", ""),
            recommendation.get("status", ""),
        )

        rank = self._rank_value(recommendation)

        for column, value in enumerate(values):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            if rank == 1:
                self._apply_top_rank_style(item)

            if column == 3:
                self._apply_signal_style(
                    item,
                    str(value),
                )

            if column == 4:
                self._apply_status_style(
                    item,
                    str(value),
                )

            self.table.setItem(
                row,
                column,
                item,
            )

    def _handle_cell_clicked(
        self,
        row: int,
        column: int,
    ) -> None:
        del column

        if row < 0 or row >= len(self._recommendations):
            return

        self.recommendation_selected.emit(
            dict(self._recommendations[row])
        )

    @staticmethod
    def _rank_value(
        recommendation: dict[str, object],
    ) -> int:
        try:
            return int(recommendation.get("rank", 999999))
        except (TypeError, ValueError):
            return 999999

    @staticmethod
    def _apply_top_rank_style(
        item: QTableWidgetItem,
    ) -> None:
        font = QFont(item.font())
        font.setBold(True)

        item.setFont(font)
        item.setBackground(QColor("#172554"))
        item.setForeground(QColor("#FFFFFF"))

    def _apply_signal_style(
        self,
        item: QTableWidgetItem,
        signal: str,
    ) -> None:
        color = self.SIGNAL_COLORS.get(signal.upper())

        if color is None:
            return

        font = QFont(item.font())
        font.setBold(True)

        item.setFont(font)
        item.setForeground(color)

    def _apply_status_style(
        self,
        item: QTableWidgetItem,
        status: str,
    ) -> None:
        color = self.STATUS_COLORS.get(status)

        if color is None:
            return

        font = QFont(item.font())
        font.setBold(True)

        item.setFont(font)
        item.setForeground(color)