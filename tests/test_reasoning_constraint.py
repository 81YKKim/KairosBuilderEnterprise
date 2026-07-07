from dataclasses import FrozenInstanceError

import pytest

from builder.reasoning.constraint import (
    ConstraintEngine,
    ConstraintEvaluation,
    ConstraintViolation,
    ReasoningConstraint,
)
from builder.reasoning.model import (
    Inference,
    ReasoningCollection,
    ReasoningResult,
    ReasoningSeverity,
    ReasoningType,
)


def test_reasoning_constraint_creation():
    constraint = ReasoningConstraint(
        constraint_id="minimum_confidence",
        name="Minimum Confidence",
        description="Reasoning confidence must meet the minimum threshold.",
        severity=ReasoningSeverity.WARNING,
        enabled=True,
        metadata={"threshold": "0.5"},
    )

    assert constraint.constraint_id == "minimum_confidence"
    assert constraint.name == "Minimum Confidence"
    assert constraint.enabled is True
    assert constraint.metadata == {"threshold": "0.5"}


def test_constraint_violation_creation_uses_stable_violation_id():
    first = ConstraintViolation.create(
        constraint_id="minimum_confidence",
        message="Confidence is below threshold.",
        severity=ReasoningSeverity.WARNING,
        evidence_ids=("evidence-b", "evidence-a"),
        metadata={"target": "result-001"},
    )
    second = ConstraintViolation.create(
        constraint_id="minimum_confidence",
        message="Confidence is below threshold.",
        severity=ReasoningSeverity.WARNING,
        evidence_ids=("evidence-a", "evidence-b"),
        metadata={"target": "result-001"},
    )

    assert first.violation_id == second.violation_id
    assert first.evidence_ids == ("evidence-a", "evidence-b")
    assert first.metadata == {"target": "result-001"}


def test_constraint_engine_default_constraints():
    constraints = ConstraintEngine().default_constraints()

    assert [constraint.constraint_id for constraint in constraints] == [
        "minimum_confidence",
        "no_empty_reasoning_summary",
        "no_error_without_evidence",
    ]
    assert all(constraint.enabled for constraint in constraints)


def test_constraint_engine_evaluates_passing_collection():
    collection = ReasoningCollection(
        results=(make_result("supported", ("evidence-001",), 0.9),)
    )

    evaluations = ConstraintEngine().evaluate(
        collection,
        ConstraintEngine().default_constraints(),
    )

    assert all(evaluation.passed for evaluation in evaluations)
    assert sum(evaluation.violation_count for evaluation in evaluations) == 0


def test_constraint_engine_evaluates_minimum_confidence_violation():
    collection = ReasoningCollection(
        results=(make_result("low-confidence", ("evidence-001",), 0.2),)
    )
    constraint = next(
        constraint
        for constraint in ConstraintEngine().default_constraints()
        if constraint.constraint_id == "minimum_confidence"
    )

    evaluation = ConstraintEngine().evaluate_constraint(
        collection,
        constraint,
    )

    assert isinstance(evaluation, ConstraintEvaluation)
    assert evaluation.passed is False
    assert evaluation.violation_count == 1
    assert evaluation.violations[0].constraint_id == "minimum_confidence"
    assert evaluation.violations[0].severity == ReasoningSeverity.WARNING


def test_constraint_engine_evaluates_no_error_without_evidence_violation():
    collection = ReasoningCollection(
        results=(
            make_result(
                "error-without-evidence",
                (),
                0.9,
                severity=ReasoningSeverity.ERROR,
            ),
        )
    )
    constraint = next(
        constraint
        for constraint in ConstraintEngine().default_constraints()
        if constraint.constraint_id == "no_error_without_evidence"
    )

    evaluation = ConstraintEngine().evaluate_constraint(
        collection,
        constraint,
    )

    assert evaluation.passed is False
    assert evaluation.violation_count == 1
    assert evaluation.violations[0].constraint_id == (
        "no_error_without_evidence"
    )
    assert evaluation.violations[0].severity == ReasoningSeverity.ERROR


def test_constraint_engine_evaluates_no_empty_reasoning_summary_violation():
    collection = ReasoningCollection(
        results=(make_result("", ("evidence-001",), 0.9),)
    )
    constraint = next(
        constraint
        for constraint in ConstraintEngine().default_constraints()
        if constraint.constraint_id == "no_empty_reasoning_summary"
    )

    evaluation = ConstraintEngine().evaluate_constraint(
        collection,
        constraint,
    )

    assert evaluation.passed is False
    assert evaluation.violation_count == 1
    assert evaluation.violations[0].constraint_id == (
        "no_empty_reasoning_summary"
    )


def test_constraint_engine_skips_disabled_constraint():
    collection = ReasoningCollection(
        results=(make_result("low-confidence", ("evidence-001",), 0.0),)
    )
    constraint = ReasoningConstraint(
        constraint_id="minimum_confidence",
        name="Minimum Confidence",
        description="Disabled test constraint.",
        severity=ReasoningSeverity.WARNING,
        enabled=False,
    )

    evaluation = ConstraintEngine().evaluate_constraint(
        collection,
        constraint,
    )

    assert evaluation.passed is True
    assert evaluation.violation_count == 0
    assert evaluation.violations == ()


def test_constraint_engine_returns_deterministic_ordering_and_stable_ids():
    collection = ReasoningCollection(
        results=(
            make_result("zeta", ("evidence-zeta",), 0.0),
            make_result("alpha", ("evidence-alpha",), 0.0),
        )
    )
    constraint = next(
        constraint
        for constraint in ConstraintEngine().default_constraints()
        if constraint.constraint_id == "minimum_confidence"
    )

    first = ConstraintEngine().evaluate_constraint(collection, constraint)
    second = ConstraintEngine().evaluate_constraint(collection, constraint)

    assert [violation.violation_id for violation in first.violations] == [
        violation.violation_id for violation in second.violations
    ]
    assert first.violations == tuple(
        sorted(
            first.violations,
            key=lambda violation: violation.violation_id,
        )
    )


def test_reasoning_constraint_models_are_immutable():
    constraint = ReasoningConstraint(
        constraint_id="minimum_confidence",
        name="Minimum Confidence",
        description="Reasoning confidence must meet the minimum threshold.",
        severity=ReasoningSeverity.WARNING,
    )
    violation = ConstraintViolation.create(
        constraint_id=constraint.constraint_id,
        message="Confidence is below threshold.",
        severity=ReasoningSeverity.WARNING,
        evidence_ids=(),
    )
    evaluation = ConstraintEvaluation(
        constraint=constraint,
        violations=(violation,),
    )

    with pytest.raises(FrozenInstanceError):
        constraint.name = "Changed"

    with pytest.raises(FrozenInstanceError):
        violation.message = "Changed"

    with pytest.raises(FrozenInstanceError):
        evaluation.violations = ()


def make_result(
    name: str,
    evidence_ids: tuple[str, ...],
    confidence: float,
    severity: ReasoningSeverity = ReasoningSeverity.INFO,
) -> ReasoningResult:
    inference = Inference.create(
        inference_type=ReasoningType.INFERENCE,
        subject=name or "empty",
        predicate="exists",
        object="module",
        evidence_ids=evidence_ids,
        confidence=confidence,
    )
    summary = f"{name} exists" if name else ""

    return ReasoningResult.create(
        reasoning_type=ReasoningType.INFERENCE,
        summary=summary,
        inferences=(inference,),
        severity=severity,
        confidence=confidence,
        evidence_ids=evidence_ids,
    )
