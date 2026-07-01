class SchemaValidator:
    def validate(self, template: dict) -> bool:
        required_keys = ["structure", "files"]
        return all(k in template for k in required_keys)