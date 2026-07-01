class FeedbackCollector:
    def __init__(self):
        self.logs = []

    def record(self, command: str, success: bool):
        self.logs.append({
            "command": command,
            "success": success
        })

    def history(self):
        return self.logs