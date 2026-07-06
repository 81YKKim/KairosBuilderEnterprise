from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):
    dashboard_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)

        title = QLabel("KAIROS")
        title.setObjectName("sidebarTitle")

        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setObjectName("sidebarButton")
        self.dashboard_button.clicked.connect(
            self.dashboard_requested.emit
        )

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.dashboard_button)
        layout.addStretch()