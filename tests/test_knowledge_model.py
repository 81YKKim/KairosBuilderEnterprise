from dataclasses import FrozenInstanceError

import pytest

from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)


def test_knowledge_entity_creation_uses_stable_entity_id():
    first = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="builder.repository.integration",
        summary="RepositoryPlatform public integration module.",
        evidence_ids=("evidence-b", "evidence-a"),
        metadata={
            "layer": "perception",
            "epic": "EPIC-01",
        },
    )
    second = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="builder.repository.integration",
        summary="RepositoryPlatform public integration module.",
        evidence_ids=("evidence-a", "evidence-b"),
        metadata={
            "epic": "EPIC-01",
            "layer": "perception",
        },
    )

    assert first.entity_id == second.entity_id
    assert first.entity_type == KnowledgeEntityType.MODULE
    assert first.evidence_ids == ("evidence-a", "evidence-b")
    assert first.metadata == {
        "epic": "EPIC-01",
        "layer": "perception",
    }


def test_knowledge_relationship_creation_uses_stable_relationship_id():
    first = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.CONTAINS,
        source_entity_id="entity:repository",
        target_entity_id="entity:module",
        evidence_ids=("evidence-b", "evidence-a"),
        metadata={
            "source": "RepositoryPlatform",
        },
    )
    second = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.CONTAINS,
        source_entity_id="entity:repository",
        target_entity_id="entity:module",
        evidence_ids=("evidence-a", "evidence-b"),
        metadata={
            "source": "RepositoryPlatform",
        },
    )

    assert first.relationship_id == second.relationship_id
    assert first.relationship_type == KnowledgeRelationshipType.CONTAINS
    assert first.evidence_ids == ("evidence-a", "evidence-b")
    assert first.metadata == {
        "source": "RepositoryPlatform",
    }


def test_knowledge_collection_counts_and_filters():
    repository = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.REPOSITORY,
        name="KairosBuilderEnterprise",
        summary="Repository source of truth.",
        evidence_ids=("evidence-repository",),
    )
    module = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="builder.repository.integration",
        summary="RepositoryPlatform module.",
        evidence_ids=("evidence-module",),
    )
    contains = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.CONTAINS,
        source_entity_id=repository.entity_id,
        target_entity_id=module.entity_id,
        evidence_ids=("evidence-relationship",),
    )
    references = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.REFERENCES,
        source_entity_id=module.entity_id,
        target_entity_id=repository.entity_id,
        evidence_ids=("evidence-reference",),
    )

    collection = KnowledgeCollection(
        entities=(module, repository),
        relationships=(references, contains),
    )

    assert collection.entity_count == 2
    assert collection.relationship_count == 2
    assert collection.entities_by_type(KnowledgeEntityType.MODULE).entities == (
        module,
    )
    assert collection.relationships_by_type(
        KnowledgeRelationshipType.CONTAINS
    ).relationships == (contains,)
    assert collection.find_entity(repository.entity_id) == repository
    assert collection.find_relationship(contains.relationship_id) == contains
    assert collection.find_entity("missing") is None
    assert collection.find_relationship("missing") is None


def test_knowledge_collection_returns_deterministic_ordering():
    zeta = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="zeta",
        summary="Zeta",
        evidence_ids=("evidence-zeta",),
    )
    alpha = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="alpha",
        summary="Alpha",
        evidence_ids=("evidence-alpha",),
    )
    zeta_relationship = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.REFERENCES,
        source_entity_id=zeta.entity_id,
        target_entity_id=alpha.entity_id,
        evidence_ids=("evidence-zeta",),
    )
    alpha_relationship = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.REFERENCES,
        source_entity_id=alpha.entity_id,
        target_entity_id=zeta.entity_id,
        evidence_ids=("evidence-alpha",),
    )

    collection = KnowledgeCollection(
        entities=(zeta, alpha),
        relationships=(zeta_relationship, alpha_relationship),
    )

    assert collection.entities == tuple(
        sorted(collection.entities, key=lambda entity: entity.entity_id)
    )
    assert collection.relationships == tuple(
        sorted(
            collection.relationships,
            key=lambda relationship: relationship.relationship_id,
        )
    )


def test_knowledge_models_are_immutable():
    entity = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.DOCUMENT,
        name="Master Architecture",
        summary="Architecture document.",
        evidence_ids=("evidence-document",),
    )
    relationship = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.REFERENCES,
        source_entity_id=entity.entity_id,
        target_entity_id=entity.entity_id,
        evidence_ids=("evidence-document",),
    )
    collection = KnowledgeCollection(
        entities=(entity,),
        relationships=(relationship,),
    )

    with pytest.raises(FrozenInstanceError):
        entity.name = "Changed"

    with pytest.raises(FrozenInstanceError):
        relationship.source_entity_id = "changed"

    with pytest.raises(FrozenInstanceError):
        collection.entities = ()
