from builder.autonomous.task_generator import TaskGenerator
from builder.autonomous.priority_engine import PriorityEngine
from builder.autonomous.execution_engine import ExecutionEngine
from builder.autonomous.feedback_engine import FeedbackEngine


class AutonomousLoop:
    def __init__(self):
        self.generator = TaskGenerator()
        self.priority = PriorityEngine()
        self.executor = ExecutionEngine()
        self.feedback = FeedbackEngine()

    def run(self):
        tasks = self.generator.generate()
        ranked = self.priority.rank(tasks)

        results = []
        for task in ranked:
            result = self.executor.execute(task)
            results.append({
                "result": result,
                "feedback": self.feedback.analyze(result)
            })

        return {
            "tasks": tasks,
            "ranked": ranked,
            "results": results
        }