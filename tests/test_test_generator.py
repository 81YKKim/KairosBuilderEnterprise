from builder.services.test_generator import TestGenerator


def test_generate_test_file(tmp_path):
    generator = TestGenerator()

    output_path = generator.generate("UserService", str(tmp_path))

    assert output_path.exists()
    assert output_path.name == "test_user_service.py"
    assert "def test_userservice()" in output_path.read_text(encoding="utf-8")
