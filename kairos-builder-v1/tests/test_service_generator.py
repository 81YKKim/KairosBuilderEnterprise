from pathlib import Path

from builder.generator.service import ServiceGenerator


def test_service_generator():
    generator = ServiceGenerator()

    result = generator.generate("order")

    assert "generated:" in result

    text = Path("output/service/order_service.py").read_text(encoding="utf-8")

    assert "class OrderService" in text
    assert "def execute" in text
