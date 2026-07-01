from builder.plugin.plugin_base import PluginBase


class PluginRegistry:
    def __init__(self):
        self.plugins: dict[str, PluginBase] = {}

    def register(self, plugin: PluginBase):
        self.plugins[plugin.name] = plugin

    def get(self, name: str):
        return self.plugins.get(name)

    def list(self):
        return list(self.plugins.keys())