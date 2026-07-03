from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from desktop.main_window import MainWindow
from desktop.theme import DARK_THEME


def create_app() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    app.setApplicationName("{{project_name}}")
    app.setStyleSheet(DARK_THEME)

    main_window = MainWindow()
    main_window.show()

    app.main_window = main_window

    return app