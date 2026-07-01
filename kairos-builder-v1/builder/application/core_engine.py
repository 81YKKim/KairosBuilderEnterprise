class CoreSignalEngine:

    def detect(self, money_flow):

        score = money_flow.get("score", 0)

        if score >= 80:
            signal = "EXPLOSIVE_BREAKOUT"
            strength = 100

        elif score >= 60:
            signal = "STRONG_MOMENTUM"
            strength = 80

        elif score >= 40:
            signal = "ACCUMULATION"
            strength = 60

        elif score >= 20:
            signal = "EARLY_SIGNAL"
            strength = 40

        else:
            signal = "IGNORE"
            strength = 10

        return {
            "signal": signal,
            "flow_score": score,   # 🔥 중요 (score 보호)
            "strength": strength
        }


class CoreDecisionEngine:

    def decide(self, signal, context=None):

        score = signal.get("flow_score", 0)  # 🔥 FIX
        strength = signal.get("strength", 0)

        total = score + (strength * 0.5)

        if total >= 90:
            action = "FULL_BUY"

        elif total >= 70:
            action = "PARTIAL_BUY"

        elif total >= 50:
            action = "WATCH"

        else:
            action = "NO_TRADE"

        return {
            "action": action,
            "raw_score": score,
            "final_score": total,
            "confidence": min(100, total)
        }