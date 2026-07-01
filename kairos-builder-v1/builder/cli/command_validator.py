class CommandValidator:
    def validate(self, parts: list[str]) -> tuple[bool, str | None]:
        if not parts:
            return False, "EMPTY_COMMAND"

        cmd = parts[0]

        allowed = {
            "new", "generate", "list", "describe",
            "verify", "inspect", "health", "doctor",
            "workflow", "version", "frozen", "stable",
            "sprint", "exit", "quit"
        }

        if cmd not in allowed:
            return False, f"UNKNOWN_COMMAND: {cmd}"

        return True, None