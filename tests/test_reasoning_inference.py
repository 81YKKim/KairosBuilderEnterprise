from pathlib import Path

from builder.knowledge.integration import KnowledgePlatform
from builder.knowledge.model import (
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)
from builder.reasoning.inference import InferenceEngine
from builder.reasoning.model import (
    ReasoningCollection,
    ReasoningSeverity,
    ReasoningType,
)
from builder.repository.integration import RepositoryPlatform


def create_sample_repository(root: Path) -> None:
    source = root / "src" / "sample"
    tests = root / "tests"

    source.mkdir(parents=True)
    tests.mkdir()
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "alpha.py").write_text("", encoding="utf-8")
    (tests / "test_alpha.py").write_text("", encoding="utf-8")


def build_knowledge_platform(tmp_path: Path) -> KnowledgePlatform:
    repository = tmp_path / "sample_repo"
    create_sample_repository(repository)

    return KnowledgePlatform.build(
        RepositoryPlatform.create(repository)
    )


def test_inference_engine_creation():
    engine = InferenceEngine()

    assert isinstance(engine, InferenceEngine)


def test_inference_engine_infers_entities(tmp_path):
    platform = build_knowledge_platform(tmp_path)
    engine = InferenceEngine()

    result = engine.infer_entities(platform)

    assert isinstance(result, ReasoningCollection)
    assert result.count == len(platform.entities())
    assert all(
        item.reasoning_type == ReasoningType.INFERENCE
        for item in result.results
    )
    assert all(
        item.severity == ReasoningSeverity.INFO
        for item in result.results
    )
    assert {
        inference.predicate
        for item in result.results
        for inference in item.inferences
    } == {"exists"}


def test_inference_engine_infers_relationships(tmp_path):
    platform = build_knowledge_platform(tmp_path)
    engine = InferenceEngine()

    result = engine.infer_relationships(platform)

    assert result.count == len(platform.relationships())
    assert {
        inference.predicate
        for item in result.results
        for inference in item.inferences
    } == {"contains"}


def test_inference_engine_marks_dependency_relationship():
    platform = build_manual_platform(KnowledgeRelationshipType.DEPENDS_ON)
    result = InferenceEngine().infer_relationships(platform)
    inference = result.results[0].inferences[0]

    assert inference.predicate == "depends_on"
    assert result.results[0].metadata["relationship_kind"] == "dependency"


def test_inference_engine_marks_test_relationship():
    platform = build_manual_platform(KnowledgeRelationshipType.TESTS)
    result = InferenceEngine().infer_relationships(platform)
    inference = result.results[0].inferences[0]

    assert inference.predicate == "tests"
    assert result.results[0].metadata["relationship_kind"] == "test"


def test_inference_engine_marks_contains_relationship(tmp_path):
    platform = build_knowledge_platform(tmp_path)
    result = InferenceEngine().infer_relationships(platform)

    assert {
        item.metadata["relationship_kind"]
        for item in result.results
    } == {"contains"}


def test_inference_engine_infer_all_combines_entity_and_relationship_results(
    tmp_path,
):
    platform = build_knowledge_platform(tmp_path)
    engine = InferenceEngine()

    result = engine.infer_all(platform)

    assert result.count == len(platform.entities()) + len(
        platform.relationships()
    )


def test_inference_engine_returns_deterministic_ordering_and_stable_ids(
    tmp_path,
):
    platform = build_knowledge_platform(tmp_path)
    engine = InferenceEngine()

    first = engine.infer_all(platform)
    second = engine.infer_all(platform)

    assert [item.result_id for item in first.results] == [
        item.result_id for item in second.results
    ]
    assert first.results == tuple(
        sorted(
            first.results,
            key=lambda item: item.result_id,
        )
    )


def build_manual_platform(
    relationship_type: KnowledgeRelationshipType,
) -> KnowledgePlatform:
    from builder.evidence.model import EvidenceCollection
    from builder.knowledge.cache import KnowledgeCache
    from builder.knowledge.extractor import KnowledgeExtractor
    from builder.knowledge.graph import KnowledgeGraph
    from builder.knowledge.model import (
        KnowledgeCollection,
        KnowledgeEntity,
        KnowledgeEntityType,
        KnowledgeRelationship,
    )
    from builder.knowledge.query import KnowledgeQuery

    source = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="source",
        summary="Source module.",
        evidence_ids=("evidence:source",),
    )
    target = KnowledgeEntity.create(
        entity_type=KnowledgeEntityType.MODULE,
        name="target",
        summary="Target module.",
        evidence_ids=("evidence:target",),
    )
    relationship = KnowledgeRelationship.create(
        relationship_type=relationship_type,
        source_entity_id=source.entity_id,
        target_entity_id=target.entity_id,
        evidence_ids=("evidence:relationship",),
    )
    knowledge = KnowledgeCollection(
        entities=(source, target),
        relationships=(relationship,),
    )
    graph = KnowledgeGraph.from_collection(knowledge)

    return KnowledgePlatform(
        repository_platform=None,
        evidence_extractor=None,
        evidence=EvidenceCollection(),
        knowledge_extractor=KnowledgeExtractor(),
        knowledge=knowledge,
        graph=graph,
        query=KnowledgeQuery(graph),
        cache=KnowledgeCache.create(graph),
    )
