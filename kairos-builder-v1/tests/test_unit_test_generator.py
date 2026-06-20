from pathlib import Path

from builder.generator.unit_test import UnitTestGenerator


def test_unit_test_generator():
    generator = UnitTestGenerator()

    result = generator.generate("order")

    assert "generated:" in result

    text = Path("output/tests/test_order.py").read_text(encoding="utf-8")

    assert "def test_order()" in text
    assert "assert True" in text
