from builder.domain.generation_request import GenerationRequest
from builder.services.generator_service import GeneratorService


def test_generator_creates_file(tmp_path):
    output = tmp_path / "generated" / "sample.md"

    request = GenerationRequest(
        target_type="document",
        name="Sample Document",
        output_path=str(output),
    )

    result = GeneratorService().generate(request)

    assert result.created is True
    assert output.exists()
    assert "Sample Document" in output.read_text(encoding="utf-8")


def test_generator_does_not_overwrite_existing_file(tmp_path):
    output = tmp_path / "existing.md"
    output.write_text("Original Content", encoding="utf-8")

    request = GenerationRequest(
        target_type="document",
        name="Existing Document",
        output_path=str(output),
    )

    result = GeneratorService().generate(request)

    assert result.created is False
    assert output.read_text(encoding="utf-8") == "Original Content"
