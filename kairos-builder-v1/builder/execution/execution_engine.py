class ExecutionEngine:

    def __init__(self, broker=None):
        self.broker = broker

    def execute_top(self, positions, capital=10000):

        results = []

        for p in positions:

            ticker = p["ticker"]
            allocation = p["allocation"]
            score = p["score"]
            signal = p["signal"]

            # 🔥 EXECUTE 조건 완전 완화
            if score >= 35:

                qty = max(1, int(allocation / 100))

                order = self._send_order(ticker, qty)

                results.append({
                    "ticker": ticker,
                    "status": "EXECUTED",
                    "qty": qty,
                    "allocation": allocation,
                    "signal": signal,
                    "result": order
                })

            else:

                results.append({
                    "ticker": ticker,
                    "status": "SKIPPED",
                    "score": score
                })

        return results

    def _send_order(self, ticker, qty):

        if self.broker:
            return self.broker.buy(ticker, qty)

        return {
            "order_id": f"MOCK-{ticker}",
            "status": "SUCCESS",
            "qty": qty
        }