from pathlib import Path

from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder
from builder.repository.query import RepositoryQuery


def build_query(repository: Path) -> RepositoryQuery:
    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)
    intelligence = RepositoryIntelligence(
        inventory=inventory,
        graph=graph,
    )

    return RepositoryQuery(intelligence=intelligence)


def test_repository_query_returns_packages_and_modules(tmp_path):
    repository = tmp_path / "sample_repo"
    domain = repository / "src" / "sample" / "domain"
    service = repository / "src" / "sample" / "service"

    domain.mkdir(parents=True)
    service.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (domain / "__init__.py").write_text("", encoding="utf-8")
    (domain / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")
    (service / "__init__.py").write_text("", encoding="utf-8")
    (service / "handler.py").write_text("class Handler: pass\n", encoding="utf-8")

    query = build_query(repository)
    package_result = query.packages()
    module_result = query.modules()

    assert package_result.query == "packages"
    assert package_result.count == 3
    assert [package.name for package in package_result.items] == [
        "sample",
        "sample.domain",
        "sample.service",
    ]
    assert module_result.query == "modules"
    assert [module.name for module in module_result.items] == [
        "sample.domain.entity",
        "sample.service.handler",
    ]


def test_repository_query_supports_package_and_module_lookup(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"

    package.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")

    query = build_query(repository)

    assert query.find_package("sample.domain").items[0].name == "sample.domain"
    assert query.find_module("sample.domain.entity").items[0].name == (
        "sample.domain.entity"
    )
    assert query.find_package("missing").items == ()
    assert query.find_module("missing").items == ()


def test_repository_query_finds_tests_and_tests_for_module(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")
    (tests / "test_entity.py").write_text(
        "def test_entity():\n    assert True\n",
        encoding="utf-8",
    )
    (tests / "test_other.py").write_text(
        "def test_other():\n    assert True\n",
        encoding="utf-8",
    )

    query = build_query(repository)

    assert [test.path for test in query.find_tests().items] == [
        Path("tests/test_entity.py"),
        Path("tests/test_other.py"),
    ]
    assert [test.path for test in query.tests_for_module("sample.entity").items] == [
        Path("tests/test_entity.py")
    ]


def test_repository_query_searches_by_name_and_text(tmp_path):
    repository = tmp_path / "sample_repo"
    domain = repository / "src" / "sample" / "domain"
    tests = repository / "tests"

    domain.mkdir(parents=True)
    tests.mkdir()
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (domain / "__init__.py").write_text("", encoding="utf-8")
    (domain / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")
    (tests / "test_entity.py").write_text(
        "def test_entity():\n    assert True\n",
        encoding="utf-8",
    )
    (repository / "README.md").write_text("# Entity docs\n", encoding="utf-8")

    query = build_query(repository)

    assert [item.name for item in query.find_by_name("sample.domain").items] == [
        "sample.domain"
    ]
    assert [item.name for item in query.search("entity").items] == [
        "sample.domain.entity",
        "test_entity",
        "README",
    ]


def test_repository_query_where_filters_items_deterministically(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")

    query = build_query(repository)
    result = query.where(
        "modules",
        lambda item: item.name.endswith("zeta"),
    )

    assert result.query == "where"
    assert result.filters == (
        ("source", "modules"),
    )
    assert [module.name for module in result.items] == ["sample.zeta"]


def test_repository_query_returns_relationship_queries(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"

    package.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "alpha.py").write_text("", encoding="utf-8")
    (package / "beta.py").write_text("", encoding="utf-8")

    query = build_query(repository)

    assert [module.name for module in query.find_modules_in_package("sample.domain").items] == [
        "sample.domain.alpha",
        "sample.domain.beta",
    ]
    assert query.find_importers("sample.domain.alpha").items == ()
    assert query.find_dependents("sample.domain.alpha").items == ()


def test_repository_query_does_not_rescan_repository(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "stable.py").write_text("", encoding="utf-8")

    query = build_query(repository)
    (source / "created_after_query.py").write_text("", encoding="utf-8")

    assert query.find_module("sample.stable").count == 1
    assert query.find_module("sample.created_after_query").count == 0
