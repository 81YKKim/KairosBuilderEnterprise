from builder.generator.repository_generator import RepositoryGenerator


def test_repository_generator_creates_repository_structure(tmp_path):
    generator = RepositoryGenerator()

    result = generator.generate("sample_project", tmp_path)

    assert result.exists()
    assert (result / "src").exists()
    assert (result / "tests").exists()
    assert (result / "docs").exists()
    assert (result / "README.md").exists()


def test_repository_generator_is_idempotent(tmp_path):
    generator = RepositoryGenerator()

    first = generator.generate("sample_project", tmp_path)
    second = generator.generate("sample_project", tmp_path)

    assert first == second
    assert (second / "README.md").exists()
