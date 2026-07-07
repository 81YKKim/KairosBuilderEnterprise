from pathlib import Path

from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.index import build_index, create_cache
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder
from builder.repository.qa import RepositoryQA
from builder.repository.query import RepositoryQuery


def build_repository_services(repository: Path):
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

    return intelligence, query, qa


def test_repository_index_creates_lookup_tables(tmp_path):
    repository = tmp_path / "sample_repo"
    domain = repository / "src" / "sample" / "domain"

    domain.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (domain / "__init__.py").write_text("", encoding="utf-8")
    (domain / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")

    intelligence, query, qa = build_repository_services(repository)
    index = build_index(intelligence, query, qa)

    assert index.find_package("sample.domain").name == "sample.domain"
    assert index.find_module("sample.domain.entity").name == (
        "sample.domain.entity"
    )
    assert sorted(index.packages_by_name) == [
        "sample",
        "sample.domain",
    ]
    assert sorted(index.modules_by_name) == [
        "sample.domain.entity",
    ]


def test_repository_index_groups_modules_tests_and_resources(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (tests / "test_alpha.py").write_text("", encoding="utf-8")
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")
    (repository / "config.json").write_text("{}", encoding="utf-8")

    intelligence, query, qa = build_repository_services(repository)
    index = build_index(intelligence, query, qa)

    assert [module.name for module in index.modules_in_package("sample")] == [
        "sample.alpha",
        "sample.zeta",
    ]
    assert [test.path for test in index.tests_for_module("sample.alpha")] == [
        Path("tests/test_alpha.py")
    ]
    assert index.tests_for_module("sample.zeta") == ()
    assert index.resources_by_suffix == {
        ".json": (Path("config.json"),),
        ".md": (Path("README.md"),),
    }


def test_repository_cache_creation_is_stable(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")

    intelligence, query, qa = build_repository_services(repository)
    first_cache = create_cache(
        intelligence,
        query,
        qa,
        created_at="2026-07-07T00:00:00Z",
    )
    second_cache = create_cache(
        intelligence,
        query,
        qa,
        created_at="2026-07-07T00:00:00Z",
    )

    assert first_cache.snapshot_id == second_cache.snapshot_id
    assert first_cache.created_at == "2026-07-07T00:00:00Z"
    assert first_cache.metrics.total_files == 3
    assert first_cache.qa_summary == {
        "issue_count": 0,
        "passed": True,
        "failed_checks": (),
    }


def test_repository_index_is_deterministically_ordered(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (tests / "test_zeta.py").write_text("", encoding="utf-8")
    (repository / "zeta.txt").write_text("", encoding="utf-8")
    (repository / "alpha.txt").write_text("", encoding="utf-8")

    intelligence, query, qa = build_repository_services(repository)
    index = build_index(intelligence, query, qa)

    assert tuple(index.packages_by_name) == ("sample",)
    assert tuple(index.modules_by_name) == (
        "sample.alpha",
        "sample.zeta",
        "tests.test_zeta",
    )
    assert index.resources_by_suffix[".txt"] == (
        Path("alpha.txt"),
        Path("zeta.txt"),
    )
