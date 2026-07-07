from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping

from builder.knowledge.graph import KnowledgeGraph
from builder.knowledge.model import (
    KnowledgeEntity,
    KnowledgeRelationship,
)


@dataclass(frozen=True, slots=True)
class KnowledgeSnapshot:
    snapshot_id: str
    entity_count: int
    relationship_count: int
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeCache:
    cache_id: str
    created_at: str
    entity_count: int
    relationship_count: int
    graph: KnowledgeGraph
    metadata: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        graph: KnowledgeGraph,
        metadata: Mapping[str, str] | None = None,
        created_at: str | None = None,
    ) -> KnowledgeCache:
        normalized_metadata = dict(metadata or {})

        return cls(
            cache_id=_build_cache_id(
                graph=graph,
                metadata=normalized_metadata,
            ),
            created_at=created_at or _created_at(),
            entity_count=len(graph.entities()),
            relationship_count=len(graph.relationships()),
            graph=graph,
            metadata=MappingProxyType(normalized_metadata),
        )

    def find_entity(
        self,
        entity_id: str,
    ) -> KnowledgeEntity | None:
        return self.graph.find_entity(entity_id)

    def find_relationship(
        self,
        relationship_id: str,
    ) -> KnowledgeRelationship | None:
        return self.graph.find_relationship(relationship_id)

    def entities(self) -> tuple[KnowledgeEntity, ...]:
        return self.graph.entities()

    def relationships(self) -> tuple[KnowledgeRelationship, ...]:
        return self.graph.relationships()

    def snapshot(self) -> KnowledgeSnapshot:
        return KnowledgeSnapshot(
            snapshot_id=self.cache_id,
            entity_count=self.entity_count,
            relationship_count=self.relationship_count,
            metadata=self.metadata,
        )

    def validate(self) -> bool:
        if self.entity_count != len(self.graph.entities()):
            return False

        if self.relationship_count != len(self.graph.relationships()):
            return False

        entity_ids = {
            entity.entity_id
            for entity in self.graph.entities()
        }

        return all(
            relationship.source_entity_id in entity_ids
            and relationship.target_entity_id in entity_ids
            for relationship in self.graph.relationships()
        )


def _created_at() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _build_cache_id(
    graph: KnowledgeGraph,
    metadata: Mapping[str, str],
) -> str:
    raw_id = "|".join(
        (
            _entity_ids_text(graph),
            _relationship_ids_text(graph),
            _metadata_text(metadata),
        )
    )

    return sha256(raw_id.encode("utf-8")).hexdigest()[:16]


def _entity_ids_text(
    graph: KnowledgeGraph,
) -> str:
    return ";".join(
        entity.entity_id
        for entity in graph.entities()
    )


def _relationship_ids_text(
    graph: KnowledgeGraph,
) -> str:
    return ";".join(
        relationship.relationship_id
        for relationship in graph.relationships()
    )


def _metadata_text(
    metadata: Mapping[str, str],
) -> str:
    return ";".join(
        f"{key}={metadata[key]}"
        for key in sorted(metadata)
    )
