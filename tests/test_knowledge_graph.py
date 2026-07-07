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


def test_knowledge_graph_builds_from_collection():
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
    collection = KnowledgeCollection(
        entities=(module, repository, package),
        relationships=(contains_module, contains_package),
    )

    graph = KnowledgeGraph.from_collection(collection)

    assert graph.entities() == collection.entities
    assert graph.relationships() == collection.relationships


def test_knowledge_graph_finds_entities_and_relationships():
    repository = make_entity("repo", KnowledgeEntityType.REPOSITORY)
    module = make_entity("sample.module", KnowledgeEntityType.MODULE)
    relationship = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        repository,
        module,
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(repository, module),
            relationships=(relationship,),
        )
    )

    assert graph.find_entity(repository.entity_id) == repository
    assert graph.find_entity("missing") is None
    assert graph.find_relationship(relationship.relationship_id) == relationship
    assert graph.find_relationship("missing") is None


def test_knowledge_graph_returns_neighbors_outgoing_and_incoming():
    repository = make_entity("repo", KnowledgeEntityType.REPOSITORY)
    package = make_entity("sample", KnowledgeEntityType.PACKAGE)
    module = make_entity("sample.module", KnowledgeEntityType.MODULE)
    test = make_entity("test_module", KnowledgeEntityType.TEST)
    repository_contains_package = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        repository,
        package,
    )
    package_contains_module = make_relationship(
        KnowledgeRelationshipType.CONTAINS,
        package,
        module,
    )
    test_tests_module = make_relationship(
        KnowledgeRelationshipType.TESTS,
        test,
        module,
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(repository, package, module, test),
            relationships=(
                repository_contains_package,
                package_contains_module,
                test_tests_module,
            ),
        )
    )

    assert graph.outgoing(package.entity_id) == (package_contains_module,)
    assert graph.incoming(module.entity_id) == tuple(
        sorted(
            (
                package_contains_module,
                test_tests_module,
            ),
            key=lambda relationship: relationship.relationship_id,
        )
    )
    assert graph.neighbors(package.entity_id) == tuple(
        sorted(
            (
                module,
                repository,
            ),
            key=lambda entity: entity.entity_id,
        )
    )


def test_knowledge_graph_dependencies_and_dependents():
    service = make_entity("service", KnowledgeEntityType.SERVICE)
    module = make_entity("module", KnowledgeEntityType.MODULE)
    document = make_entity("document", KnowledgeEntityType.DOCUMENT)
    service_uses_module = make_relationship(
        KnowledgeRelationshipType.USES,
        service,
        module,
    )
    document_references_service = make_relationship(
        KnowledgeRelationshipType.REFERENCES,
        document,
        service,
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(service, module, document),
            relationships=(
                service_uses_module,
                document_references_service,
            ),
        )
    )

    assert graph.dependencies(service.entity_id) == (module,)
    assert graph.dependents(service.entity_id) == (document,)


def test_knowledge_graph_returns_deterministic_ordering():
    alpha = make_entity("alpha", KnowledgeEntityType.MODULE)
    zeta = make_entity("zeta", KnowledgeEntityType.MODULE)
    beta = make_entity("beta", KnowledgeEntityType.MODULE)
    alpha_uses_zeta = make_relationship(
        KnowledgeRelationshipType.USES,
        alpha,
        zeta,
    )
    alpha_uses_beta = make_relationship(
        KnowledgeRelationshipType.USES,
        alpha,
        beta,
    )
    graph = KnowledgeGraph.from_collection(
        KnowledgeCollection(
            entities=(zeta, alpha, beta),
            relationships=(alpha_uses_zeta, alpha_uses_beta),
        )
    )

    assert graph.entities() == tuple(
        sorted(graph.entities(), key=lambda entity: entity.entity_id)
    )
    assert graph.relationships() == tuple(
        sorted(
            graph.relationships(),
            key=lambda relationship: relationship.relationship_id,
        )
    )
    assert graph.dependencies(alpha.entity_id) == tuple(
        sorted(
            graph.dependencies(alpha.entity_id),
            key=lambda entity: entity.entity_id,
        )
    )
