from builder.services.service_generator import ServiceGenerator


def test_generate_service_file(tmp_path):
    generator = ServiceGenerator()

    output_path = generator.generate("UserService", str(tmp_path))

    assert output_path.exists()
    assert output_path.name == "user_service.py"
    assert "class UserService" in output_path.read_text(encoding="utf-8")
