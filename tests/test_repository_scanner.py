from pathlib import Path

from builder.repository.scanner import RepositoryScanner as IntelligenceScanner
from builder.services.repository_scanner import RepositoryScanner


def test_repository_scanner_detects_python_project(tmp_path):
    project_dir = tmp_path / "sample_project"
    src_dir = project_dir / "src"
    tests_dir = project_dir / "tests"

    src_dir.mkdir(parents=True)
    tests_dir.mkdir(parents=True)

    (project_dir / "pyproject.toml").write_text("", encoding="utf-8")
    (project_dir / "builder.manifest.json").write_text(
        '{"architecture": "Enterprise"}',
        encoding="utf-8",
    )
    (project_dir / ".git").mkdir()

    (src_dir / "main.py").write_text("print('hello')", encoding="utf-8")
    (tests_dir / "test_main.py").write_text(
        "def test_main(): pass",
        encoding="utf-8",
    )

    scanner = RepositoryScanner()
    info = scanner.scan(str(project_dir))

    assert info.name == "sample_project"
    assert info.language == "Python"
    assert info.architecture == "Enterprise"
    assert info.manifest_found is True
    assert info.git_found is True
    assert info.source_files == 1
    assert info.test_files == 1
    assert info.directories >= 3


def test_repository_scanner_handles_unknown_project(tmp_path):
    project_dir = tmp_path / "unknown_project"
    project_dir.mkdir()

    scanner = RepositoryScanner()
    info = scanner.scan(str(project_dir))

    assert info.name == "unknown_project"
    assert info.language == "Unknown"
    assert info.architecture == "Unknown"
    assert info.manifest_found is False
    assert info.git_found is False
    assert info.branch == "Unknown"


def test_intelligence_scanner_detects_python_modules_packages_and_tests(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"
    tests = repository / "tests"
    docs = repository / "docs"

    package.mkdir(parents=True)
    tests.mkdir(parents=True)
    docs.mkdir(parents=True)

    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "model.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tests / "test_model.py").write_text(
        "def test_model():\n    assert True\n",
        encoding="utf-8",
    )
    (docs / "README.md").write_text("# Docs\n", encoding="utf-8")
    (repository / "pyproject.toml").write_text(
        "[project]\nname = 'sample'\n",
        encoding="utf-8",
    )

    result = IntelligenceScanner().scan(
        repository,
        git_root=repository,
        branch="main",
        head_commit="abc123",
    )

    assert Path("src/sample/domain/model.py") in result.python_files
    assert Path("pyproject.toml") in result.files
    assert Path("src/sample/domain/model.py") in result.files
    assert Path("src/sample/domain") in result.directories
    assert result.model.repository_root == repository
    assert result.model.git_root == repository
    assert result.model.branch == "main"
    assert result.model.head_commit == "abc123"
    assert result.model.python_modules[0].name == "sample.domain.model"
    assert [package.name for package in result.model.packages] == [
        "sample",
        "sample.domain",
    ]
    assert result.model.tests[0].path == Path("tests/test_model.py")
    assert result.model.documentation[0].path == Path("docs/README.md")
    assert result.model.statistics.python_file_count == 4
    assert result.model.statistics.test_file_count == 1
    assert result.model.statistics.documentation_file_count == 1


def test_intelligence_scanner_ignores_hidden_and_cache_directories(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "visible.py").write_text("VALUE = 1\n", encoding="utf-8")

    ignored_directories = (
        ".git",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "__pycache__",
        ".hidden",
    )

    for directory_name in ignored_directories:
        directory = repository / directory_name
        directory.mkdir()
        (directory / "ignored.py").write_text(
            "IGNORED = True\n",
            encoding="utf-8",
        )

    result = IntelligenceScanner().scan(repository)

    assert Path("src/sample/visible.py") in result.python_files
    assert all(
        Path(directory_name, "ignored.py") not in result.files
        for directory_name in ignored_directories
    )
    assert all(
        Path(directory_name) not in result.directories
        for directory_name in ignored_directories
    )
    assert result.model.statistics.python_file_count == 2


def test_intelligence_scanner_returns_deterministic_sorted_results(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    source.mkdir(parents=True)

    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")

    result = IntelligenceScanner().scan(repository)

    assert result.files == tuple(
        sorted(result.files, key=lambda path: path.as_posix())
    )
    assert result.directories == tuple(
        sorted(result.directories, key=lambda path: path.as_posix())
    )
    assert result.python_files == tuple(
        sorted(result.python_files, key=lambda path: path.as_posix())
    )
    assert [module.name for module in result.model.python_modules] == [
        "sample.alpha",
        "sample.zeta",
    ]
