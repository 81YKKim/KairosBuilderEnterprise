from concurrent.futures import ThreadPoolExecutor, as_completed


class UniverseScanner:

    def scan_all(self, universe, market_engine, flow_engine):

        results = []

        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [
                executor.submit(self._scan_one, t, market_engine, flow_engine)
                for t in universe
            ]

            for f in as_completed(futures):

                result = f.result()

                if result:
                    results.append(result)

        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    def _scan_one(self, ticker, market_engine, flow_engine):

        data = market_engine.get_stock_data(ticker)

        if not data:
            return None

        flow = flow_engine.analyze(data)
        score = flow.get("score", 0)

        if score >= 80:
            signal = "EXPLOSIVE_BREAKOUT"
        elif score >= 60:
            signal = "STRONG_MOMENTUM"
        elif score >= 40:
            signal = "ACCUMULATION"
        elif score >= 20:
            signal = "EARLY_SIGNAL"
        else:
            signal = "IGNORE"

        return {
            "ticker": ticker,
            "score": score,
            "signal": signal
        }