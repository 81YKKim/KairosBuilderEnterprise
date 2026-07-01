"""
Production Build Pipeline
Sprint #000033
"""

from builder.generator.registry import GeneratorRegistry


class ProductionPipeline:
    """Production build pipeline."""

    def run(self):
        registry = GeneratorRegistry()

        return registry
