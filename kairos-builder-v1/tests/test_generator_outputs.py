from builder.generator.domain import DomainGenerator
from builder.generator.service import ServiceGenerator
from builder.generator.unit_test import UnitTestGenerator


def test_all_generators_support_custom_output_root(tmp_path):
    assert DomainGenerator().generate("order", tmp_path).parent == tmp_path
    assert ServiceGenerator().generate("order", tmp_path).parent == tmp_path
    assert UnitTestGenerator().generate("order", tmp_path).parent == tmp_path
