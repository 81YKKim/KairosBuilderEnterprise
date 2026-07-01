from builder.generator.service import ServiceGenerator


def test_service_generator():
    generator = ServiceGenerator()

    result = generator.generate("order")

    assert result.exists()
    assert result.name == "order_service.py"
