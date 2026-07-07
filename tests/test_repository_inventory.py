from pathlib import Path

from builder.repository.inventory import RepositoryInventoryBuilder


def test_repository_inventory_classifies_scanner_results(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample" / "domain"
    tests = repository / "tests"
    assets = repository / "resources"

    package.mkdir(parents=True)
    tests.mkdir(parents=True)
    assets.mkdir(parents=True)

    (repository / "src" / "sample" / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "entity.py").write_text("class Entity: pass\n", encoding="utf-8")
    (package / "service.py").write_text("class Service: pass\n", encoding="utf-8")
    (tests / "test_entity.py").write_text(
        "def test_entity():\n    assert True\n",
        encoding="utf-8",
    )
    (assets / "config.json").write_text("{}", encoding="utf-8")
    (repository / "README.md").write_text("# Sample\n", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(
        repository,
        git_root=repository,
        branch="main",
        head_commit="abc123",
    )

    assert inventory.repository_root == repository
    assert inventory.files == (
        Path("README.md"),
        Path("resources/config.json"),
        Path("src/sample/__init__.py"),
        Path("src/sample/domain/__init__.py"),
        Path("src/sample/domain/entity.py"),
        Path("src/sample/domain/service.py"),
        Path("tests/test_entity.py"),
    )
    assert inventory.python_files == (
        Path("src/sample/__init__.py"),
        Path("src/sample/domain/__init__.py"),
        Path("src/sample/domain/entity.py"),
        Path("src/sample/domain/service.py"),
        Path("tests/test_entity.py"),
    )
    assert [package.name for package in inventory.packages] == [
        "sample",
        "sample.domain",
    ]
    assert [module.name for module in inventory.modules] == [
        "sample.domain.entity",
        "sample.domain.service",
        "tests.test_entity",
    ]
    assert [test_file.path for test_file in inventory.test_files] == [
        Path("tests/test_entity.py")
    ]
    assert inventory.resource_files == (
        Path("README.md"),
        Path("resources/config.json"),
    )


def test_repository_inventory_summarizes_counts(tmp_path):
    repository = tmp_path / "sample_repo"
    package = repository / "src" / "sample"
    tests = repository / "tests"

    package.mkdir(parents=True)
    tests.mkdir()

    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tests / "test_module.py").write_text(
        "def test_module():\n    assert True\n",
        encoding="utf-8",
    )
    (repository / "pyproject.toml").write_text(
        "[project]\nname = 'sample'\n",
        encoding="utf-8",
    )

    inventory = RepositoryInventoryBuilder().build(repository)

    assert inventory.package_count == 1
    assert inventory.module_count == 2
    assert inventory.python_file_count == 3
    assert inventory.test_count == 1
    assert inventory.resource_count == 1
    assert inventory.total_file_count == 4
    assert inventory.summary == {
        "package_count": 1,
        "module_count": 2,
        "python_file_count": 3,
        "test_count": 1,
        "resource_count": 1,
        "total_file_count": 4,
    }


def test_repository_inventory_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"
    tests = repository / "tests"

    source.mkdir(parents=True)
    tests.mkdir()

    (source / "zeta.py").write_text("", encoding="utf-8")
    (repository / "zeta.json").write_text("{}", encoding="utf-8")
    (source / "__init__.py").write_text("", encoding="utf-8")
    (tests / "test_zeta.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (repository / "alpha.json").write_text("{}", encoding="utf-8")

    inventory = RepositoryInventoryBuilder().build(repository)

    assert inventory.files == tuple(
        sorted(inventory.files, key=lambda path: path.as_posix())
    )
    assert inventory.python_files == tuple(
        sorted(inventory.python_files, key=lambda path: path.as_posix())
    )
    assert inventory.resource_files == tuple(
        sorted(inventory.resource_files, key=lambda path: path.as_posix())
    )
    assert [module.name for module in inventory.modules] == [
        "sample.alpha",
        "sample.zeta",
        "tests.test_zeta",
    ]
