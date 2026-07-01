from builder.generator.registry import default_registry


class Factory:
    def __init__(self, registry=None):
        self.registry = registry or default_registry()

    def create(self, name):
        return self.registry.create(name)
