class ContextMemory:
    def __init__(self, max_size: int = 10):
        self.history = []
        self.max_size = max_size

    def add(self, command: str):
        self.history.append(command)
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def recent(self):
        return self.history[-5:]

    def last(self):
        return self.history[-1] if self.history else None