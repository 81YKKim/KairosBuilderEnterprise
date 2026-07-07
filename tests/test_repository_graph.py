from pathlib import Path

from builder.repository.graph import RepositoryGraphBuilder
from builder.repository.inventory import RepositoryInventoryBuilder


def test_repository_graph_builds_package_and_module_graph(tmp_path):
    repository = tmp_path / "sample_repo"
    domain = repository / "src" / "sample" / "domain"
    services = repository / "src" / "sample" / "services"

    domain.mkdir(parents=True)
    services.mkdir(parents=True)

    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (domain / "__init__.py").write_text("", encoding="utf-8")
    (domain / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")
    (services / "__init__.py").write_text("", encoding="utf-8")
    (services / "service.py").write_text("class Service: pass\n", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)

    assert [package.name for package in graph.packages()] == [
        "sample",
        "sample.domain",
        "sample.services",
    ]
    assert [module.name for module in graph.modules()] == [
        "sample.domain.entity",
        "sample.services.service",
    ]
    assert graph.find_package("sample.domain").name == "sample.domain"
    assert graph.find_module("sample.services.service").name == (
        "sample.services.service"
    )
    assert graph.find_package("missing") is None
    assert graph.find_module("missing") is None


def test_repository_graph_tracks_package_module_relationships(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"

    package.mkdir(parents=True)
    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "alpha.py").write_text("ALPHA = 1\n", encoding="utf-8")
    (package / "zeta.py").write_text("ZETA = 1\n", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)

    assert [module.name for module in graph.modules_in_package("sample")] == []
    assert [module.name for module in graph.modules_in_package("sample.domain")] == [
        "sample.domain.alpha",
        "sample.domain.zeta",
    ]
    assert graph.parent_package("sample") is None
    assert graph.parent_package("sample.domain").name == "sample"
    assert graph.child_packages("sample")[0].name == "sample.domain"


def test_repository_graph_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    beta = source / "beta"
    alpha = source / "alpha"

    beta.mkdir(parents=True)
    alpha.mkdir(parents=True)

    (source / "__init__.py").write_text("", encoding="utf-8")
    (beta / "__init__.py").write_text("", encoding="utf-8")
    (beta / "zeta.py").write_text("", encoding="utf-8")
    (alpha / "__init__.py").write_text("", encoding="utf-8")
    (alpha / "alpha.py").write_text("", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)
    graph = RepositoryGraphBuilder().build(inventory)

    assert [package.name for package in graph.packages()] == [
        "sample",
        "sample.alpha",
        "sample.beta",
    ]
    assert [module.name for module in graph.modules()] == [
        "sample.alpha.alpha",
        "sample.beta.zeta",
    ]
    assert graph.package_names == (
        "sample",
        "sample.alpha",
        "sample.beta",
    )
    assert graph.module_names == (
        "sample.alpha.alpha",
        "sample.beta.zeta",
    )


def test_repository_graph_uses_inventory_without_rescanning(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    source.mkdir(parents=True)

    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "stable.py").write_text("VALUE = 1\n", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)
    (source / "created_after_inventory.py").write_text(
        "VALUE = 2\n",
        encoding="utf-8",
    )

    graph = RepositoryGraphBuilder().build(inventory)

    assert graph.find_module("sample.stable") is not None
    assert graph.find_module("sample.created_after_inventory") is None
