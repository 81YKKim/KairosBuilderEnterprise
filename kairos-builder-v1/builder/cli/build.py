"""
Build CLI
Sprint #000033
"""

from builder.workflow.production_pipeline import ProductionPipeline


def build():
    ProductionPipeline().run()
