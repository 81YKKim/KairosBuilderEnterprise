from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping


class KnowledgeEntityType(StrEnum):
    REPOSITORY = "repository"
    PACKAGE = "package"
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    TEST = "test"
    SERVICE = "service"
    GENERATOR = "generator"
    DOCUMENT = "document"


class KnowledgeRelationshipType(StrEnum):
    CONTAINS = "contains"
    IMPORTS = "imports"
    TESTS = "tests"
    USES = "uses"
    DEPENDS_ON = "depends_on"
    GENERATES = "generates"
    REFERENCES = "references"
    OWNS = "owns"


@dataclass(frozen=True, slots=True)
class KnowledgeEntity:
    entity_id: str
    entity_type: KnowledgeEntityType
    name: str
    summary: str
    evidence_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        entity_type: KnowledgeEntityType,
        name: str,
        summary: str,
        evidence_ids: tuple[str, ...],
        metadata: Mapping[str, str] | None = None,
    ) -> KnowledgeEntity:
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            entity_id=_build_entity_id(
                entity_type=entity_type,
                name=name,
                summary=summary,
                evidence_ids=normalized_evidence_ids,
                metadata=normalized_metadata,
            ),
            entity_type=entity_type,
            name=name,
            summary=summary,
            evidence_ids=normalized_evidence_ids,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeRelationship:
    relationship_id: str
    relationship_type: KnowledgeRelationshipType
    source_entity_id: str
    target_entity_id: str
    evidence_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        relationship_type: KnowledgeRelationshipType,
        source_entity_id: str,
        target_entity_id: str,
        evidence_ids: tuple[str, ...],
        metadata: Mapping[str, str] | None = None,
    ) -> KnowledgeRelationship:
        normalized_evidence_ids = tuple(sorted(evidence_ids))
        normalized_metadata = dict(metadata or {})

        return cls(
            relationship_id=_build_relationship_id(
                relationship_type=relationship_type,
                source_entity_id=source_entity_id,
                target_entity_id=target_entity_id,
                evidence_ids=normalized_evidence_ids,
                metadata=normalized_metadata,
            ),
            relationship_type=relationship_type,
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            evidence_ids=normalized_evidence_ids,
            metadata=MappingProxyType(normalized_metadata),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeCollection:
    entities: tuple[KnowledgeEntity, ...] = ()
    relationships: tuple[KnowledgeRelationship, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entities",
            tuple(
                sorted(
                    self.entities,
                    key=lambda entity: entity.entity_id,
                )
            ),
        )
        object.__setattr__(
            self,
            "relationships",
            tuple(
                sorted(
                    self.relationships,
                    key=lambda relationship: relationship.relationship_id,
                )
            ),
        )

    @property
    def entity_count(self) -> int:
        return len(self.entities)

    @property
    def relationship_count(self) -> int:
        return len(self.relationships)

    def entities_by_type(
        self,
        entity_type: KnowledgeEntityType,
    ) -> KnowledgeCollection:
        return KnowledgeCollection(
            entities=tuple(
                entity
                for entity in self.entities
                if entity.entity_type == entity_type
            ),
            relationships=(),
        )

    def relationships_by_type(
        self,
        relationship_type: KnowledgeRelationshipType,
    ) -> KnowledgeCollection:
        return KnowledgeCollection(
            entities=(),
            relationships=tuple(
                relationship
                for relationship in self.relationships
                if relationship.relationship_type == relationship_type
            ),
        )

    def find_entity(
        self,
        entity_id: str,
    ) -> KnowledgeEntity | None:
        return next(
            (
                entity
                for entity in self.entities
                if entity.entity_id == entity_id
            ),
            None,
        )

    def find_relationship(
        self,
        relationship_id: str,
    ) -> KnowledgeRelationship | None:
        return next(
            (
                relationship
                for relationship in self.relationships
                if relationship.relationship_id == relationship_id
            ),
            None,
        )


def _build_entity_id(
    entity_type: KnowledgeEntityType,
    name: str,
    summary: str,
    evidence_ids: tuple[str, ...],
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            entity_type.value,
            name,
            summary,
            ";".join(evidence_ids),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _build_relationship_id(
    relationship_type: KnowledgeRelationshipType,
    source_entity_id: str,
    target_entity_id: str,
    evidence_ids: tuple[str, ...],
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            relationship_type.value,
            source_entity_id,
            target_entity_id,
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
