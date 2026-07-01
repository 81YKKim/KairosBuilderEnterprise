class RecallEngine:
    def recall(self, memory, command: str):
        matches = [
            m for m in memory.get_all()
            if command in m["command"]
        ]

        return matches[-5:]