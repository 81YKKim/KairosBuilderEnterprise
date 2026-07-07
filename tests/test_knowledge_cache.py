from builder.knowledge.cache import KnowledgeCache, KnowledgeSnapshot
from builder.knowledge.graph import KnowledgeGraph
from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)


def make_entity(name: str, entity_type: KnowledgeEntityType) -> KnowledgeEntity:
    return KnowledgeEntity.create(
        entity_type=entity_type,
        name=name,
        summary=f"{name} summary",
        evidence_ids=(f"evidence:{name}",),
    )


def make_relationship(
    relationship_type: KnowledgeRelationshipType,
    source: KnowledgeEntity,
    target: KnowledgeEntity,
) -> KnowledgeRelationship:
    return KnowledgeRelationship.create(
        relationship_type=relationship_type,
        source_entity_id=source.entity_id,
        target_entity_id=target.entity_id,
        evidence_ids=(f"evidence:{source.name}:{target.name}",),
    )


def make_graph() -> KnowledgeGraph:
    repository = make_entity("repo", KnowledgeEntityType.REPOSITORY)
    package = make_entity("sample", KnowledgeEntityType.PACKAGE)
    module = make_entity("sample.module", KnowledgeEntityType.MODULE)
    contains_package = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        repository,
        package,
    )
    contains_module = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        package,
        module,
    )

    return KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(module, repository, package),
            relationships=(contains_module, contains_package),
        )
    )


def test_knowledge_cache_create_stores_graph_counts_and_metadata():
    graph = make_graph()

    cache = KnowledgeCache.create(
        graph,
        metadata={"source": "unit-test"},
    )

    assert cache.graph == graph
    assert cache.entity_count == 3
    assert cache.relationship_count == 2
    assert cache.metadata["source"] == "unit-test"
    assert cache.cache_id
    assert cache.created_at


def test_knowledge_cache_finds_entities_and_relationships():
    graph = make_graph()
    cache = KnowledgeCache.create(graph)
    entity = graph.entities()[0]
    relationship = graph.relationships()[0]

    assert cache.find_entity(entity.entity_id) == entity
    assert cache.find_entity("missing") is None
    assert cache.find_relationship(relationship.relationship_id) == relationship
    assert cache.find_relationship("missing") is None


def test_knowledge_cache_returns_deterministic_entities_and_relationships():
    graph = make_graph()
    cache = KnowledgeCache.create(graph)

    assert cache.entities() == tuple(
        sorted(
            graph.entities(),
            key=lambda entity: entity.entity_id,
        )
    )
    assert cache.relationships() == tuple(
        sorted(
            graph.relationships(),
            key=lambda relationship: relationship.relationship_id,
        )
    )


def test_knowledge_cache_snapshot_has_stable_id_and_counts():
    graph = make_graph()
    first_cache = KnowledgeCache.create(
        graph,
        metadata={"source": "unit-test"},
    )
    second_cache = KnowledgeCache.create(
        graph,
        metadata={"source": "unit-test"},
    )

    first_snapshot = first_cache.snapshot()
    second_snapshot = second_cache.snapshot()

    assert isinstance(first_snapshot, KnowledgeSnapshot)
    assert first_snapshot.snapshot_id == second_snapshot.snapshot_id
    assert first_snapshot.snapshot_id == first_cache.cache_id
    assert first_snapshot.entity_count == 3
    assert first_snapshot.relationship_count == 2
    assert first_snapshot.metadata["source"] == "unit-test"
    assert first_cache.cache_id == second_cache.cache_id


def test_knowledge_cache_validate_passes_for_consistent_graph():
    cache = KnowledgeCache.create(make_graph())

    assert cache.validate() is True


def test_knowledge_cache_validate_fails_for_missing_relationship_endpoint():
    source = make_entity("source", KnowledgeEntityType.MODULE)
    relationship = KnowledgeRelationship.create(
        relationship_type=KnowledgeRelationshipType.DEPENDS_ON,
        source_entity_id=source.entity_id,
        target_entity_id="missing-target",
        evidence_ids=("evidence:missing-target",),
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(source,),
            relationships=(relationship,),
        )
    )

    cache = KnowledgeCache.create(graph)

    assert cache.validate() is False
