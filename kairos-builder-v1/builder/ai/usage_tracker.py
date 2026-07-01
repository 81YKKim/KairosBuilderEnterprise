from collections import defaultdict


class CommandUsageTracker:
    def __init__(self):
        self.counter = defaultdict(int)

    def record(self, command: str):
        base = command.split()[0]
        self.counter[base] += 1

    def most_used(self):
        if not self.counter:
            return None
        return max(self.counter.items(), key=lambda x: x[1])[0]

    def stats(self):
        return dict(self.counter)