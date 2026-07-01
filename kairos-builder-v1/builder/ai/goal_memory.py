class GoalMemory:
    def __init__(self):
        self.goal = None
        self.history = []

    def set_goal(self, goal: str):
        self.goal = goal

    def get_goal(self):
        return self.goal

    def log(self, step: str):
        self.history.append(step)

    def trace(self):
        return self.history[-10:]