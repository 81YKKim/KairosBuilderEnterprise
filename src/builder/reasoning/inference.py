from __future__ import annotations

from dataclasses import dataclass

from builder.knowledge.integration import KnowledgePlatform
from builder.knowledge.model import (
    KnowledgeEntity,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)
from builder.reasoning.model import (
    Inference,
    ReasoningCollection,
    ReasoningResult,
    ReasoningSeverity,
    ReasoningType,
)


@dataclass(frozen=True, slots=True)
class InferenceEngine:
    def infer_all(
        self,
        knowledge_platform: KnowledgePlatform,
    ) -> ReasoningCollection:
        entity_results = self.infer_entities(knowledge_platform).results
        relationship_results = self.infer_relationships(
            knowledge_platform
        ).results

        return ReasoningCollection(
            results=entity_results + relationship_results,
        )

    def infer_entities(
        self,
        knowledge_platform: KnowledgePlatform,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                self._entity_result(entity)
                for entity in knowledge_platform.entities()
            )
        )

    def infer_relationships(
        self,
        knowledge_platform: KnowledgePlatform,
    ) -> ReasoningCollection:
        return ReasoningCollection(
            results=tuple(
                self._relationship_result(
                    relationship,
                    knowledge_platform,
                )
                for relationship in knowledge_platform.relationships()
            )
        )

    def _entity_result(
        self,
        entity: KnowledgeEntity,
    ) -> ReasoningResult:
        inference = Inference.create(
            inference_type=ReasoningType.INFERENCE,
            subject=entity.name,
            predicate="exists",
            object=entity.entity_type.value,
            evidence_ids=entity.evidence_ids,
            confidence=1.0,
            metadata={
                "entity_id": entity.entity_id,
                "entity_type": entity.entity_type.value,
            },
        )

        return ReasoningResult.create(
            reasoning_type=ReasoningType.INFERENCE,
            summary=f"Entity exists: {entity.name}",
            inferences=(inference,),
            severity=ReasoningSeverity.INFO,
            confidence=inference.confidence,
            evidence_ids=entity.evidence_ids,
            metadata={
                "entity_id": entity.entity_id,
                "entity_type": entity.entity_type.value,
                "inference_kind": "entity_exists",
            },
        )

    def _relationship_result(
        self,
        relationship: KnowledgeRelationship,
        knowledge_platform: KnowledgePlatform,
    ) -> ReasoningResult:
        source = knowledge_platform.find_entity(
            relationship.source_entity_id
        )
        target = knowledge_platform.find_entity(
            relationship.target_entity_id
        )
        source_name = source.name if source is not None else (
            relationship.source_entity_id
        )
        target_name = target.name if target is not None else (
            relationship.target_entity_id
        )
        predicate = self._relationship_predicate(relationship)
        relationship_kind = self._relationship_kind(relationship)
        inference = Inference.create(
            inference_type=ReasoningType.INFERENCE,
            subject=source_name,
            predicate=predicate,
            object=target_name,
            evidence_ids=relationship.evidence_ids,
            confidence=1.0,
            metadata={
                "relationship_id": relationship.relationship_id,
                "relationship_type": relationship.relationship_type.value,
                "relationship_kind": relationship_kind,
                "source_entity_id": relationship.source_entity_id,
                "target_entity_id": relationship.target_entity_id,
            },
        )

        return ReasoningResult.create(
            reasoning_type=ReasoningType.INFERENCE,
            summary=(
                f"Relationship exists: {source_name} "
                f"{predicate} {target_name}"
            ),
            inferences=(inference,),
            severity=ReasoningSeverity.INFO,
            confidence=inference.confidence,
            evidence_ids=relationship.evidence_ids,
            metadata={
                "relationship_id": relationship.relationship_id,
                "relationship_type": relationship.relationship_type.value,
                "relationship_kind": relationship_kind,
                "inference_kind": "relationship_exists",
            },
        )

    def _relationship_predicate(
        self,
        relationship: KnowledgeRelationship,
    ) -> str:
        return relationship.relationship_type.value

    def _relationship_kind(
        self,
        relationship: KnowledgeRelationship,
    ) -> str:
        if relationship.relationship_type in {
            KnowledgeRelationshipType.DEPENDS_ON,
            KnowledgeRelationshipType.IMPORTS,
            KnowledgeRelationshipType.USES,
        }:
            return "dependency"

        if relationship.relationship_type == KnowledgeRelationshipType.TESTS:
            return "test"

        if (
            relationship.relationship_type
            == KnowledgeRelationshipType.CONTAINS
        ):
            return "contains"

        return "relationship"
