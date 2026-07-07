from pathlib import Path

from builder.evidence.extractor import EvidenceExtractor
from builder.evidence.model import (
    EvidenceSeverity,
    EvidenceType,
)
from builder.repository.integration import RepositoryPlatform


def create_sample_repository(root: Path) -> None:
    source = root / "src" / "sample"
    tests = root / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "module.py").write_text("", encoding="utf-8")
    (tests / "test_module.py").write_text("", encoding="utf-8")
    (root / "README.md").write_text("# Sample\n", encoding="utf-8")
    (root / "config.json").write_text("{}", encoding="utf-8")


def test_evidence_extractor_extracts_package_evidence(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    platform = RepositoryPlatform.create(repository)
    extractor = EvidenceExtractor(platform=platform)

    collection = extractor.extract_packages()

    assert collection.count == 1
    evidence = collection.items[0]
    assert evidence.evidence_type == EvidenceType.PACKAGE
    assert evidence.source.source_type == EvidenceType.PACKAGE
    assert evidence.source.name == "sample"
    assert evidence.source.path == Path("src/sample")
    assert evidence.severity == EvidenceSeverity.INFO


def test_evidence_extractor_extracts_module_and_test_evidence(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    platform = RepositoryPlatform.create(repository)
    extractor = EvidenceExtractor(platform=platform)

    module_collection = extractor.extract_modules()
    test_collection = extractor.extract_tests()

    assert sorted(item.source.name for item in module_collection.items) == [
        "sample.module",
        "tests.test_module",
    ]
    assert all(
        item.evidence_type == EvidenceType.MODULE
        for item in module_collection.items
    )
    assert [item.source.name for item in test_collection.items] == [
        "test_module"
    ]
    assert test_collection.items[0].evidence_type == EvidenceType.TEST


def test_evidence_extractor_extracts_resource_and_document_evidence(
    tmp_path,
):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    platform = RepositoryPlatform.create(repository)
    extractor = EvidenceExtractor(platform=platform)

    collection = extractor.extract_resources()

    assert sorted(
        (item.source.path for item in collection.items),
        key=lambda path: path.as_posix().casefold(),
    ) == [
        Path("config.json"),
        Path("README.md"),
    ]
    assert all(item.evidence_type == EvidenceType.DOCUMENT for item in collection.items)
    assert sorted(item.metadata["suffix"] for item in collection.items) == [
        ".json",
        ".md",
    ]


def test_evidence_extractor_extract_all_count_and_stable_ids(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    platform = RepositoryPlatform.create(repository)
    extractor = EvidenceExtractor(platform=platform)

    first = extractor.extract_all()
    second = extractor.extract_all()

    assert first.count == 6
    assert [item.evidence_id for item in first.items] == [
        item.evidence_id for item in second.items
    ]


def test_evidence_extractor_returns_deterministic_ordering(tmp_path):
    repository = tmp_path / "sample_repo"
    source = repository / "src" / "sample"

    source.mkdir(parents=True)
    (source / "zeta.py").write_text("", encoding="utf-8")
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (repository / "zeta.md").write_text("# Zeta\n", encoding="utf-8")
    (repository / "alpha.md").write_text("# Alpha\n", encoding="utf-8")

    platform = RepositoryPlatform.create(repository)
    extractor = EvidenceExtractor(platform=platform)
    collection = extractor.extract_all()

    assert collection.items == tuple(
        sorted(collection.items, key=lambda item: item.evidence_id)
    )


def test_evidence_extractor_uses_existing_platform_snapshot(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    platform = RepositoryPlatform.create(repository)
    (repository / "src" / "sample" / "created_after_platform.py").write_text(
        "",
        encoding="utf-8",
    )

    extractor = EvidenceExtractor(platform=platform)
    collection = extractor.extract_modules()

    assert sorted(item.source.name for item in collection.items) == [
        "sample.module",
        "tests.test_module",
    ]
