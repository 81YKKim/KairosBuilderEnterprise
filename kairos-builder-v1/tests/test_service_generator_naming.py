from pathlib import Path

from builder.generator.service import ServiceGenerator


def test_service_generator_preserves_camel_case_class_name(
    tmp_path: Path,
):
    result = ServiceGenerator().generate(
        "LiveRuntime",
        str(tmp_path),
    )

    source = result.read_text(encoding="utf-8")

    assert result.name == "live_runtime_service.py"
    assert "class LiveRuntimeService" in source
