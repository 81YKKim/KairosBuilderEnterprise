from pathlib import Path


class KairosFactory:

    def create_signal_engine(self, output_root: str):
        base = Path(output_root) / "signal_engine"
        base.mkdir(parents=True, exist_ok=True)

        (base / "__init__.py").write_text("")

        (base / "engine.py").write_text("""
class SignalEngine:

    def detect(self, money_flow):
        flow = money_flow.get("flow")
        score = money_flow.get("score", 0)

        # ---------------- FIXED FLOW LOGIC ----------------
        if flow == "STRONG_INFLOW":
            signal = "EXPLOSIVE_BREAKOUT"
            strength = 95
        elif flow == "ACCUMULATION":
            signal = "EARLY_MOMENTUM"
            strength = 75
        elif flow == "WEAK_FLOW":
            signal = "WATCH"
            strength = 50
        else:
            signal = "IGNORE"
            strength = 10

        return {
            "signal": signal,
            "strength": strength,
            "flow_score": score
        }
""")

        return base