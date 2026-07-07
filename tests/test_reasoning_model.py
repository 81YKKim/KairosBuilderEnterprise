from dataclasses import FrozenInstanceError

import pytest

from builder.reasoning.model import (
    Inference,
    ReasoningCollection,
    ReasoningEvidence,
    ReasoningResult,
    ReasoningSeverity,
    ReasoningType,
)


def test_reasoning_evidence_creation():
    evidence = ReasoningEvidence(
        evidence_id="evidence-001",
        source_id="module:builder.knowledge.integration",
        summary="KnowledgePlatform exists.",
    )

    assert evidence.evidence_id == "evidence-001"
    assert evidence.source_id == "module:builder.knowledge.integration"
    assert evidence.summary == "KnowledgePlatform exists."


def test_inference_creation_uses_stable_inference_id():
    first = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject="KnowledgePlatform",
        predicate="provides",
        object="single public entry point",
        evidence_ids=("evidence-b", "evidence-a"),
        confidence=0.9,
        metadata={
            "epic": "EPIC-02",
            "layer": "knowledge",
        },
    )
    second = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject="KnowledgePlatform",
        predicate="provides",
        object="single public entry point",
        evidence_ids=("evidence-a", "evidence-b"),
        confidence=0.9,
        metadata={
            "layer": "knowledge",
            "epic": "EPIC-02",
        },
    )

    assert first.inference_id == second.inference_id
    assert first.inference_type == ReasoningType.INFERENCE
    assert first.evidence_ids == ("evidence-a", "evidence-b")
    assert first.metadata == {
        "epic": "EPIC-02",
        "layer": "knowledge",
    }


def test_reasoning_result_creation_uses_stable_result_id():
    inference = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject="RepositoryPlatform",
        predicate="feeds",
        object="KnowledgePlatform",
        evidence_ids=("evidence-platform",),
        confidence=0.8,
    )
    first = ReasoningResult.create(
        reasoning_type=ReasoningType.EXPLANATION,
        summary="KnowledgePlatform is supported by RepositoryPlatform.",
        inferences=(inference,),
        severity=ReasoningSeverity.INFO,
        confidence=0.8,
        evidence_ids=("evidence-b", "evidence-a"),
        metadata={
            "source": "reasoning-model-test",
        },
    )
    second = ReasoningResult.create(
        reasoning_type=ReasoningType.EXPLANATION,
        summary="KnowledgePlatform is supported by RepositoryPlatform.",
        inferences=(inference,),
        severity=ReasoningSeverity.INFO,
        confidence=0.8,
        evidence_ids=("evidence-a", "evidence-b"),
        metadata={
            "source": "reasoning-model-test",
        },
    )

    assert first.result_id == second.result_id
    assert first.reasoning_type == ReasoningType.EXPLANATION
    assert first.inferences == (inference,)
    assert first.evidence_ids == ("evidence-a", "evidence-b")


def test_reasoning_collection_counts_and_filters():
    info = make_result(
        ReasoningType.INFERENCE,
        ReasoningSeverity.INFO,
        0.95,
        "info",
    )
    warning = make_result(
        ReasoningType.CONFLICT,
        ReasoningSeverity.WARNING,
        0.45,
        "warning",
    )
    error = make_result(
        ReasoningType.CONSTRAINT,
        ReasoningSeverity.ERROR,
        0.2,
        "error",
    )

    collection = ReasoningCollection(results=(warning, error, info))

    assert collection.count == 3
    assert collection.by_type(ReasoningType.INFERENCE).results == (info,)
    assert collection.errors().results == (error,)
    assert collection.warnings().results == (warning,)
    assert collection.infos().results == (info,)
    assert collection.high_confidence(0.8).results == (info,)
    assert collection.low_confidence(0.5).results == tuple(
        sorted(
            (warning, error),
            key=lambda result: result.result_id,
        )
    )


def test_reasoning_collection_returns_deterministic_ordering():
    zeta = make_result(
        ReasoningType.INFERENCE,
        ReasoningSeverity.INFO,
        0.7,
        "zeta",
    )
    alpha = make_result(
        ReasoningType.INFERENCE,
        ReasoningSeverity.INFO,
        0.7,
        "alpha",
    )

    collection = ReasoningCollection(results=(zeta, alpha))

    assert collection.results == tuple(
        sorted(
            collection.results,
            key=lambda result: result.result_id,
        )
    )


def test_reasoning_models_are_immutable():
    evidence = ReasoningEvidence(
        evidence_id="evidence-001",
        source_id="source",
        summary="summary",
    )
    inference = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject="subject",
        predicate="predicate",
        object="object",
        evidence_ids=("evidence-001",),
        confidence=0.9,
    )
    result = ReasoningResult.create(
        reasoning_type=ReasoningType.INFERENCE,
        summary="summary",
        inferences=(inference,),
        severity=ReasoningSeverity.INFO,
        confidence=0.9,
        evidence_ids=("evidence-001",),
    )
    collection = ReasoningCollection(results=(result,))

    with pytest.raises(FrozenInstanceError):
        evidence.summary = "changed"

    with pytest.raises(FrozenInstanceError):
        inference.subject = "changed"

    with pytest.raises(FrozenInstanceError):
        result.summary = "changed"

    with pytest.raises(FrozenInstanceError):
        collection.results = ()


def make_result(
    reasoning_type: ReasoningType,
    severity: ReasoningSeverity,
    confidence: float,
    name: str,
) -> ReasoningResult:
    inference = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject=name,
        predicate="supports",
        object="reasoning",
        evidence_ids=(f"evidence:{name}",),
        confidence=confidence,
    )

    return ReasoningResult.create(
        reasoning_type=reasoning_type,
        summary=f"{name} result",
        inferences=(inference,),
        severity=severity,
        confidence=confidence,
        evidence_ids=(f"evidence:{name}",),
    )
