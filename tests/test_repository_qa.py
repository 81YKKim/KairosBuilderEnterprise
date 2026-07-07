from pathlib import Path

from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder
from builder.repository.qa import RepositoryQA
from builder.repository.query import RepositoryQuery


def build_qa(repository: Path) -> RepositoryQA:
    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)
    intelligence = RepositoryIntelligence(
        inventory=inventory,
        graph=graph,
    )
    query = RepositoryQuery(intelligence=intelligence)

    return RepositoryQA(
        intelligence=intelligence,
        query=query,
    )


def test_repository_qa_detects_empty_packages(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    empty = source / "empty"

    empty.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (empty / "__init__.py").write_text("", encoding="utf-8")

    qa = build_qa(repository)
    result = qa.run_check("empty_packages")

    assert result.passed is False
    assert [issue.code for issue in result.issues] == [
        "repository.empty_package",
        "repository.empty_package",
    ]
    assert [issue.target for issue in result.issues] == [
        "sample",
        "sample.empty",
    ]


def test_repository_qa_detects_duplicate_module_names(tmp_path):
    repository = tmp_path / "sample_repo"
    alpha = repository / "src" / "sample" / "alpha"
    beta = repository / "src" / "sample" / "beta"

    alpha.mkdir(parents=True)
    beta.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (alpha / "__init__.py").write_text("", encoding="utf-8")
    (alpha / "service.py").write_text("", encoding="utf-8")
    (beta / "__init__.py").write_text("", encoding="utf-8")
    (beta / "service.py").write_text("", encoding="utf-8")

    qa = build_qa(repository)
    result = qa.run_check("duplicate_module_names")

    assert result.passed is False
    assert result.issues[0].code == "repository.duplicate_module_name"
    assert result.issues[0].severity == "warning"
    assert result.issues[0].target == "service"


def test_repository_qa_detects_missing_tests(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "covered.py").write_text("", encoding="utf-8")
    (source / "uncovered.py").write_text("", encoding="utf-8")
    (tests / "test_covered.py").write_text(
        "def test_covered():\n    assert True\n",
        encoding="utf-8",
    )

    qa = build_qa(repository)
    result = qa.run_check("missing_tests")

    assert result.passed is False
    assert [issue.target for issue in result.issues] == [
        "sample.uncovered",
    ]
    assert result.issues[0].severity == "warning"


def test_repository_qa_run_all_returns_failed_checks_and_issues(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    empty = source / "empty"

    source.mkdir(parents=True)
    empty.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (empty / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")

    qa = build_qa(repository)
    result = qa.run_all()

    assert result.passed is False
    assert result.issue_count == len(qa.issues())
    assert result.failed_checks == (
        "empty_packages",
        "missing_tests",
    )
    assert qa.passed() is False


def test_repository_qa_passes_when_no_required_issues_exist(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text(
        "def test_module():\n    assert True\n",
        encoding="utf-8",
    )

    qa = build_qa(repository)
    result = qa.run_all()

    assert result.passed is True
    assert result.issue_count == 0
    assert result.failed_checks == ()
    assert qa.passed() is True


def test_repository_qa_returns_deterministic_issue_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")

    qa = build_qa(repository)
    result = qa.run_check("missing_tests")

    assert [issue.target for issue in result.issues] == [
        "sample.alpha",
        "sample.zeta",
    ]
