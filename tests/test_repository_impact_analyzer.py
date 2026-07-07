from dataclasses import dataclass
from pathlib import Path

from builder.repository.change_analyzer import RepositoryChangeAnalyzer
from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.impact_analyzer import RepositoryImpactAnalyzer
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder
from builder.repository.qa import QAIssue, RepositoryQA
from builder.repository.query import RepositoryQuery


def build_impact_analyzer(repository: Path) -> RepositoryImpactAnalyzer:
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
    change_analyzer = RepositoryChangeAnalyzer(
        intelligence=intelligence,
        query=query,
        qa=qa,
    )

    return RepositoryImpactAnalyzer(
        intelligence=intelligence,
        query=query,
        qa=qa,
        change_analyzer=change_analyzer,
    )


def test_impact_analyzer_creates_impact_scope(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("README.md", "src/sample/module.py"))

    assert scope.source_files == (
        Path("README.md"),
        Path("src/sample/module.py"),
    )
    assert [module.name for module in scope.changed_modules] == [
        "sample.module",
    ]
    assert [module.name for module in scope.affected_modules] == [
        "sample.module",
    ]
    assert [package.name for package in scope.affected_packages] == [
        "sample",
    ]
    assert [test.path for test in scope.affected_tests] == [
        Path("tests/test_module.py")
    ]
    assert scope.qa_required is True
    assert scope.risk_level == "medium"


def test_impact_analyzer_detects_test_only_change_low_risk(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("tests/test_module.py",))

    assert scope.changed_modules[0].name == "tests.test_module"
    assert scope.affected_tests[0].path == Path("tests/test_module.py")
    assert scope.qa_required is True
    assert scope.risk_level == "low"


def test_impact_analyzer_raises_package_init_change_to_medium(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("src/sample/__init__.py",))

    assert [package.name for package in scope.affected_packages] == [
        "sample",
    ]
    assert scope.risk_level == "medium"


def test_impact_analyzer_raises_missing_tests_to_medium(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "uncovered.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("src/sample/uncovered.py",))

    assert scope.affected_tests == ()
    assert scope.risk_level == "medium"


def test_impact_analyzer_raises_core_module_change_to_high(tmp_path):
    repository = tmp_path / "sample_repo"
    repository_core = repository / "src" / "builder" / "repository"

    repository_core.mkdir(parents=True)
    (repository / "src" / "builder" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (repository_core / "__init__.py").write_text("", encoding="utf-8")
    (repository_core / "query.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("src/builder/repository/query.py",))

    assert scope.risk_level == "high"


@dataclass(frozen=True, slots=True)
class ErrorQA:
    def issues(self) -> tuple[QAIssue, ...]:
        return (
            QAIssue(
                code="repository.error",
                message="Synthetic error",
                severity="error",
                target="repository",
            ),
        )


def test_impact_analyzer_raises_qa_error_to_high(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    analyzer = RepositoryImpactAnalyzer(
        intelligence=analyzer.intelligence,
        query=analyzer.query,
        qa=ErrorQA(),
        change_analyzer=analyzer.change_analyzer,
    )
    scope = analyzer.analyze(("src/sample/module.py",))

    assert scope.risk_level == "high"


def test_impact_analyzer_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")

    analyzer = build_impact_analyzer(repository)
    scope = analyzer.analyze(("src/sample/zeta.py", "src/sample/alpha.py"))

    assert scope.source_files == (
        Path("src/sample/alpha.py"),
        Path("src/sample/zeta.py"),
    )
    assert [module.name for module in scope.affected_modules] == [
        "sample.alpha",
        "sample.zeta",
    ]
