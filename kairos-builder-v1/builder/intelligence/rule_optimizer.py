class RuleOptimizer:
    def optimize(self, analysis: dict):
        if analysis["fail_rate"] > 0.3:
            return {"mode": "safe_mode"}

        if analysis["success_rate"] > 0.8:
            return {"mode": "fast_mode"}

        return {"mode": "balanced_mode"}