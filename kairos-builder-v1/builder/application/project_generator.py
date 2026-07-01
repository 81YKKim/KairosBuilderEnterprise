from builder.template.template_registry import TemplateRegistry
from builder.template.schema_validator import SchemaValidator
from builder.template.template_engine import TemplateEngine


class ProjectGenerator:
    def __init__(self):
        self.registry = TemplateRegistry()
        self.validator = SchemaValidator()
        self.engine = TemplateEngine(self.registry, self.validator)

    def generate(self, name: str, output_root: str = "output/projects"):
        return self.engine.render("project", "v1", output_root)