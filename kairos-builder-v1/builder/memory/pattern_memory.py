class PatternMemory:
    def __init__(self):
        self.patterns = {}

    def update(self, command: str, success: bool):
        if command not in self.patterns:
            self.patterns[command] = {"success": 0, "fail": 0}

        if success:
            self.patterns[command]["success"] += 1
        else:
            self.patterns[command]["fail"] += 1

    def get(self):
        return self.patterns