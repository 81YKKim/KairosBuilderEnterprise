class ExecutionChain:
    def build_chain(self, tasks: list[str]) -> list[str]:
        return [f"EXEC:{task}" for task in tasks]

    def optimize(self, chain: list[str]) -> list[str]:
        seen = set()
        optimized = []

        for c in chain:
            if c not in seen:
                optimized.append(c)
                seen.add(c)

        return optimized