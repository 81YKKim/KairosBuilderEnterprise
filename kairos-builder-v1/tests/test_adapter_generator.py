from pathlib import Path

from builder.generator.adapter_generator import AdapterGenerator


def test_adapter_generator_creates_adapter_file(tmp_path: Path):
    result = AdapterGenerator().generate("ReplayAdapter", str(tmp_path))

    assert result.exists()
    assert result.name == "replay_adapter.py"
    assert "class ReplayAdapter" in result.read_text(encoding="utf-8")
