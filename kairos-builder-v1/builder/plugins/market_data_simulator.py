import random


class MarketDataSimulator:

    def generate(self):
        """
        실제 시장 데이터처럼 보이는 랜덤 시뮬레이션
        """

        return {
            "price_change": round(random.uniform(-5, 15), 2),
            "volume_ratio": round(random.uniform(0.5, 6), 2),
            "market_cap": random.randint(300_000_000, 5_000_000_000),
            "volatility": round(random.uniform(0.5, 5), 2)
        }