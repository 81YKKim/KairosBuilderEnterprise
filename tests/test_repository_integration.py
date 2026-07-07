from pathlib import Path

from builder.repository.integration import RepositoryPlatform


def create_sample_repository(root: Path) -> None:
    source = root / "src" / "sample"
    tests = root / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (tests / "test_alpha.py").write_text("", encoding="utf-8")
    (root / "README.md").write_text("# Sample\n", encoding="utf-8")


def test_repository_platform_create_builds_all_services(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    platform = RepositoryPlatform.create(repository)

    assert platform.scanner is not None
    assert platform.inventory.repository_root == repository
    assert platform.graph is not None
    assert platform.intelligence is not None
    assert platform.query_service is not None
    assert platform.qa_service is not None
    assert platform.change_analyzer is not None
    assert platform.impact_analyzer is not None
    assert platform.index is not None


def test_repository_platform_build_alias_matches_create(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    created = RepositoryPlatform.create(repository)
    built = RepositoryPlatform.build(repository)

    assert created.summary() == built.summary()
    assert tuple(created.index.modules_by_name) == tuple(built.index.modules_by_name)


def test_repository_platform_delegates_summary_metrics_and_query(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    platform = RepositoryPlatform.create(repository)

    assert platform.summary()["package_count"] == 1
    assert platform.metrics().module_count == 3
    assert [module.name for module in platform.modules()] == [
        "sample.alpha",
        "sample.zeta",
        "tests.test_alpha",
    ]
    assert [package.name for package in platform.packages()] == [
        "sample",
    ]
    assert platform.find_module("sample.alpha").name == "sample.alpha"
    assert platform.find_package("sample").name == "sample"
    assert platform.query("modules").count == 3


def test_repository_platform_delegates_qa_change_and_impact(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    platform = RepositoryPlatform.create(repository)
    qa_result = platform.qa()
    change_set = platform.analyze_change(("src/sample/alpha.py",))
    impact_scope = platform.analyze_impact(("src/sample/alpha.py",))

    assert qa_result.issue_count >= 1
    assert [module.name for module in change_set.changed_modules] == [
        "sample.alpha",
    ]
    assert [module.name for module in impact_scope.affected_modules] == [
        "sample.alpha",
    ]


def test_repository_platform_validate_reports_health(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    platform = RepositoryPlatform.create(repository)
    health = platform.validate()

    assert health["repository_root"] == str(repository)
    assert health["has_inventory"] is True
    assert health["has_graph"] is True
    assert health["has_index"] is True
    assert health["package_count"] == 1
    assert health["module_count"] == 3
    assert health["qa_passed"] is False


def test_repository_platform_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    platform = RepositoryPlatform.create(repository)

    assert [module.name for module in platform.modules()] == [
        "sample.alpha",
        "sample.zeta",
        "tests.test_alpha",
    ]
    assert tuple(platform.index.modules_by_name) == (
        "sample.alpha",
        "sample.zeta",
        "tests.test_alpha",
    )
