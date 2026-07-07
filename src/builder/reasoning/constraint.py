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
class ReasoningConstraint:
    constraint_id: str
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
class ConstraintViolation:
    violation_id: str
    constraint_id: str
    message: str
    severity: ReasoningSeverity
    evidence_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        constraint_id: str,
        message: str,
        severity: ReasoningSeverity,
        evidence_ids: tuple[str, ...],
        metadata: Mapping[str, str] | None = None,
    ) -> ConstraintViolation:
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            violation_id=_build_violation_id(
                constraint_id=constraint_id,
                message=message,
                severity=severity,
                evidence_ids=normalized_evidence_ids,
                metadata=normalized_metadata,
            ),
            constraint_id=constraint_id,
            message=message,
            severity=severity,
            evidence_ids=normalized_evidence_ids,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class ConstraintEvaluation:
    constraint: ReasoningConstraint
    violations: tuple[ConstraintViolation, ...] = ()

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
class ConstraintEngine:
    def evaluate(
        self,
        collection: ReasoningCollection,
        constraints: tuple[ReasoningConstraint, ...],
    ) -> tuple[ConstraintEvaluation, ...]:
        return tuple(
            sorted(
                (
                    self.evaluate_constraint(
                        collection,
                        constraint,
                    )
                    for constraint in constraints
                ),
                key=lambda evaluation: evaluation.constraint.constraint_id,
            )
        )

    def evaluate_constraint(
        self,
        collection: ReasoningCollection,
        constraint: ReasoningConstraint,
    ) -> ConstraintEvaluation:
        if not constraint.enabled:
            return ConstraintEvaluation(constraint=constraint)

        violations = self._violations_for_constraint(
            collection,
            constraint,
        )

        return ConstraintEvaluation(
            constraint=constraint,
            violations=violations,
        )

    def default_constraints(self) -> tuple[ReasoningConstraint, ...]:
        return tuple(
            sorted(
                (
                    ReasoningConstraint(
                        constraint_id="minimum_confidence",
                        name="Minimum Confidence",
                        description=(
                            "Reasoning results and inferences must meet "
                            "the minimum confidence threshold."
                        ),
                        severity=ReasoningSeverity.WARNING,
                        metadata={
                            "threshold": "0.5",
                        },
                    ),
                    ReasoningConstraint(
                        constraint_id="no_error_without_evidence",
                        name="No Error Without Evidence",
                        description=(
                            "Error severity reasoning results must cite "
                            "evidence."
                        ),
                        severity=ReasoningSeverity.ERROR,
                        metadata={"scope": "reasoning"},
                    ),
                    ReasoningConstraint(
                        constraint_id="no_empty_reasoning_summary",
                        name="No Empty Reasoning Summary",
                        description=(
                            "Reasoning results must provide a non-empty "
                            "summary."
                        ),
                        severity=ReasoningSeverity.WARNING,
                        metadata={"scope": "reasoning"},
                    ),
                ),
                key=lambda constraint: constraint.constraint_id,
            )
        )

    def _violations_for_constraint(
        self,
        collection: ReasoningCollection,
        constraint: ReasoningConstraint,
    ) -> tuple[ConstraintViolation, ...]:
        if constraint.constraint_id == "minimum_confidence":
            return self._minimum_confidence_violations(
                collection,
                constraint,
            )

        if constraint.constraint_id == "no_error_without_evidence":
            return self._error_without_evidence_violations(
                collection,
                constraint,
            )

        if constraint.constraint_id == "no_empty_reasoning_summary":
            return self._empty_summary_violations(
                collection,
                constraint,
            )

        return ()

    def _minimum_confidence_violations(
        self,
        collection: ReasoningCollection,
        constraint: ReasoningConstraint,
    ) -> tuple[ConstraintViolation, ...]:
        threshold = _threshold(constraint)
        violations: list[ConstraintViolation] = []

        for result in collection.results:
            if result.confidence < threshold:
                violations.append(
                    self._violation(
                        constraint=constraint,
                        result=result,
                        message=(
                            "Reasoning result confidence is below "
                            "minimum threshold."
                        ),
                        metadata={
                            "threshold": _confidence_text(threshold),
                            "confidence": _confidence_text(
                                result.confidence
                            ),
                        },
                    )
                )
                continue

            for inference in result.inferences:
                if inference.confidence < threshold:
                    violations.append(
                        self._violation(
                            constraint=constraint,
                            result=result,
                            message=(
                                "Reasoning inference confidence is below "
                                "minimum threshold."
                            ),
                            metadata={
                                "inference_id": inference.inference_id,
                                "threshold": _confidence_text(threshold),
                                "confidence": _confidence_text(
                                    inference.confidence
                                ),
                            },
                        )
                    )

        return tuple(violations)

    def _error_without_evidence_violations(
        self,
        collection: ReasoningCollection,
        constraint: ReasoningConstraint,
    ) -> tuple[ConstraintViolation, ...]:
        return tuple(
            self._violation(
                constraint=constraint,
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

    def _empty_summary_violations(
        self,
        collection: ReasoningCollection,
        constraint: ReasoningConstraint,
    ) -> tuple[ConstraintViolation, ...]:
        return tuple(
            self._violation(
                constraint=constraint,
                result=result,
                message="Reasoning result summary must not be empty.",
            )
            for result in collection.results
            if not result.summary.strip()
        )

    def _violation(
        self,
        constraint: ReasoningConstraint,
        result: ReasoningResult,
        message: str,
        metadata: Mapping[str, str] | None = None,
    ) -> ConstraintViolation:
        normalized_metadata = {
            "result_id": result.result_id,
        }
        normalized_metadata.update(metadata or {})

        return ConstraintViolation.create(
            constraint_id=constraint.constraint_id,
            message=message,
            severity=constraint.severity,
            evidence_ids=result.evidence_ids,
            metadata=normalized_metadata,
        )


def _threshold(
    constraint: ReasoningConstraint,
) -> float:
    return float(constraint.metadata.get("threshold", "0.5"))


def _build_violation_id(
    constraint_id: str,
    message: str,
    severity: ReasoningSeverity,
    evidence_ids: tuple[str, ...],
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            constraint_id,
            message,
            severity.value,
            ";".join(evidence_ids),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _confidence_text(
    confidence: float,
) -> str:
    return f"{confidence:.6f}"


def _metadata_text(
    metadata: Mapping[str, str],
) -> str:
    return ";".join(
        f"{key}={metadata[key]}"
        for key in sorted(metadata)
    )
