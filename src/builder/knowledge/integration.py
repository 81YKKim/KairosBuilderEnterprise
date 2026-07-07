from __future__ import annotations

from dataclasses import dataclass

from builder.evidence.extractor import EvidenceExtractor
from builder.evidence.model import EvidenceCollection, EvidenceType
from builder.knowledge.cache import KnowledgeCache, KnowledgeSnapshot
from builder.knowledge.extractor import KnowledgeExtractor
from builder.knowledge.graph import KnowledgeGraph
from builder.knowledge.model import (
    KnowledgeCollection,
    KnowledgeEntity,
    KnowledgeEntityType,
    KnowledgeRelationship,
)
from builder.knowledge.query import KnowledgeQuery
from builder.repository.integration import RepositoryPlatform


@dataclass(frozen=True, slots=True)
class KnowledgePlatform:
    repository_platform: RepositoryPlatform
    evidence_extractor: EvidenceExtractor
    evidence: EvidenceCollection
    knowledge_extractor: KnowledgeExtractor
    knowledge: KnowledgeCollection
    graph: KnowledgeGraph
    query: KnowledgeQuery
    cache: KnowledgeCache

    @classmethod
    def build(
        cls,
        repository_platform: RepositoryPlatform,
    ) -> KnowledgePlatform:
        evidence_extractor = EvidenceExtractor(repository_platform)
        evidence = evidence_extractor.extract_all()
        knowledge_extractor = KnowledgeExtractor()
        knowledge = knowledge_extractor.extract(evidence)
        graph = KnowledgeGraph.from_collection(knowledge)
        query = KnowledgeQuery(graph)
        cache = KnowledgeCache.create(
            graph,
            metadata={
                "source": "knowledge-platform",
            },
        )

        return cls(
            repository_platform=repository_platform,
            evidence_extractor=evidence_extractor,
            evidence=evidence,
            knowledge_extractor=knowledge_extractor,
            knowledge=knowledge,
            graph=graph,
            query=query,
            cache=cache,
        )

    @classmethod
    def create(
        cls,
        repository_platform: RepositoryPlatform,
    ) -> KnowledgePlatform:
        return cls.build(repository_platform)

    def evidence_summary(self) -> dict[str, int]:
        return {
            "total": self.evidence.count,
            "packages": self.evidence.by_type(EvidenceType.PACKAGE).count,
            "modules": self.evidence.by_type(EvidenceType.MODULE).count,
            "tests": self.evidence.by_type(EvidenceType.TEST).count,
            "documents": self.evidence.by_type(EvidenceType.DOCUMENT).count,
            "errors": self.evidence.errors().count,
            "warnings": self.evidence.warnings().count,
            "infos": self.evidence.infos().count,
        }

    def knowledge_summary(self) -> dict[str, int]:
        return {
            "entities": self.knowledge.entity_count,
            "relationships": self.knowledge.relationship_count,
            "packages": self._entity_count(KnowledgeEntityType.PACKAGE),
            "modules": self._entity_count(KnowledgeEntityType.MODULE),
            "tests": self._entity_count(KnowledgeEntityType.TEST),
            "documents": self._entity_count(KnowledgeEntityType.DOCUMENT),
        }

    def entities(self) -> tuple[KnowledgeEntity, ...]:
        return self.cache.entities()

    def relationships(self) -> tuple[KnowledgeRelationship, ...]:
        return self.cache.relationships()

    def find_entity(
        self,
        entity_id: str,
    ) -> KnowledgeEntity | None:
        return self.cache.find_entity(entity_id)

    def find_relationship(
        self,
        relationship_id: str,
    ) -> KnowledgeRelationship | None:
        return self.cache.find_relationship(relationship_id)

    def neighbors(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        return self.query.neighbors(entity_id).items

    def dependencies(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        return self.query.dependencies(entity_id).items

    def dependents(
        self,
        entity_id: str,
    ) -> tuple[KnowledgeEntity, ...]:
        return self.query.dependents(entity_id).items

    def snapshot(self) -> KnowledgeSnapshot:
        return self.cache.snapshot()

    def validate(self) -> dict[str, int | bool]:
        return {
            "has_repository_platform": self.repository_platform is not None,
            "has_evidence": self.evidence is not None,
            "has_knowledge": self.knowledge is not None,
            "has_graph": self.graph is not None,
            "has_query": self.query is not None,
            "has_cache": self.cache is not None,
            "cache_valid": self.cache.validate(),
            "entity_count": self.knowledge.entity_count,
            "relationship_count": self.knowledge.relationship_count,
        }

    def _entity_count(
        self,
        entity_type: KnowledgeEntityType,
    ) -> int:
        return self.knowledge.entities_by_type(entity_type).entity_count
