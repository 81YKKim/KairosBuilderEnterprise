from pathlib import Path

from builder.repository.change_analyzer import RepositoryChangeAnalyzer
from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder
from builder.repository.qa import RepositoryQA
from builder.repository.query import RepositoryQuery


def build_analyzer(repository: Path) -> RepositoryChangeAnalyzer:
    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)
    intelligence = RepositoryIntelligence(
        inventory=inventory,
        graph=graph,
    )
    query = RepositoryQuery(intelligence=intelligence)
    qa = RepositoryQA(
        intelligence=intelligence,
        query=query,
    )

    return RepositoryChangeAnalyzer(
        intelligence=intelligence,
        query=query,
        qa=qa,
    )


def test_change_analyzer_classifies_changed_files(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")

    analyzer = build_analyzer(repository)
    change_set = analyzer.analyze_files(
        (
            "README.md",
            "src/sample/module.py",
            "tests/test_module.py",
        )
    )

    assert change_set.changed_files == (
        Path("README.md"),
        Path("src/sample/module.py"),
        Path("tests/test_module.py"),
    )
    assert change_set.changed_python_files == (
        Path("src/sample/module.py"),
        Path("tests/test_module.py"),
    )
    assert change_set.changed_test_files == (
        Path("tests/test_module.py"),
    )
    assert [package.name for package in change_set.changed_packages] == [
        "sample",
    ]
    assert [module.name for module in change_set.changed_modules] == [
        "sample.module",
        "tests.test_module",
    ]


def test_change_analyzer_detects_affected_tests_and_modules(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (source / "beta.py").write_text("", encoding="utf-8")
    (tests / "test_alpha.py").write_text("", encoding="utf-8")
    (tests / "test_beta.py").write_text("", encoding="utf-8")

    analyzer = build_analyzer(repository)

    assert [module.name for module in analyzer.affected_modules(("src/sample/alpha.py",))] == [
        "sample.alpha",
    ]
    assert [test.path for test in analyzer.affected_tests(("src/sample/alpha.py",))] == [
        Path("tests/test_alpha.py")
    ]


def test_change_analyzer_reports_change_impact_and_risk(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "covered.py").write_text("", encoding="utf-8")
    (source / "uncovered.py").write_text("", encoding="utf-8")

    analyzer = build_analyzer(repository)
    impact = analyzer.analyze_files(
        (
            "src/sample/covered.py",
            "src/sample/uncovered.py",
        )
    )

    assert [package.name for package in impact.impact.affected_packages] == [
        "sample",
    ]
    assert [module.name for module in impact.impact.affected_modules] == [
        "sample.covered",
        "sample.uncovered",
    ]
    assert impact.impact.affected_tests == ()
    assert impact.impact.qa_required is True
    assert impact.impact.risk_level == "high"
    assert analyzer.risk_level(("src/sample/covered.py",)) == "medium"
    assert analyzer.risk_level(("README.md",)) == "low"


def test_change_analyzer_parses_git_status_lines(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")

    analyzer = build_analyzer(repository)
    analysis = analyzer.analyze_git_status(
        (
            " M src/sample/module.py",
            "?? tests/test_module.py",
            "R  old.py -> src/sample/module.py",
        )
    )

    assert analysis.changed_files == (
        Path("src/sample/module.py"),
        Path("tests/test_module.py"),
    )


def test_change_analyzer_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")

    analyzer = build_analyzer(repository)
    analysis = analyzer.analyze_files(
        (
            "src/sample/zeta.py",
            "src/sample/alpha.py",
        )
    )

    assert analysis.changed_files == (
        Path("src/sample/alpha.py"),
        Path("src/sample/zeta.py"),
    )
    assert [module.name for module in analysis.changed_modules] == [
        "sample.alpha",
        "sample.zeta",
    ]
