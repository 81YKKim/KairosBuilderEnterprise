from __future__ import annotations

from dataclasses import dataclass

from builder.evidence.model import (
    Evidence,
    EvidenceCollection,
    EvidenceType,
)
from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
    KnowledgeRelationshipType,
)


@dataclass(frozen=True, slots=True)
class KnowledgeExtractor:
    def extract(
        self,
        evidence_collection: EvidenceCollection,
    ) -> KnowledgeCollection:
        entities = self.extract_entities(evidence_collection).entities
        relationships = self.extract_relationships(
            evidence_collection,
            entities,
        ).relationships

        return KnowledgeCollection(
            entities=entities,
            relationships=relationships,
        )

    def extract_entities(
        self,
        evidence_collection: EvidenceCollection,
    ) -> KnowledgeCollection:
        return KnowledgeCollection(
            entities=tuple(
                self._entity_from_evidence(evidence)
                for evidence in evidence_collection.items
                if self._entity_type(evidence) is not None
            ),
            relationships=(),
        )

    def extract_relationships(
        self,
        evidence_collection: EvidenceCollection,
        entities: tuple[KnowledgeEntity, ...] | None = None,
    ) -> KnowledgeCollection:
        if entities is None:
            entities = self.extract_entities(evidence_collection).entities

        entity_by_name = {
            entity.name: entity for entity in entities
        }
        repository_entity = self._repository_entity(entities)
        relationships: list[KnowledgeRelationship] = []

        if repository_entity is not None:
            relationships.extend(
                self._repository_contains_relationships(
                    repository_entity,
                    entities,
                )
            )

        relationships.extend(
            self._package_contains_module_relationships(
                evidence_collection,
                entity_by_name,
            )
        )
        relationships.extend(
            self._test_tests_module_relationships(
                evidence_collection,
                entity_by_name,
            )
        )

        return KnowledgeCollection(
            entities=(),
            relationships=tuple(relationships),
        )

    def _entity_from_evidence(
        self,
        evidence: Evidence,
    ) -> KnowledgeEntity:
        entity_type = self._entity_type(evidence)

        if entity_type is None:
            raise ValueError(
                f"Unsupported evidence type: {evidence.evidence_type}"
            )

        return KnowledgeEntity.create(
            entity_type=entity_type,
            name=evidence.source.name,
            summary=evidence.summary,
            evidence_ids=(evidence.evidence_id,),
            metadata={
                "source_id": evidence.source.source_id,
                "source_path": evidence.source.path.as_posix(),
            },
        )

    def _entity_type(
        self,
        evidence: Evidence,
    ) -> KnowledgeEntityType | None:
        return {
            EvidenceType.REPOSITORY: KnowledgeEntityType.REPOSITORY,
            EvidenceType.PACKAGE: KnowledgeEntityType.PACKAGE,
            EvidenceType.MODULE: KnowledgeEntityType.MODULE,
            EvidenceType.TEST: KnowledgeEntityType.TEST,
            EvidenceType.DOCUMENT: KnowledgeEntityType.DOCUMENT,
            EvidenceType.GENERATOR: KnowledgeEntityType.GENERATOR,
            EvidenceType.CLASS: KnowledgeEntityType.CLASS,
            EvidenceType.FUNCTION: KnowledgeEntityType.FUNCTION,
        }.get(evidence.evidence_type)

    def _repository_entity(
        self,
        entities: tuple[KnowledgeEntity, ...],
    ) -> KnowledgeEntity | None:
        return next(
            (
                entity
                for entity in entities
                if entity.entity_type == KnowledgeEntityType.REPOSITORY
            ),
            None,
        )

    def _repository_contains_relationships(
        self,
        repository_entity: KnowledgeEntity,
        entities: tuple[KnowledgeEntity, ...],
    ) -> tuple[KnowledgeRelationship, ...]:
        return tuple(
            KnowledgeRelationship.create(
                relationship_type=KnowledgeRelationshipType.CONTAINS,
                source_entity_id=repository_entity.entity_id,
                target_entity_id=entity.entity_id,
                evidence_ids=(
                    repository_entity.evidence_ids
                    + entity.evidence_ids
                ),
                metadata={
                    "relationship": self._repository_relationship_name(entity),
                },
            )
            for entity in entities
            if entity.entity_id != repository_entity.entity_id
            and entity.entity_type
            in {
                KnowledgeEntityType.PACKAGE,
                KnowledgeEntityType.MODULE,
            }
        )

    def _repository_relationship_name(
        self,
        entity: KnowledgeEntity,
    ) -> str:
        if entity.entity_type == KnowledgeEntityType.PACKAGE:
            return "repository_contains_package"

        return "repository_contains_module"

    def _package_contains_module_relationships(
        self,
        evidence_collection: EvidenceCollection,
        entity_by_name: dict[str, KnowledgeEntity],
    ) -> tuple[KnowledgeRelationship, ...]:
        relationships: list[KnowledgeRelationship] = []

        for evidence in evidence_collection.by_type(EvidenceType.MODULE).items:
            package_name = evidence.metadata.get("package")

            if not package_name:
                continue

            package_entity = entity_by_name.get(package_name)
            module_entity = entity_by_name.get(evidence.source.name)

            if package_entity is None or module_entity is None:
                continue

            relationships.append(
                KnowledgeRelationship.create(
                    relationship_type=KnowledgeRelationshipType.CONTAINS,
                    source_entity_id=package_entity.entity_id,
                    target_entity_id=module_entity.entity_id,
                    evidence_ids=(evidence.evidence_id,),
                    metadata={
                        "relationship": "package_contains_module",
                    },
                )
            )

        return tuple(relationships)

    def _test_tests_module_relationships(
        self,
        evidence_collection: EvidenceCollection,
        entity_by_name: dict[str, KnowledgeEntity],
    ) -> tuple[KnowledgeRelationship, ...]:
        relationships: list[KnowledgeRelationship] = []

        for evidence in evidence_collection.by_type(EvidenceType.TEST).items:
            module_name = evidence.metadata.get("module")

            if not module_name:
                continue

            test_entity = entity_by_name.get(evidence.source.name)
            module_entity = entity_by_name.get(module_name)

            if test_entity is None or module_entity is None:
                continue

            relationships.append(
                KnowledgeRelationship.create(
                    relationship_type=KnowledgeRelationshipType.TESTS,
                    source_entity_id=test_entity.entity_id,
                    target_entity_id=module_entity.entity_id,
                    evidence_ids=(evidence.evidence_id,),
                    metadata={
                        "relationship": "test_tests_module",
                    },
                )
            )

        return tuple(relationships)
