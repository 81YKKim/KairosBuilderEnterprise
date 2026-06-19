from builder.services.cli_generator import CLIGenerator


def test_generate_cli_file(tmp_path):
    generator = CLIGenerator()

    output_path = generator.generate("MainCLI", str(tmp_path))

    assert output_path.exists()
    assert output_path.name == "main_c_l_i.py"
    assert "def main()" in output_path.read_text(encoding="utf-8")
