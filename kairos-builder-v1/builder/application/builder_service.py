from builder.plugins.market_data_engine import MarketDataEngine
from builder.plugins.money_flow_engine import MoneyFlowEngine
from builder.plugins.universe_scanner import UniverseScanner
from builder.plugins.universe_provider import UniverseProvider

from builder.execution.execution_engine import ExecutionEngine


class BuilderService:

    def __init__(self, context=None):

        self.context = context

        self.market = MarketDataEngine()
        self.flow = MoneyFlowEngine()
        self.scanner = UniverseScanner()
        self.universe = UniverseProvider()

        self.executor = ExecutionEngine()

    # -----------------------------
    # FULL MARKET SCAN
    # -----------------------------
    def run_full_market_scan(self):

        universe = self.universe.get_all_us_stocks()

        ranked = self.scanner.scan_all(
            universe,
            self.market,
            self.flow
        )

        return ranked[:20]

    # -----------------------------
    # AUTO TRADE
    # -----------------------------
    def execute_top_scan(self, capital=10000):

        universe = self.universe.get_all_us_stocks()

        ranked = self.scanner.scan_all(
            universe,
            self.market,
            self.flow
        )

        filtered = ranked[:10]

        adjusted = []
        total = sum(x["score"] for x in filtered) or 1

        for x in filtered:

            weight = x["score"] / total
            allocation = capital * weight

            adjusted.append({
                "ticker": x["ticker"],
                "score": x["score"],
                "signal": x["signal"],
                "allocation": allocation
            })

        return self.executor.execute_top(adjusted, capital)