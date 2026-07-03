from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal

from desktop.services.market_service import MarketService


class DashboardViewModel(QObject):
    title_changed = Signal()
    subtitle_changed = Signal()
    status_changed = Signal()
    recommendations_changed = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
        market_service: MarketService | None = None,
    ) -> None:
        super().__init__(parent)

        self.market_service = market_service or MarketService()

        self._title = "Kairos Dashboard"
        self._subtitle = "Enterprise MVVM Desktop"
        self._status = "Ready"
        self._recommendations: list[dict[str, object]] = []

        self.refresh()

    @Property(str, notify=title_changed)
    def title(self) -> str:
        return self._title

    @Property(str, notify=subtitle_changed)
    def subtitle(self) -> str:
        return self._subtitle

    @Property(str, notify=status_changed)
    def status(self) -> str:
        return self._status

    @property
    def recommendations(
        self,
    ) -> list[dict[str, object]]:
        return list(self._recommendations)

    def set_status(self, value: str) -> None:
        if self._status == value:
            return

        self._status = value
        self.status_changed.emit()

    def set_recommendations(
        self,
        value: list[dict[str, object]],
    ) -> None:
        if self._recommendations == value:
            return

        self._recommendations = list(value)
        self.recommendations_changed.emit()

    def refresh(self) -> None:
        self.set_status(
            self.market_service.get_market_status()
        )
        self.set_recommendations(
            self.market_service.get_recommendations()
        )