from datetime import datetime


class CLILogger:
    def log(self, level: str, message: str):
        return {
            "time": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
        }