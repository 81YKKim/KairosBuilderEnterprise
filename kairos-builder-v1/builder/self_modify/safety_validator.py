class SafetyValidator:
    def validate(self, diff: str) -> bool:
        dangerous_keywords = [
            "rm -rf",
            "os.system",
            "subprocess",
            "eval",
            "exec"
        ]

        for kw in dangerous_keywords:
            if kw in diff:
                return False

        return True