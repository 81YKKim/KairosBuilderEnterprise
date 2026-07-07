from pathlib import Path

from builder.evidence.model import (
    Evidence,
    EvidenceCollection,
    EvidenceSeverity,
    EvidenceSource,
    EvidenceType,
)
from builder.knowledge.extractor import KnowledgeExtractor
from builder.knowledge.model import (
    KnowledgeEntityType,
    KnowledgeRelationshipType,
)


def make_evidence(
    evidence_type: EvidenceType,
    name: str,
    path: str,
    metadata: dict[str, str] | None = None,
) -> Evidence:
    return Evidence.create(
        evidence_type=evidence_type,
        source=EvidenceSource(
            source_id=f"{evidence_type.value}:{name}",
            source_type=evidence_type,
            path=Path(path),
            name=name,
        ),
        summary=f"{name} summary",
        details=f"{name} details",
        severity=EvidenceSeverity.INFO,
        metadata=metadata or {},
    )


def test_knowledge_extractor_creates_entities_from_evidence():
    repository = make_evidence(EvidenceType.REPOSITORY, "repo", ".")
    package = make_evidence(EvidenceType.PACKAGE, "sample", "src/sample")
    module = make_evidence(
        EvidenceType.MODULE,
        "sample.module",
        "src/sample/module.py",
        {"package": "sample"},
    )
    test = make_evidence(
        EvidenceType.TEST,
        "test_module",
        "tests/test_module.py",
        {"module": "sample.module"},
    )
    document = make_evidence(EvidenceType.DOCUMENT, "README", "README.md")

    collection = KnowledgeExtractor().extract_entities(
        EvidenceCollection(
            items=(
                module,
                repository,
                document,
                test,
                package,
            )
        )
    )

    assert collection.relationship_count == 0
    assert sorted(entity.name for entity in collection.entities) == [
        "README",
        "repo",
        "sample",
        "sample.module",
        "test_module",
    ]
    assert sorted(entity.entity_type for entity in collection.entities) == [
        KnowledgeEntityType.DOCUMENT,
        KnowledgeEntityType.MODULE,
        KnowledgeEntityType.PACKAGE,
        KnowledgeEntityType.REPOSITORY,
        KnowledgeEntityType.TEST,
    ]


def test_knowledge_extractor_creates_repository_contains_relationships():
    repository = make_evidence(EvidenceType.REPOSITORY, "repo", ".")
    package = make_evidence(EvidenceType.PACKAGE, "sample", "src/sample")
    module = make_evidence(EvidenceType.MODULE, "sample.module", "src/sample/module.py")

    collection = KnowledgeExtractor().extract(
        EvidenceCollection(items=(repository, package, module))
    )
    contains = collection.relationships_by_type(
        KnowledgeRelationshipType.CONTAINS
    )

    assert contains.relationship_count == 2
    assert sorted(
        relationship.metadata["relationship"]
        for relationship in contains.relationships
    ) == [
        "repository_contains_module",
        "repository_contains_package",
    ]


def test_knowledge_extractor_creates_package_contains_module_relationship():
    repository = make_evidence(EvidenceType.REPOSITORY, "repo", ".")
    package = make_evidence(EvidenceType.PACKAGE, "sample", "src/sample")
    module = make_evidence(
        EvidenceType.MODULE,
        "sample.module",
        "src/sample/module.py",
        {"package": "sample"},
    )

    collection = KnowledgeExtractor().extract(
        EvidenceCollection(items=(repository, package, module))
    )

    assert any(
        relationship.metadata["relationship"] == "package_contains_module"
        for relationship in collection.relationships
    )


def test_knowledge_extractor_creates_test_tests_module_relationship():
    repository = make_evidence(EvidenceType.REPOSITORY, "repo", ".")
    module = make_evidence(EvidenceType.MODULE, "sample.module", "src/sample/module.py")
    test = make_evidence(
        EvidenceType.TEST,
        "test_module",
        "tests/test_module.py",
        {"module": "sample.module"},
    )

    collection = KnowledgeExtractor().extract(
        EvidenceCollection(items=(repository, module, test))
    )
    tests_relationships = collection.relationships_by_type(
        KnowledgeRelationshipType.TESTS
    )

    assert tests_relationships.relationship_count == 1
    assert tests_relationships.relationships[0].metadata["relationship"] == (
        "test_tests_module"
    )


def test_knowledge_extractor_returns_stable_ids_and_deterministic_ordering():
    repository = make_evidence(EvidenceType.REPOSITORY, "repo", ".")
    alpha = make_evidence(EvidenceType.MODULE, "sample.alpha", "src/sample/alpha.py")
    zeta = make_evidence(EvidenceType.MODULE, "sample.zeta", "src/sample/zeta.py")
    extractor = KnowledgeExtractor()

    first = extractor.extract(EvidenceCollection(items=(zeta, repository, alpha)))
    second = extractor.extract(EvidenceCollection(items=(alpha, zeta, repository)))

    assert [entity.entity_id for entity in first.entities] == [
        entity.entity_id for entity in second.entities
    ]
    assert [relationship.relationship_id for relationship in first.relationships] == [
        relationship.relationship_id for relationship in second.relationships
    ]
    assert first.entities == tuple(
        sorted(first.entities, key=lambda entity: entity.entity_id)
    )
    assert first.relationships == tuple(
        sorted(
            first.relationships,
            key=lambda relationship: relationship.relationship_id,
        )
    )
