from builder.autonomous.intent_generator import IntentGenerator
from builder.autonomous.architecture_designer import ArchitectureDesigner
from builder.autonomous.full_project_builder import FullProjectBuilder
from builder.autonomous.self_validator import SelfValidator
from builder.autonomous.deployment_simulator import DeploymentSimulator


class FullAutonomousLoop:
    def __init__(self):
        self.intent = IntentGenerator()
        self.designer = ArchitectureDesigner()
        self.builder = FullProjectBuilder()
        self.validator = SelfValidator()
        self.deployer = DeploymentSimulator()

    def run(self) -> dict:
        intent = self.intent.generate()
        architecture = self.designer.design(intent)
        project = self.builder.build(architecture)
        validation = self.validator.validate(project)
        deployment = self.deployer.deploy(project)

        return {
            "intent": intent,
            "architecture": architecture,
            "project": project,
            "validation": validation,
            "deployment": deployment
        }