class CommandMemory:
    def __init__(self):
        self.history = []

    def record(self, command: str, result: str):
        self.history.append({
            "command": command,
            "result": result
        })

    def get_all(self):
        return self.history

    def recent(self, n: int = 10):
        return self.history[-n:]