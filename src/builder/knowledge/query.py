from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from builder.knowledge.graph import KnowledgeGraph
from builder.knowledge.model import (
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)


@dataclass(frozen=True, slots=True)
class QueryResult:
    items: tuple[Any, ...]
    count: int
    query: str
    filters: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class KnowledgeQuery:
    graph: KnowledgeGraph

    def entities(self) -> QueryResult:
        return self._result(
            query="entities",
            items=self.graph.entities(),
        )

    def relationships(self) -> QueryResult:
        return self._result(
            query="relationships",
            items=self.graph.relationships(),
        )

    def find_entity(
        self,
        entity_id: str,
    ) -> QueryResult:
        return self._result(
            query="find_entity",
            items=self._optional_item(
                self.graph.find_entity(entity_id)
            ),
            filters=(("entity_id", entity_id),),
        )

    def find_relationship(
        self,
        relationship_id: str,
    ) -> QueryResult:
        return self._result(
            query="find_relationship",
            items=self._optional_item(
                self.graph.find_relationship(relationship_id)
            ),
            filters=(("relationship_id", relationship_id),),
        )

    def entities_by_type(
        self,
        entity_type: KnowledgeEntityType,
    ) -> QueryResult:
        return self._result(
            query="entities_by_type",
            items=tuple(
                entity
                for entity in self.graph.entities()
                if entity.entity_type == entity_type
            ),
            filters=(("entity_type", entity_type.value),),
        )

    def relationships_by_type(
        self,
        relationship_type: KnowledgeRelationshipType,
    ) -> QueryResult:
        return self._result(
            query="relationships_by_type",
            items=tuple(
                relationship
                for relationship in self.graph.relationships()
                if relationship.relationship_type == relationship_type
            ),
            filters=(("relationship_type", relationship_type.value),),
        )

    def search_entities(
        self,
        text: str,
    ) -> QueryResult:
        normalized_text = text.casefold()

        return self._result(
            query="search_entities",
            items=tuple(
                entity
                for entity in self.graph.entities()
                if normalized_text in self._entity_search_text(entity)
            ),
            filters=(("text", text),),
        )

    def search_relationships(
        self,
        text: str,
    ) -> QueryResult:
        normalized_text = text.casefold()

        return self._result(
            query="search_relationships",
            items=tuple(
                relationship
                for relationship in self.graph.relationships()
                if normalized_text
                in self._relationship_search_text(relationship)
            ),
            filters=(("text", text),),
        )

    def neighbors(
        self,
        entity_id: str,
    ) -> QueryResult:
        return self._result(
            query="neighbors",
            items=self.graph.neighbors(entity_id),
            filters=(("entity_id", entity_id),),
        )

    def dependencies(
        self,
        entity_id: str,
    ) -> QueryResult:
        return self._result(
            query="dependencies",
            items=self.graph.dependencies(entity_id),
            filters=(("entity_id", entity_id),),
        )

    def dependents(
        self,
        entity_id: str,
    ) -> QueryResult:
        return self._result(
            query="dependents",
            items=self.graph.dependents(entity_id),
            filters=(("entity_id", entity_id),),
        )

    def where_entities(
        self,
        predicate: Callable[[KnowledgeEntity], bool],
    ) -> QueryResult:
        return self._result(
            query="where_entities",
            items=tuple(
                entity
                for entity in self.graph.entities()
                if predicate(entity)
            ),
        )

    def where_relationships(
        self,
        predicate: Callable[[KnowledgeRelationship], bool],
    ) -> QueryResult:
        return self._result(
            query="where_relationships",
            items=tuple(
                relationship
                for relationship in self.graph.relationships()
                if predicate(relationship)
            ),
        )

    def _entity_search_text(
        self,
        entity: KnowledgeEntity,
    ) -> str:
        metadata = " ".join(
            f"{key} {value}" for key, value in entity.metadata.items()
        )

        return (
            f"{entity.entity_id} {entity.entity_type.value} "
            f"{entity.name} {entity.summary} {metadata}"
        ).casefold()

    def _relationship_search_text(
        self,
        relationship: KnowledgeRelationship,
    ) -> str:
        metadata = " ".join(
            f"{key} {value}" for key, value in relationship.metadata.items()
        )

        return (
            f"{relationship.relationship_id} "
            f"{relationship.relationship_type.value} "
            f"{relationship.source_entity_id} "
            f"{relationship.target_entity_id} {metadata}"
        ).casefold()

    def _optional_item(
        self,
        item: KnowledgeEntity | KnowledgeRelationship | None,
    ) -> tuple[KnowledgeEntity | KnowledgeRelationship, ...]:
        if item is None:
            return ()

        return (item,)

    def _result(
        self,
        query: str,
        items: tuple[Any, ...],
        filters: tuple[tuple[str, str], ...] = (),
    ) -> QueryResult:
        return QueryResult(
            items=items,
            count=len(items),
            query=query,
            filters=filters,
        )
