class PortfolioEngine:

    def build(self, ranked_list, total_capital=10000):

        portfolio = []

        if not ranked_list:
            return []

        total_score = sum(item.get("score", 0) for item in ranked_list)

        if total_score <= 0:
            return []

        for item in ranked_list:

            ticker = item.get("ticker", "UNKNOWN")
            score = item.get("score", 0)

            weight = score / total_score
            allocation = round(total_capital * weight, 2)

            # ---------------- SAFE SIGNAL EXTRACTION ----------------
            signal_obj = item.get("signal")
            if isinstance(signal_obj, dict):
                signal_name = signal_obj.get("signal", "UNKNOWN")
            else:
                signal_name = "UNKNOWN"

            # ---------------- SAFE DECISION EXTRACTION ----------------
            decision_obj = item.get("decision")
            if isinstance(decision_obj, dict):
                decision_name = decision_obj.get("action", "NO_TRADE")
            else:
                decision_name = "NO_TRADE"

            portfolio.append({
                "ticker": ticker,
                "allocation": allocation,
                "weight": round(weight * 100, 2),
                "signal": signal_name,
                "decision": decision_name
            })

        return portfolio