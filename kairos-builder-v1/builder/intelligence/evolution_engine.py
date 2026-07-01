class EvolutionEngine:
    def evolve(self, memory: list[dict]) -> dict:
        if len(memory) < 3:
            return {"mode": "explore"}

        success = sum(1 for m in memory if m.get("success"))

        if success / len(memory) > 0.7:
            return {"mode": "fast_evolution"}

        return {"mode": "stable_learning"}