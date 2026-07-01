class DecisionEngine:
    def decide(self, command: str) -> dict:
        cmd = command.split()[0]

        rules = {
            "new": ("create_project", 0.2),
            "generate": ("generate_code", 0.3),
            "verify": ("run_tests", 0.4),
            "dispatch": ("distributed_task", 0.6),
            "dispatch cloud": ("remote_task", 0.8),
        }

        action, risk = rules.get(cmd, ("unknown", 1.0))

        return {
            "command": cmd,
            "action": action,
            "risk": risk
        }