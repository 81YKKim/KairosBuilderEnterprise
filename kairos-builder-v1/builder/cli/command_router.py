from builder.application.builder_service import BuilderService


class CommandRouter:

    def __init__(self, service=None):
        self.service = service or BuilderService()

    def handle(self, command: str):

        command = command.strip()

        if command == "scan all":
            return self.service.run_full_market_scan()

        if command == "run auto":
            return self.service.execute_top_scan(10000)

        if command == "run live":
            return self.service.start_live(10000)

        if command == "stop":
            return self.service.stop_trading()

        return {"error": f"Unknown command: {command}"}