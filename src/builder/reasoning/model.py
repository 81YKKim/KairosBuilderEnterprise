from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping


class ReasoningType(StrEnum):
    INFERENCE = "inference"
    RULE = "rule"
    CONSTRAINT = "constraint"
    CONFIDENCE = "confidence"
    CONFLICT = "conflict"
    EXPLANATION = "explanation"


class ReasoningSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class ReasoningEvidence:
    evidence_id: str
    source_id: str
    summary: str


@dataclass(frozen=True, slots=True)
class Inference:
    inference_id: str
    inference_type: ReasoningType
    subject: str
    predicate: str
    object: str
    evidence_ids: tuple[str, ...]
    confidence: float
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        inference_type: ReasoningType,
        subject: str,
        predicate: str,
        object: str,
        evidence_ids: tuple[str, ...],
        confidence: float,
        metadata: Mapping[str, str] | None = None,
    ) -> Inference:
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            inference_id=_build_inference_id(
                inference_type=inference_type,
                subject=subject,
                predicate=predicate,
                object=object,
                evidence_ids=normalized_evidence_ids,
                confidence=confidence,
                metadata=normalized_metadata,
            ),
            inference_type=inference_type,
            subject=subject,
            predicate=predicate,
            object=object,
            evidence_ids=normalized_evidence_ids,
            confidence=confidence,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class ReasoningResult:
    result_id: str
    reasoning_type: ReasoningType
    summary: str
    inferences: tuple[Inference, ...]
    severity: ReasoningSeverity
    confidence: float
    evidence_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        reasoning_type: ReasoningType,
        summary: str,
        inferences: tuple[Inference, ...],
        severity: ReasoningSeverity,
        confidence: float,
        evidence_ids: tuple[str, ...],
        metadata: Mapping[str, str] | None = None,
    ) -> ReasoningResult:
        normalized_inferences = _sort_inferences(inferences)
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            result_id=_build_result_id(
                reasoning_type=reasoning_type,
                summary=summary,
                inferences=normalized_inferences,
                severity=severity,
                confidence=confidence,
                evidence_ids=normalized_evidence_ids,
                metadata=normalized_metadata,
            ),
            reasoning_type=reasoning_type,
            summary=summary,
            inferences=normalized_inferences,
            severity=severity,
            confidence=confidence,
            evidence_ids=normalized_evidence_ids,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class ReasoningCollection:
    results: tuple[ReasoningResult, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "results",
            tuple(
                sorted(
                    self.results,
                    key=lambda result: result.result_id,
                )
            ),
        )

    @property
    def count(self) -> int:
        return len(self.results)

    def by_type(
        self,
        reasoning_type: ReasoningType,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                result
                for result in self.results
                if result.reasoning_type == reasoning_type
            )
        )

    def errors(self) -> ReasoningCollection:
        return self._by_severity(ReasoningSeverity.ERROR)

    def warnings(self) -> ReasoningCollection:
        return self._by_severity(ReasoningSeverity.WARNING)

    def infos(self) -> ReasoningCollection:
        return self._by_severity(ReasoningSeverity.INFO)

    def high_confidence(
        self,
        threshold: float,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                result
                for result in self.results
                if result.confidence >= threshold
            )
        )

    def low_confidence(
        self,
        threshold: float,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                result
                for result in self.results
                if result.confidence <= threshold
            )
        )

    def _by_severity(
        self,
        severity: ReasoningSeverity,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                result
                for result in self.results
                if result.severity == severity
            )
        )


def _build_inference_id(
    inference_type: ReasoningType,
    subject: str,
    predicate: str,
    object: str,
    evidence_ids: tuple[str, ...],
    confidence: float,
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            inference_type.value,
            subject,
            predicate,
            object,
            ";".join(evidence_ids),
            _confidence_text(confidence),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _build_result_id(
    reasoning_type: ReasoningType,
    summary: str,
    inferences: tuple[Inference, ...],
    severity: ReasoningSeverity,
    confidence: float,
    evidence_ids: tuple[str, ...],
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            reasoning_type.value,
            summary,
            _inference_ids_text(inferences),
            severity.value,
            _confidence_text(confidence),
            ";".join(evidence_ids),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _sort_inferences(
    inferences: tuple[Inference, ...],
) -> tuple[Inference, ...]:
    return tuple(
        sorted(
            inferences,
            key=lambda inference: inference.inference_id,
        )
    )


def _inference_ids_text(
    inferences: tuple[Inference, ...],
) -> str:
    return ";".join(
        inference.inference_id
        for inference in inferences
    )


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
