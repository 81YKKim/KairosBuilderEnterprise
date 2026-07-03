from __future__ import annotations


class ReplayAdapter:
    name = "ReplayAdapter"

    def load(self) -> dict[str, object]:
        return {
            "adapter": self.name,
            "layer": "desktop.adapter",
            "status": "Market Service Connected",
            "recommendations": [
                {
                    "rank": 1,
                    "symbol": "KAIROS-A",
                    "score": 98.7,
                    "signal": "BUY",
                    "status": "Actionable",
                    "ai_score": 99.2,
                    "entry_timing": "BUY NOW",
                    "evidence": (
                        "Volume acceleration + money flow "
                        "+ AI score velocity confirmed"
                    ),
                },
                {
                    "rank": 2,
                    "symbol": "KAIROS-B",
                    "score": 94.2,
                    "signal": "WATCH",
                    "status": "Monitoring",
                    "ai_score": 95.1,
                    "entry_timing": "SPLIT BUY",
                    "evidence": (
                        "Strong relative volume with "
                        "developing momentum"
                    ),
                },
                {
                    "rank": 3,
                    "symbol": "KAIROS-C",
                    "score": 89.5,
                    "signal": "WAIT",
                    "status": "Pullback",
                    "ai_score": 90.3,
                    "entry_timing": "WAIT PULLBACK",
                    "evidence": (
                        "Opportunity remains valid but "
                        "current price position is extended"
                    ),
                },
                {
                    "rank": 4,
                    "symbol": "KAIROS-D",
                    "score": 78.4,
                    "signal": "WAIT",
                    "status": "Extended",
                    "ai_score": 80.1,
                    "entry_timing": "DO NOT CHASE",
                    "evidence": (
                        "Price extension exceeds safe "
                        "entry timing threshold"
                    ),
                },
            ],
        }