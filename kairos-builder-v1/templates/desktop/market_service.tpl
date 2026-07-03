from __future__ import annotations

from desktop.adapters.replay_adapter import ReplayAdapter


class MarketService:
    def __init__(
        self,
        adapter: ReplayAdapter | None = None,
    ) -> None:
        self.adapter = adapter or ReplayAdapter()

    def get_market_status(self) -> str:
        data = self.adapter.load()

        return str(
            data.get(
                "status",
                "Unknown",
            )
        )

    def get_recommendations(
        self,
    ) -> list[dict[str, object]]:
        data = self.adapter.load()
        recommendations = data.get("recommendations", [])

        if not isinstance(recommendations, list):
            return []

        return [
            item
            for item in recommendations
            if isinstance(item, dict)
        ]