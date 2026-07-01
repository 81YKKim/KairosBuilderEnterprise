from pathlib import Path

from builder.application.project_generator import ProjectGenerator


def test_project_generator_creates_full_structure(tmp_path: Path):
    generator = ProjectGenerator()

    result = generator.generate("KairosDesktop", str(tmp_path))

    assert (result / "src").exists()
    assert (result / "tests").exists()
    assert (result / "docs").exists()
    assert (result / "resources").exists()
    assert (result / "data").exists()

    assert (result / "README.md").exists()
    assert (result / "pyproject.toml").exists()
    assert (result / ".gitignore").exists()