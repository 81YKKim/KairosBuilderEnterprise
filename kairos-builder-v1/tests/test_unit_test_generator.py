from builder.generator.unit_test import UnitTestGenerator


def test_unit_test_generator():
    generator = UnitTestGenerator()

    result = generator.generate("order")

    assert result.exists()
    assert result.name == "test_order.py"
