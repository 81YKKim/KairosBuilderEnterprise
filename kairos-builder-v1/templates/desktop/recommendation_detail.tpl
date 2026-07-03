from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class RecommendationDetail(QWidget):
    ENTRY_TIMING_STYLE_NAMES = {
        "BUY NOW": "entryTimingBuyNow",
        "SPLIT BUY": "entryTimingSplitBuy",
        "WAIT PULLBACK": "entryTimingWaitPullback",
        "DO NOT CHASE": "entryTimingDoNotChase",
    }

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("recommendationDetail")

        self.title_label = QLabel("Recommendation Detail")
        self.title_label.setObjectName("detailTitle")

        self.symbol_label = QLabel("-")
        self.score_label = QLabel("-")
        self.signal_label = QLabel("-")
        self.status_label = QLabel("-")
        self.ai_score_label = QLabel("-")

        self.entry_timing_label = QLabel("-")
        self.entry_timing_label.setObjectName("entryTimingDefault")

        self.evidence_label = QLabel("-")
        self.evidence_label.setWordWrap(True)

        summary_frame = QFrame(self)
        summary_frame.setObjectName("detailSummaryFrame")

        summary_layout = QFormLayout(summary_frame)
        summary_layout.addRow("Symbol", self.symbol_label)
        summary_layout.addRow("Score", self.score_label)
        summary_layout.addRow("Signal", self.signal_label)
        summary_layout.addRow("Status", self.status_label)

        intelligence_frame = QFrame(self)
        intelligence_frame.setObjectName("detailIntelligenceFrame")

        intelligence_layout = QFormLayout(intelligence_frame)
        intelligence_layout.addRow("AI Score", self.ai_score_label)
        intelligence_layout.addRow(
            "Entry Timing",
            self.entry_timing_label,
        )
        intelligence_layout.addRow(
            "Evidence",
            self.evidence_label,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        layout.addWidget(self.title_label)
        layout.addWidget(summary_frame)
        layout.addWidget(intelligence_frame)
        layout.addStretch()

    def set_recommendation(
        self,
        recommendation: dict[str, object] | None,
    ) -> None:
        if recommendation is None:
            self.clear()
            return

        self.symbol_label.setText(
            str(recommendation.get("symbol", "-"))
        )
        self.score_label.setText(
            str(recommendation.get("score", "-"))
        )
        self.signal_label.setText(
            str(recommendation.get("signal", "-"))
        )
        self.status_label.setText(
            str(recommendation.get("status", "-"))
        )
        self.ai_score_label.setText(
            str(recommendation.get("ai_score", "-"))
        )

        entry_timing = str(
            recommendation.get("entry_timing", "-")
        )

        self.entry_timing_label.setText(entry_timing)
        self._apply_entry_timing_style(entry_timing)

        self.evidence_label.setText(
            str(recommendation.get("evidence", "-"))
        )

    def clear(self) -> None:
        self.symbol_label.setText("-")
        self.score_label.setText("-")
        self.signal_label.setText("-")
        self.status_label.setText("-")
        self.ai_score_label.setText("-")
        self.entry_timing_label.setText("-")
        self.evidence_label.setText("-")

        self._apply_entry_timing_style("-")

    def _apply_entry_timing_style(
        self,
        entry_timing: str,
    ) -> None:
        style_name = self.ENTRY_TIMING_STYLE_NAMES.get(
            entry_timing.upper(),
            "entryTimingDefault",
        )

        self.entry_timing_label.setObjectName(style_name)
        self.entry_timing_label.style().unpolish(
            self.entry_timing_label
        )
        self.entry_timing_label.style().polish(
            self.entry_timing_label
        )

        font = self.entry_timing_label.font()
        font.setBold(entry_timing.upper() == "BUY NOW")
        self.entry_timing_label.setFont(font)