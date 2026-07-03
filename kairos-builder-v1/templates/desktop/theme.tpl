from __future__ import annotations


DARK_THEME = """
QWidget {
    background-color: #111827;
    color: #F3F4F6;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QMainWindow {
    background-color: #111827;
}

QMenuBar {
    background-color: #0F172A;
    color: #F3F4F6;
    padding: 4px;
}

QMenuBar::item:selected {
    background-color: #1F2937;
}

QMenu {
    background-color: #111827;
    color: #F3F4F6;
    border: 1px solid #374151;
}

QMenu::item:selected {
    background-color: #2563EB;
}

QToolBar {
    background-color: #0F172A;
    border: none;
    spacing: 6px;
    padding: 4px;
}

QStatusBar {
    background-color: #0F172A;
    color: #9CA3AF;
}

QWidget#sidebar {
    background-color: #0F172A;
    border-right: 1px solid #1F2937;
}

QLabel#sidebarTitle {
    color: #F9FAFB;
    font-size: 18pt;
    font-weight: 700;
}

QPushButton#sidebarButton {
    background-color: transparent;
    color: #D1D5DB;
    border: none;
    border-radius: 6px;
    padding: 12px;
    text-align: left;
}

QPushButton#sidebarButton:hover {
    background-color: #1F2937;
    color: #FFFFFF;
}

QPushButton#sidebarButton:pressed {
    background-color: #2563EB;
}

QLabel#desktopTitle {
    color: #F9FAFB;
    font-size: 28pt;
    font-weight: 700;
}

QLabel#desktopSubtitle {
    color: #9CA3AF;
    font-size: 12pt;
}

QLabel#desktopStatus {
    color: #38BDF8;
    font-weight: 600;
}

QWidget#recommendationDetail {
    background-color: #0F172A;
}

QLabel#detailTitle {
    color: #F9FAFB;
    font-size: 14pt;
    font-weight: 700;
}

QLabel#entryTimingDefault {
    color: #F3F4F6;
}

QLabel#entryTimingBuyNow {
    color: #22C55E;
    font-weight: 700;
}

QLabel#entryTimingSplitBuy {
    color: #38BDF8;
    font-weight: 700;
}

QLabel#entryTimingWaitPullback {
    color: #F59E0B;
    font-weight: 700;
}

QLabel#entryTimingDoNotChase {
    color: #EF4444;
    font-weight: 700;
}

QFrame#detailSummaryFrame,
QFrame#detailIntelligenceFrame {
    background-color: #111827;
    border: 1px solid #374151;
    border-radius: 6px;
    padding: 8px;
}

QTableWidget#recommendationTableGrid {
    background-color: #111827;
    alternate-background-color: #111827;
    border: 1px solid #374151;
    border-radius: 6px;
    selection-background-color: #1E3A8A;
    selection-color: #FFFFFF;
}

QTableWidget#recommendationTableGrid::item {
    border-bottom: 1px solid #1F2937;
    padding: 8px;
}

QHeaderView::section {
    background-color: #1F2937;
    color: #F9FAFB;
    border: none;
    border-right: 1px solid #374151;
    border-bottom: 1px solid #374151;
    padding: 10px;
    font-weight: 700;
}
"""