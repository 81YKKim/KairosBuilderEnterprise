class PluginBase:
    name: str = "base"

    def execute(self, context: dict):
        raise NotImplementedError