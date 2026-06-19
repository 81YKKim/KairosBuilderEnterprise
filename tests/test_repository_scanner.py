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
    (tests_dir / "test_main.py").write_text("def test_main(): pass", encoding="utf-8")

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
