from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping

from builder.reasoning.model import (
    ReasoningCollection,
    ReasoningResult,
    ReasoningSeverity,
)


@dataclass(frozen=True, slots=True)
class ReasoningRule:
    rule_id: str
    name: str
    description: str
    severity: ReasoningSeverity
    enabled: bool = True
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(frozen=True, slots=True)
class RuleViolation:
    violation_id: str
    rule_id: str
    message: str
    severity: ReasoningSeverity
    evidence_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        rule_id: str,
        message: str,
        severity: ReasoningSeverity,
        evidence_ids: tuple[str, ...],
        metadata: Mapping[str, str] | None = None,
    ) -> RuleViolation:
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            violation_id=_build_violation_id(
                rule_id=rule_id,
                message=message,
                severity=severity,
                evidence_ids=normalized_evidence_ids,
                metadata=normalized_metadata,
            ),
            rule_id=rule_id,
            message=message,
            severity=severity,
            evidence_ids=normalized_evidence_ids,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class RuleEvaluation:
    rule: ReasoningRule
    violations: tuple[RuleViolation, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "violations",
            tuple(
                sorted(
                    self.violations,
                    key=lambda violation: violation.violation_id,
                )
            ),
        )

    @property
    def passed(self) -> bool:
        return self.violation_count == 0

    @property
    def violation_count(self) -> int:
        return len(self.violations)


@dataclass(frozen=True, slots=True)
class RuleEngine:
    def evaluate(
        self,
        collection: ReasoningCollection,
        rules: tuple[ReasoningRule, ...],
    ) -> tuple[RuleEvaluation, ...]:
        return tuple(
            sorted(
                (
                    self.evaluate_rule(
                        collection,
                        rule,
                    )
                    for rule in rules
                ),
                key=lambda evaluation: evaluation.rule.rule_id,
            )
        )

    def evaluate_rule(
        self,
        collection: ReasoningCollection,
        rule: ReasoningRule,
    ) -> RuleEvaluation:
        if not rule.enabled:
            return RuleEvaluation(rule=rule)

        violations = self._violations_for_rule(
            collection,
            rule,
        )

        return RuleEvaluation(
            rule=rule,
            violations=violations,
        )

    def default_rules(self) -> tuple[ReasoningRule, ...]:
        return tuple(
            sorted(
                (
                    ReasoningRule(
                        rule_id="evidence_required",
                        name="Evidence Required",
                        description=(
                            "Reasoning results and inferences must cite "
                            "evidence."
                        ),
                        severity=ReasoningSeverity.ERROR,
                        metadata={"scope": "reasoning"},
                    ),
                    ReasoningRule(
                        rule_id="confidence_required",
                        name="Confidence Required",
                        description=(
                            "Reasoning results and inferences must have "
                            "positive confidence."
                        ),
                        severity=ReasoningSeverity.WARNING,
                        metadata={"scope": "reasoning"},
                    ),
                    ReasoningRule(
                        rule_id="no_error_severity_without_evidence",
                        name="No Error Severity Without Evidence",
                        description=(
                            "Error severity reasoning results must include "
                            "evidence."
                        ),
                        severity=ReasoningSeverity.ERROR,
                        metadata={"scope": "reasoning"},
                    ),
                ),
                key=lambda rule: rule.rule_id,
            )
        )

    def _violations_for_rule(
        self,
        collection: ReasoningCollection,
        rule: ReasoningRule,
    ) -> tuple[RuleViolation, ...]:
        if rule.rule_id == "evidence_required":
            return self._evidence_required_violations(
                collection,
                rule,
            )

        if rule.rule_id == "confidence_required":
            return self._confidence_required_violations(
                collection,
                rule,
            )

        if rule.rule_id == "no_error_severity_without_evidence":
            return self._error_without_evidence_violations(
                collection,
                rule,
            )

        return ()

    def _evidence_required_violations(
        self,
        collection: ReasoningCollection,
        rule: ReasoningRule,
    ) -> tuple[RuleViolation, ...]:
        violations: list[RuleViolation] = []

        for result in collection.results:
            if not result.evidence_ids:
                violations.append(
                    self._violation(
                        rule=rule,
                        result=result,
                        message=(
                            "Reasoning result must include evidence ids."
                        ),
                    )
                )
                continue

            for inference in result.inferences:
                if not inference.evidence_ids:
                    violations.append(
                        self._violation(
                            rule=rule,
                            result=result,
                            message=(
                                "Reasoning inference must include "
                                "evidence ids."
                            ),
                            metadata={
                                "inference_id": inference.inference_id,
                            },
                        )
                    )

        return tuple(violations)

    def _confidence_required_violations(
        self,
        collection: ReasoningCollection,
        rule: ReasoningRule,
    ) -> tuple[RuleViolation, ...]:
        violations: list[RuleViolation] = []

        for result in collection.results:
            if result.confidence <= 0.0:
                violations.append(
                    self._violation(
                        rule=rule,
                        result=result,
                        message=(
                            "Reasoning result must have positive "
                            "confidence."
                        ),
                    )
                )
                continue

            for inference in result.inferences:
                if inference.confidence <= 0.0:
                    violations.append(
                        self._violation(
                            rule=rule,
                            result=result,
                            message=(
                                "Reasoning inference must have positive "
                                "confidence."
                            ),
                            metadata={
                                "inference_id": inference.inference_id,
                            },
                        )
                    )

        return tuple(violations)

    def _error_without_evidence_violations(
        self,
        collection: ReasoningCollection,
        rule: ReasoningRule,
    ) -> tuple[RuleViolation, ...]:
        return tuple(
            self._violation(
                rule=rule,
                result=result,
                message=(
                    "Error severity reasoning result must include "
                    "evidence ids."
                ),
            )
            for result in collection.results
            if result.severity == ReasoningSeverity.ERROR
            and not result.evidence_ids
        )

    def _violation(
        self,
        rule: ReasoningRule,
        result: ReasoningResult,
        message: str,
        metadata: Mapping[str, str] | None = None,
    ) -> RuleViolation:
        normalized_metadata = {
            "result_id": result.result_id,
        }
        normalized_metadata.update(metadata or {})

        return RuleViolation.create(
            rule_id=rule.rule_id,
            message=message,
            severity=rule.severity,
            evidence_ids=result.evidence_ids,
            metadata=normalized_metadata,
        )


def _build_violation_id(
    rule_id: str,
    message: str,
    severity: ReasoningSeverity,
    evidence_ids: tuple[str, ...],
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            rule_id,
            message,
            severity.value,
            ";".join(evidence_ids),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _metadata_text(
    metadata: Mapping[str, str],
) -> str:
    return ";".join(
        f"{key}={metadata[key]}"
        for key in sorted(metadata)
    )
