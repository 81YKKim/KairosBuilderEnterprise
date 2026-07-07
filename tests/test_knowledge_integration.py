from pathlib import Path

from builder.knowledge.integration import KnowledgePlatform
from builder.knowledge.model import (
    KnowledgeEntityType,
    KnowledgeRelationshipType,
)
from builder.repository.integration import RepositoryPlatform


def create_sample_repository(root: Path) -> None:
    source = root / "src" / "sample"
    tests = root / "tests"
    docs = root / "docs"

    source.mkdir(parents=True)
    tests.mkdir()
    docs.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (source / "zeta.py").write_text("", encoding="utf-8")
    (tests / "test_alpha.py").write_text("", encoding="utf-8")
    (docs / "guide.md").write_text("# Guide\n", encoding="utf-8")


def build_platform(tmp_path: Path) -> KnowledgePlatform:
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    repository_platform = RepositoryPlatform.create(repository)

    return KnowledgePlatform.build(repository_platform)


def test_knowledge_platform_builds_all_components(tmp_path):
    platform = build_platform(tmp_path)

    assert platform.repository_platform is not None
    assert platform.evidence_extractor is not None
    assert platform.evidence.count == 6
    assert platform.knowledge_extractor is not None
    assert platform.knowledge.entity_count == 6
    assert platform.graph is not None
    assert platform.query is not None
    assert platform.cache.entity_count == 6


def test_knowledge_platform_create_alias_matches_build(tmp_path):
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)
    repository_platform = RepositoryPlatform.create(repository)

    created = KnowledgePlatform.create(repository_platform)
    built = KnowledgePlatform.build(repository_platform)

    assert created.evidence_summary() == built.evidence_summary()
    assert created.knowledge_summary() == built.knowledge_summary()
    assert created.snapshot().snapshot_id == built.snapshot().snapshot_id


def test_knowledge_platform_returns_evidence_and_knowledge_summaries(tmp_path):
    platform = build_platform(tmp_path)

    assert platform.evidence_summary() == {
        "total": 6,
        "packages": 1,
        "modules": 3,
        "tests": 1,
        "documents": 1,
        "errors": 0,
        "warnings": 0,
        "infos": 6,
    }
    assert platform.knowledge_summary() == {
        "entities": 6,
        "relationships": 2,
        "packages": 1,
        "modules": 3,
        "tests": 1,
        "documents": 1,
    }


def test_knowledge_platform_delegates_entity_and_relationship_lookup(tmp_path):
    platform = build_platform(tmp_path)
    package = next(
        entity
        for entity in platform.entities()
        if entity.entity_type == KnowledgeEntityType.PACKAGE
    )
    relationship = next(
        relationship
        for relationship in platform.relationships()
        if relationship.relationship_type == KnowledgeRelationshipType.CONTAINS
    )

    assert platform.find_entity(package.entity_id) == package
    assert platform.find_entity("missing") is None
    assert platform.find_relationship(relationship.relationship_id) == relationship
    assert platform.find_relationship("missing") is None


def test_knowledge_platform_delegates_graph_navigation(tmp_path):
    platform = build_platform(tmp_path)
    package = next(
        entity
        for entity in platform.entities()
        if entity.entity_type == KnowledgeEntityType.PACKAGE
    )

    dependencies = platform.dependencies(package.entity_id)
    dependents = platform.dependents(package.entity_id)
    neighbors = platform.neighbors(package.entity_id)

    assert sorted(entity.name for entity in dependencies) == [
        "sample.alpha",
        "sample.zeta",
    ]
    assert dependents == ()
    assert neighbors == dependencies


def test_knowledge_platform_snapshot_and_validate(tmp_path):
    platform = build_platform(tmp_path)
    snapshot = platform.snapshot()

    assert snapshot.snapshot_id == platform.cache.cache_id
    assert snapshot.entity_count == 6
    assert snapshot.relationship_count == 2
    assert snapshot.metadata["source"] == "knowledge-platform"
    assert platform.validate() == {
        "has_repository_platform": True,
        "has_evidence": True,
        "has_knowledge": True,
        "has_graph": True,
        "has_query": True,
        "has_cache": True,
        "cache_valid": True,
        "entity_count": 6,
        "relationship_count": 2,
    }


def test_knowledge_platform_returns_deterministic_ordering(tmp_path):
    platform = build_platform(tmp_path)

    assert platform.entities() == tuple(
        sorted(
            platform.entities(),
            key=lambda entity: entity.entity_id,
        )
    )
    assert platform.relationships() == tuple(
        sorted(
            platform.relationships(),
            key=lambda relationship: relationship.relationship_id,
        )
    )
