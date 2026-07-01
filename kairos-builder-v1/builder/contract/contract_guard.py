class ContractGuard:
    def __init__(self, registry):
        self.registry = registry

    def check(self, name: str, value):
        contract = self.registry.get(name)
        return contract, value