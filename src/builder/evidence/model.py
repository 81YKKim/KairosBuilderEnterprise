from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


class EvidenceType(StrEnum):
    REPOSITORY = "repository"
    PACKAGE = "package"
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    IMPORT = "import"
    TEST = "test"
    GENERATOR = "generator"
    DOCUMENT = "document"


class EvidenceSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class EvidenceSource:
    source_id: str
    source_type: EvidenceType
    path: Path
    name: str


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    evidence_type: EvidenceType
    source: EvidenceSource
    summary: str
    details: str
    severity: EvidenceSeverity
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        evidence_type: EvidenceType,
        source: EvidenceSource,
        summary: str,
        details: str,
        severity: EvidenceSeverity,
        metadata: Mapping[str, str] | None = None,
    ) -> Evidence:
        normalized_metadata = dict(metadata or {})

        return cls(
            evidence_id=_build_evidence_id(
                evidence_type=evidence_type,
                source=source,
                summary=summary,
                details=details,
                severity=severity,
                metadata=normalized_metadata,
            ),
            evidence_type=evidence_type,
            source=source,
            summary=summary,
            details=details,
            severity=severity,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class EvidenceCollection:
    items: tuple[Evidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "items",
            tuple(
                sorted(
                    self.items,
                    key=lambda item: item.evidence_id,
                )
            ),
        )

    @property
    def count(self) -> int:
        return len(self.items)

    def by_type(
        self,
        evidence_type: EvidenceType,
    ) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                item
                for item in self.items
                if item.evidence_type == evidence_type
            )
        )

    def by_source(
        self,
        source_id: str,
    ) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                item
                for item in self.items
                if item.source.source_id == source_id
            )
        )

    def errors(self) -> EvidenceCollection:
        return self._by_severity(EvidenceSeverity.ERROR)

    def warnings(self) -> EvidenceCollection:
        return self._by_severity(EvidenceSeverity.WARNING)

    def infos(self) -> EvidenceCollection:
        return self._by_severity(EvidenceSeverity.INFO)

    def _by_severity(
        self,
        severity: EvidenceSeverity,
    ) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                item
                for item in self.items
                if item.severity == severity
            )
        )


def _build_evidence_id(
    evidence_type: EvidenceType,
    source: EvidenceSource,
    summary: str,
    details: str,
    severity: EvidenceSeverity,
    metadata: Mapping[str, str],
) -> str:
    metadata_parts = tuple(
        f"{key}={metadata[key]}"
        for key in sorted(metadata)
    )
    raw_id = "|".join(
        (
            evidence_type.value,
            source.source_id,
            source.source_type.value,
            source.path.as_posix(),
            source.name,
            summary,
            details,
            severity.value,
            ";".join(metadata_parts),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]
