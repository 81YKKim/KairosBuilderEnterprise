from builder.knowledge.graph import KnowledgeGraph
from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)
from builder.knowledge.query import KnowledgeQuery


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
    label: str,
) -> KnowledgeRelationship:
    return KnowledgeRelationship.create(
        relationship_type=relationship_type,
        source_entity_id=source.entity_id,
        target_entity_id=target.entity_id,
        evidence_ids=(f"evidence:{label}",),
        metadata={
            "label": label,
        },
    )


def build_query() -> KnowledgeQuery:
    repository = make_entity("repo", KnowledgeEntityType.REPOSITORY)
    package = make_entity("sample", KnowledgeEntityType.PACKAGE)
    module = make_entity("sample.module", KnowledgeEntityType.MODULE)
    test = make_entity("test_module", KnowledgeEntityType.TEST)
    contains_package = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        repository,
        package,
        "repository_contains_package",
    )
    contains_module = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        package,
        module,
        "package_contains_module",
    )
    tests_module = make_relationship(
        KnowledgeRelationshipType.TESTS,
        test,
        module,
        "test_tests_module",
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(repository, package, module, test),
            relationships=(
                contains_package,
                contains_module,
                tests_module,
            ),
        )
    )

    return KnowledgeQuery(graph=graph)


def test_knowledge_query_lists_entities_and_relationships():
    query = build_query()

    entity_result = query.entities()
    relationship_result = query.relationships()

    assert entity_result.query == "entities"
    assert entity_result.count == 4
    assert [entity.name for entity in entity_result.items] == [
        entity.name for entity in query.graph.entities()
    ]
    assert relationship_result.query == "relationships"
    assert relationship_result.count == 3


def test_knowledge_query_finds_entity_and_relationship():
    query = build_query()
    entity = query.graph.entities()[0]
    relationship = query.graph.relationships()[0]

    entity_result = query.find_entity(entity.entity_id)
    relationship_result = query.find_relationship(relationship.relationship_id)

    assert entity_result.items == (entity,)
    assert entity_result.filters == (("entity_id", entity.entity_id),)
    assert relationship_result.items == (relationship,)
    assert relationship_result.filters == (
        ("relationship_id", relationship.relationship_id),
    )
    assert query.find_entity("missing").items == ()
    assert query.find_relationship("missing").items == ()


def test_knowledge_query_filters_by_type():
    query = build_query()

    module_result = query.entities_by_type(KnowledgeEntityType.MODULE)
    contains_result = query.relationships_by_type(
        KnowledgeRelationshipType.CONTAINS
    )

    assert [entity.name for entity in module_result.items] == [
        "sample.module",
    ]
    assert contains_result.count == 2
    assert contains_result.filters == (
        ("relationship_type", "contains"),
    )


def test_knowledge_query_searches_entities_and_relationships():
    query = build_query()

    entity_result = query.search_entities("module")
    relationship_result = query.search_relationships("package_contains")

    assert sorted(entity.name for entity in entity_result.items) == [
        "sample.module",
        "test_module",
    ]
    assert relationship_result.count == 1
    assert relationship_result.items[0].metadata["label"] == (
        "package_contains_module"
    )


def test_knowledge_query_delegates_graph_relationship_queries():
    query = build_query()
    package = next(
        entity
        for entity in query.graph.entities()
        if entity.name == "sample"
    )
    module = next(
        entity
        for entity in query.graph.entities()
        if entity.name == "sample.module"
    )

    assert query.neighbors(package.entity_id).items == query.graph.neighbors(
        package.entity_id
    )
    assert query.dependencies(package.entity_id).items == (
        module,
    )
    assert query.dependents(module.entity_id).items == query.graph.dependents(
        module.entity_id
    )


def test_knowledge_query_where_filters_items():
    query = build_query()

    entity_result = query.where_entities(
        lambda entity: entity.name.startswith("sample")
    )
    relationship_result = query.where_relationships(
        lambda relationship: relationship.relationship_type
        == KnowledgeRelationshipType.TESTS
    )

    assert sorted(entity.name for entity in entity_result.items) == [
        "sample",
        "sample.module",
    ]
    assert relationship_result.count == 1
    assert relationship_result.items[0].relationship_type == (
        KnowledgeRelationshipType.TESTS
    )


def test_knowledge_query_returns_deterministic_ordering():
    query = build_query()

    assert query.entities().items == tuple(
        sorted(
            query.entities().items,
            key=lambda entity: entity.entity_id,
        )
    )
    assert query.relationships().items == tuple(
        sorted(
            query.relationships().items,
            key=lambda relationship: relationship.relationship_id,
        )
    )
