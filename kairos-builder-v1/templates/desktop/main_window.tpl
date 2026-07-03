from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QWidget,
    QHBoxLayout,
)

from desktop.pages.dashboard import Dashboard
from desktop.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("{{project_name}}")
        self.resize(1440, 900)

        self._build_menu_bar()
        self._build_tool_bar()
        self._build_workspace()
        self._build_status_bar()

    def _build_menu_bar(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction("Exit", self.close)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction("Dashboard")

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction("About")

    def _build_tool_bar(self) -> None:
        tool_bar = QToolBar("Main Toolbar", self)
        tool_bar.setMovable(False)
        tool_bar.addAction("Dashboard")

        self.addToolBar(
            Qt.ToolBarArea.TopToolBarArea,
            tool_bar,
        )

    def _build_workspace(self) -> None:
        central_widget = QWidget(self)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(central_widget)
        self.page_stack = QStackedWidget(central_widget)

        self.dashboard = Dashboard(self.page_stack)
        self.page_stack.addWidget(self.dashboard)

        self.sidebar.dashboard_requested.connect(
            self._show_dashboard
        )

        layout.addWidget(self.sidebar)
        layout.addWidget(self.page_stack, 1)

        self.setCentralWidget(central_widget)

    def _show_dashboard(self) -> None:
        self.page_stack.setCurrentWidget(self.dashboard)

    def _build_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        status_bar.showMessage("Kairos Desktop Ready")

        self.setStatusBar(status_bar)