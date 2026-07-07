from __future__ import annotations

from dataclasses import dataclass

from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeRelationship,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGraph:
    collection: KnowledgeCollection
    entities_by_id: dict[str, KnowledgeEntity]
    relationships_by_id: dict[str, KnowledgeRelationship]
    outgoing_by_entity: dict[str, tuple[KnowledgeRelationship, ...]]
    incoming_by_entity: dict[str, tuple[KnowledgeRelationship, ...]]

    @classmethod
    def from_collection(
        cls,
        collection: KnowledgeCollection,
    ) -> KnowledgeGraph:
        entities = collection.entities
        relationships = collection.relationships

        return cls(
            collection=collection,
            entities_by_id={
                entity.entity_id: entity for entity in entities
            },
            relationships_by_id={
                relationship.relationship_id: relationship
                for relationship in relationships
            },
            outgoing_by_entity=_build_outgoing(
                entities,
                relationships,
            ),
            incoming_by_entity=_build_incoming(
                entities,
                relationships,
            ),
        )

    def entities(self) -> tuple[KnowledgeEntity, ...]:
        return self.collection.entities

    def relationships(self) -> tuple[KnowledgeRelationship, ...]:
        return self.collection.relationships

    def find_entity(
        self,
        entity_id: str,
    ) -> KnowledgeEntity | None:
        return self.entities_by_id.get(entity_id)

    def find_relationship(
        self,
        relationship_id: str,
    ) -> KnowledgeRelationship | None:
        return self.relationships_by_id.get(relationship_id)

    def neighbors(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        neighbor_ids = {
            relationship.target_entity_id
            for relationship in self.outgoing(entity_id)
        }
        neighbor_ids.update(
            relationship.source_entity_id
            for relationship in self.incoming(entity_id)
        )

        return _sort_entities(
            tuple(
                entity
                for neighbor_id in neighbor_ids
                if (entity := self.find_entity(neighbor_id)) is not None
            )
        )

    def outgoing(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeRelationship, ...]:
        return self.outgoing_by_entity.get(entity_id, ())

    def incoming(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeRelationship, ...]:
        return self.incoming_by_entity.get(entity_id, ())

    def dependencies(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        return _sort_entities(
            tuple(
                entity
                for relationship in self.outgoing(entity_id)
                if (
                    entity := self.find_entity(
                        relationship.target_entity_id
                    )
                )
                is not None
            )
        )

    def dependents(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        return _sort_entities(
            tuple(
                entity
                for relationship in self.incoming(entity_id)
                if (
                    entity := self.find_entity(
                        relationship.source_entity_id
                    )
                )
                is not None
            )
        )


def _build_outgoing(
    entities: tuple[KnowledgeEntity, ...],
    relationships: tuple[KnowledgeRelationship, ...],
) -> dict[str, tuple[KnowledgeRelationship, ...]]:
    return {
        entity.entity_id: _sort_relationships(
            tuple(
                relationship
                for relationship in relationships
                if relationship.source_entity_id == entity.entity_id
            )
        )
        for entity in entities
    }


def _build_incoming(
    entities: tuple[KnowledgeEntity, ...],
    relationships: tuple[KnowledgeRelationship, ...],
) -> dict[str, tuple[KnowledgeRelationship, ...]]:
    return {
        entity.entity_id: _sort_relationships(
            tuple(
                relationship
                for relationship in relationships
                if relationship.target_entity_id == entity.entity_id
            )
        )
        for entity in entities
    }


def _sort_entities(
    entities: tuple[KnowledgeEntity, ...],
) -> tuple[KnowledgeEntity, ...]:
    return tuple(
        sorted(
            entities,
            key=lambda entity: entity.entity_id,
        )
    )


def _sort_relationships(
    relationships: tuple[KnowledgeRelationship, ...],
) -> tuple[KnowledgeRelationship, ...]:
    return tuple(
        sorted(
            relationships,
            key=lambda relationship: relationship.relationship_id,
        )
    )
