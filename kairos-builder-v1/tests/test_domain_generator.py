from builder.generator.domain import DomainGenerator


def test_domain_generator():
    generator = DomainGenerator()

    result = generator.generate("order")

    assert result.exists()
    assert result.name == "order_domain.py"
