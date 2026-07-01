from builder.workflow.production_pipeline import ProductionPipeline


def test_pipeline_exists():
    pipeline = ProductionPipeline()
    assert pipeline is not None


def test_pipeline_has_run():
    assert hasattr(ProductionPipeline(), "run")


def test_pipeline_run_returns_none():
    pipeline = ProductionPipeline()

    assert pipeline.run() is not None
