class PriorityEngine:
    def rank(self, tasks: list) -> list:
        return sorted(tasks, key=lambda x: x["priority"])