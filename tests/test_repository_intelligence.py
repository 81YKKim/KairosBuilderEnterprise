from pathlib import Path

from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.inventory import RepositoryInventoryBuilder


def build_intelligence(repository: Path) -> RepositoryIntelligence:
    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)

    return RepositoryIntelligence(
        inventory=inventory,
        graph=graph,
    )


def test_repository_intelligence_returns_summary_and_metrics(tmp_path):
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
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")

    intelligence = build_intelligence(repository)

    assert intelligence.repository_summary() == {
        "repository_root": str(repository),
        "total_files": 5,
        "python_files": 4,
        "package_count": 2,
        "module_count": 2,
        "test_count": 1,
        "resource_count": 1,
    }

    metrics = intelligence.repository_metrics()

    assert metrics.total_files == 5
    assert metrics.python_files == 4
    assert metrics.package_count == 2
    assert metrics.module_count == 2
    assert metrics.test_count == 1
    assert metrics.resource_count == 1


def test_repository_intelligence_exposes_package_and_module_lookup(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"

    package.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")

    intelligence = build_intelligence(repository)

    assert [package.name for package in intelligence.packages()] == [
        "sample",
        "sample.domain",
    ]
    assert [module.name for module in intelligence.modules()] == [
        "sample.domain.entity",
    ]
    assert intelligence.find_package("sample.domain").name == "sample.domain"
    assert intelligence.find_module("sample.domain.entity").name == (
        "sample.domain.entity"
    )
    assert intelligence.find_package("missing") is None
    assert intelligence.find_module("missing") is None


def test_repository_intelligence_returns_package_and_module_metrics(
    tmp_path,
):
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
    (domain / "alpha.py").write_text("ALPHA = 1\n", encoding="utf-8")
    (domain / "beta.py").write_text("BETA = 1\n", encoding="utf-8")
    (service / "__init__.py").write_text("", encoding="utf-8")

    intelligence = build_intelligence(repository)
    package_metrics = intelligence.package_metrics("sample.domain")
    module_metrics = intelligence.module_metrics("sample.domain.alpha")

    assert package_metrics is not None
    assert package_metrics.package_name == "sample.domain"
    assert package_metrics.module_count == 2
    assert package_metrics.child_package_count == 0
    assert package_metrics.parent_package == "sample"
    assert package_metrics.modules == (
        "sample.domain.alpha",
        "sample.domain.beta",
    )

    assert module_metrics is not None
    assert module_metrics.module_name == "sample.domain.alpha"
    assert module_metrics.package_name == "sample.domain"
    assert module_metrics.path == Path("src/sample/domain/alpha.py")
    assert intelligence.package_metrics("missing") is None
    assert intelligence.module_metrics("missing") is None


def test_repository_intelligence_identifies_largest_and_empty_packages(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    domain = repository / "src" / "sample" / "domain"
    empty = repository / "src" / "sample" / "empty"

    domain.mkdir(parents=True)
    empty.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (domain / "__init__.py").write_text("", encoding="utf-8")
    (domain / "alpha.py").write_text("ALPHA = 1\n", encoding="utf-8")
    (domain / "beta.py").write_text("BETA = 1\n", encoding="utf-8")
    (empty / "__init__.py").write_text("", encoding="utf-8")

    intelligence = build_intelligence(repository)

    assert intelligence.largest_package().package_name == "sample.domain"
    assert [package.name for package in intelligence.empty_packages()] == [
        "sample",
        "sample.empty",
    ]


def test_repository_intelligence_uses_existing_inventory_and_graph(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "stable.py").write_text("VALUE = 1\n", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)
    (source / "created_after_graph.py").write_text(
        "VALUE = 2\n",
        encoding="utf-8",
    )

    intelligence = RepositoryIntelligence(
        inventory=inventory,
        graph=graph,
    )

    assert intelligence.find_module("sample.stable") is not None
    assert intelligence.find_module("sample.created_after_graph") is None
