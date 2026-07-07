from dataclasses import FrozenInstanceError

import pytest

from builder.reasoning.model import (
    Inference,
    ReasoningCollection,
    ReasoningResult,
    ReasoningSeverity,
    ReasoningType,
)
from builder.reasoning.rule import (
    ReasoningRule,
    RuleEngine,
    RuleEvaluation,
    RuleViolation,
)


def test_reasoning_rule_creation():
    rule = ReasoningRule(
        rule_id="evidence_required",
        name="Evidence Required",
        description="Reasoning results must cite evidence.",
        severity=ReasoningSeverity.ERROR,
        enabled=True,
        metadata={"source": "default"},
    )

    assert rule.rule_id == "evidence_required"
    assert rule.name == "Evidence Required"
    assert rule.enabled is True
    assert rule.metadata == {"source": "default"}


def test_rule_violation_creation_uses_stable_violation_id():
    first = RuleViolation.create(
        rule_id="evidence_required",
        message="Missing evidence.",
        severity=ReasoningSeverity.ERROR,
        evidence_ids=("evidence-b", "evidence-a"),
        metadata={"target": "result-001"},
    )
    second = RuleViolation.create(
        rule_id="evidence_required",
        message="Missing evidence.",
        severity=ReasoningSeverity.ERROR,
        evidence_ids=("evidence-a", "evidence-b"),
        metadata={"target": "result-001"},
    )

    assert first.violation_id == second.violation_id
    assert first.evidence_ids == ("evidence-a", "evidence-b")
    assert first.metadata == {"target": "result-001"}


def test_rule_engine_default_rules():
    rules = RuleEngine().default_rules()

    assert [rule.rule_id for rule in rules] == [
        "confidence_required",
        "evidence_required",
        "no_error_severity_without_evidence",
    ]
    assert all(rule.enabled for rule in rules)


def test_rule_engine_evaluates_passing_collection():
    collection = ReasoningCollection(
        results=(make_result("supported", ("evidence-001",), 0.9),)
    )

    evaluations = RuleEngine().evaluate(
        collection,
        RuleEngine().default_rules(),
    )

    assert all(evaluation.passed for evaluation in evaluations)
    assert sum(evaluation.violation_count for evaluation in evaluations) == 0


def test_rule_engine_evaluates_evidence_required_violation():
    collection = ReasoningCollection(
        results=(make_result("unsupported", (), 0.9),)
    )
    rule = next(
        rule
        for rule in RuleEngine().default_rules()
        if rule.rule_id == "evidence_required"
    )

    evaluation = RuleEngine().evaluate_rule(collection, rule)

    assert isinstance(evaluation, RuleEvaluation)
    assert evaluation.passed is False
    assert evaluation.violation_count == 1
    assert evaluation.violations[0].rule_id == "evidence_required"
    assert evaluation.violations[0].severity == ReasoningSeverity.ERROR


def test_rule_engine_evaluates_confidence_required_violation():
    collection = ReasoningCollection(
        results=(make_result("unsupported-confidence", ("evidence-001",), 0.0),)
    )
    rule = next(
        rule
        for rule in RuleEngine().default_rules()
        if rule.rule_id == "confidence_required"
    )

    evaluation = RuleEngine().evaluate_rule(collection, rule)

    assert evaluation.passed is False
    assert evaluation.violation_count == 1
    assert evaluation.violations[0].rule_id == "confidence_required"
    assert evaluation.violations[0].metadata["result_id"]


def test_rule_engine_skips_disabled_rule():
    collection = ReasoningCollection(
        results=(make_result("unsupported", (), 0.0),)
    )
    rule = ReasoningRule(
        rule_id="evidence_required",
        name="Evidence Required",
        description="Disabled test rule.",
        severity=ReasoningSeverity.ERROR,
        enabled=False,
    )

    evaluation = RuleEngine().evaluate_rule(collection, rule)

    assert evaluation.passed is True
    assert evaluation.violation_count == 0
    assert evaluation.violations == ()


def test_rule_engine_returns_deterministic_ordering_and_stable_ids():
    collection = ReasoningCollection(
        results=(
            make_result("zeta", (), 0.0),
            make_result("alpha", (), 0.0),
        )
    )
    rule = next(
        rule
        for rule in RuleEngine().default_rules()
        if rule.rule_id == "evidence_required"
    )

    first = RuleEngine().evaluate_rule(collection, rule)
    second = RuleEngine().evaluate_rule(collection, rule)

    assert [violation.violation_id for violation in first.violations] == [
        violation.violation_id for violation in second.violations
    ]
    assert first.violations == tuple(
        sorted(
            first.violations,
            key=lambda violation: violation.violation_id,
        )
    )


def test_reasoning_rule_models_are_immutable():
    rule = ReasoningRule(
        rule_id="evidence_required",
        name="Evidence Required",
        description="Reasoning results must cite evidence.",
        severity=ReasoningSeverity.ERROR,
    )
    violation = RuleViolation.create(
        rule_id=rule.rule_id,
        message="Missing evidence.",
        severity=ReasoningSeverity.ERROR,
        evidence_ids=(),
    )
    evaluation = RuleEvaluation(
        rule=rule,
        violations=(violation,),
    )

    with pytest.raises(FrozenInstanceError):
        rule.name = "Changed"

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
        subject=name,
        predicate="exists",
        object="module",
        evidence_ids=evidence_ids,
        confidence=confidence,
    )

    return ReasoningResult.create(
        reasoning_type=ReasoningType.INFERENCE,
        summary=f"{name} exists",
        inferences=(inference,),
        severity=severity,
        confidence=confidence,
        evidence_ids=evidence_ids,
    )
