from pathlib import Path

from builder.generator.domain import DomainGenerator


def test_domain_generator():
    generator = DomainGenerator()

    result = generator.generate("order")

    assert "generated:" in result

    text = Path("output/domain/order_domain.py").read_text(encoding="utf-8")

    assert "class Order" in text
    assert 'self.name = "order"' in text
