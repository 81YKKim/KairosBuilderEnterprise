class MoneyFlowEngine:

    def analyze(self, data):

        price = data.get("price_change", 0)
        volume = data.get("volume_ratio", 0)
        volatility = data.get("volatility", 0)

        score = 0

        # ---------------- VOLUME ----------------
        if volume >= 5:
            score += 40
        elif volume >= 3:
            score += 25
        elif volume >= 1:
            score += 10

        # ---------------- PRICE ----------------
        if price >= 5:
            score += 30
        elif price >= 2:
            score += 15
        elif price > 0:
            score += 5

        # ---------------- VOLATILITY ----------------
        if volatility >= 3:
            score += 10
        elif volatility >= 1:
            score += 5

        # ---------------- FLOW CLASS ----------------
        if score >= 70:
            flow = "STRONG_INFLOW"

        elif score >= 40:
            flow = "ACCUMULATION"

        elif score >= 20:
            flow = "WEAK_FLOW"

        else:
            flow = "NO_FLOW"

        return {
            "flow": flow,
            "score": score
        }