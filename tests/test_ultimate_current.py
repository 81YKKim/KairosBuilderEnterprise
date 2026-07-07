from pathlib import Path

from builder.ultimate.current import CurrentBuilder, CurrentState


def create_sample_repository(root: Path) -> None:
    package = root / "src" / "ultimate" / "domain"
    tests = root / "tests"
    docs = root / "docs"

    package.mkdir(parents=True)
    tests.mkdir()
    docs.mkdir()
    (root / "src" / "ultimate" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "zeta.py").write_text("VALUE = 2\n", encoding="utf-8")
    (package / "alpha.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tests / "test_alpha.py").write_text(
        "def test_alpha():\n    assert True\n",
        encoding="utf-8",
    )
    (docs / "README.md").write_text("# Sample\n", encoding="utf-8")


def test_current_builder_detects_repository_exists(tmp_path):
    repository = tmp_path / "ultimate_repo"
    create_sample_repository(repository)

    state = CurrentBuilder().build(repository)

    assert isinstance(state, CurrentState)
    assert state.repository_path == repository
    assert state.repository_health["exists"] == "true"


def test_current_builder_counts_modules_packages_and_tests(tmp_path):
    repository = tmp_path / "ultimate_repo"
    create_sample_repository(repository)

    state = CurrentBuilder().build(repository)

    assert state.repository_health["python_module_count"] == "2"
    assert state.repository_health["package_count"] == "2"
    assert state.testing_health["test_count"] == "1"
    assert state.implemented_modules == (
        "ultimate.domain.alpha",
        "ultimate.domain.zeta",
    )
    assert state.implemented_packages == (
        "ultimate",
        "ultimate.domain",
    )
    assert state.implemented_tests == (
        "tests/test_alpha.py",
    )


def test_current_builder_summary_returns_required_sections(tmp_path):
    repository = tmp_path / "ultimate_repo"
    create_sample_repository(repository)
    builder = CurrentBuilder()
    builder.build(repository)

    summary = builder.summary()

    assert tuple(summary) == (
        "Repository",
        "Architecture",
        "Tests",
        "Modules",
        "Packages",
        "Release",
    )
    assert summary["Repository"]["exists"] == "true"
    assert summary["Tests"]["test_count"] == "1"
    assert summary["Modules"]["count"] == "2"
    assert summary["Packages"]["count"] == "2"


def test_current_builder_load_sets_current_state(tmp_path):
    repository = tmp_path / "ultimate_repo"
    create_sample_repository(repository)
    state = CurrentBuilder().build(repository)
    builder = CurrentBuilder().load(state)

    assert builder.summary()["Repository"]["path"] == str(repository)


def test_current_builder_returns_deterministic_state(tmp_path):
    repository = tmp_path / "ultimate_repo"
    create_sample_repository(repository)

    first = CurrentBuilder().build(repository)
    second = CurrentBuilder().build(repository)

    assert first.repository_path == second.repository_path
    assert first.repository_health == second.repository_health
    assert first.architecture_health == second.architecture_health
    assert first.testing_health == second.testing_health
    assert first.release_health == second.release_health
    assert first.implemented_features == second.implemented_features
    assert first.implemented_modules == second.implemented_modules
    assert first.implemented_tests == second.implemented_tests
    assert first.implemented_packages == second.implemented_packages
    assert first.metadata["engine"] == "ultimate-current"


def test_current_builder_handles_missing_repository(tmp_path):
    repository = tmp_path / "missing_repo"

    state = CurrentBuilder().build(repository)

    assert state.repository_health["exists"] == "false"
    assert state.repository_health["python_module_count"] == "0"
    assert state.repository_health["package_count"] == "0"
    assert state.testing_health["test_count"] == "0"
