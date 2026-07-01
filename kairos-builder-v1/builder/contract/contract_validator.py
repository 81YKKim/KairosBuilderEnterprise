class ContractValidator:
    def validate_prefix(self, contract, value: str) -> bool:
        if not contract:
            return True
        prefix = contract.get("prefix")
        if prefix:
            return value.startswith(prefix)
        return True