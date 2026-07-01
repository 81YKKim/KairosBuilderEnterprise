from builder.generator.project_generator import ProjectGenerator


def test_project_generator_creates_project_structure(tmp_path):
    generator = ProjectGenerator()

    result = generator.generate("sample_project", tmp_path)

    assert result.exists()
    assert (result / "src").exists()
    assert (result / "tests").exists()
    assert (result / "docs").exists()
    assert (result / "README.md").exists()


def test_project_generator_is_idempotent(tmp_path):
    generator = ProjectGenerator()

    first = generator.generate("sample_project", tmp_path)
    second = generator.generate("sample_project", tmp_path)

    assert first == second
    assert (second / "README.md").exists()
