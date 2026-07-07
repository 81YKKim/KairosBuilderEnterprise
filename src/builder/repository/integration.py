from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from builder.repository.change_analyzer import (
    ChangeSet,
    RepositoryChangeAnalyzer,
)
from builder.repository.graph import RepositoryGraph, RepositoryGraphBuilder
from builder.repository.impact_analyzer import (
    ImpactScope,
    RepositoryImpactAnalyzer,
)
from builder.repository.index import RepositoryIndex, build_index
from builder.repository.intelligence import (
    RepositoryIntelligence,
    RepositoryMetrics,
)
from builder.repository.inventory import (
    RepositoryInventory,
    RepositoryInventoryBuilder,
)
from builder.repository.model import PythonModule, PythonPackage
from builder.repository.qa import QAResult, RepositoryQA
from builder.repository.query import QueryResult, RepositoryQuery
from builder.repository.scanner import RepositoryScanner


@dataclass(frozen=True, slots=True)
class RepositoryPlatform:
    scanner: RepositoryScanner
    inventory: RepositoryInventory
    graph: RepositoryGraph
    intelligence: RepositoryIntelligence
    query_service: RepositoryQuery
    qa_service: RepositoryQA
    change_analyzer: RepositoryChangeAnalyzer
    impact_analyzer: RepositoryImpactAnalyzer
    index: RepositoryIndex

    @classmethod
    def create(
        cls,
        repository_root: str | Path,
        git_root: str | Path | None = None,
        branch: str = "Unknown",
        head_commit: str = "Unknown",
    ) -> RepositoryPlatform:
        scanner = RepositoryScanner()
        inventory = RepositoryInventoryBuilder(
            scanner=scanner,
        ).build(
            repository_root,
            git_root=git_root,
            branch=branch,
            head_commit=head_commit,
        )
        graph = RepositoryGraphBuilder().build(inventory)
        intelligence = RepositoryIntelligence(
            inventory=inventory,
            graph=graph,
        )
        query = RepositoryQuery(intelligence=intelligence)
        qa = RepositoryQA(
            intelligence=intelligence,
            query=query,
        )
        change_analyzer = RepositoryChangeAnalyzer(
            intelligence=intelligence,
            query=query,
            qa=qa,
        )
        impact_analyzer = RepositoryImpactAnalyzer(
            intelligence=intelligence,
            query=query,
            qa=qa,
            change_analyzer=change_analyzer,
        )
        index = build_index(
            intelligence,
            query,
            qa,
        )

        return cls(
            scanner=scanner,
            inventory=inventory,
            graph=graph,
            intelligence=intelligence,
            query_service=query,
            qa_service=qa,
            change_analyzer=change_analyzer,
            impact_analyzer=impact_analyzer,
            index=index,
        )

    @classmethod
    def build(
        cls,
        repository_root: str | Path,
        git_root: str | Path | None = None,
        branch: str = "Unknown",
        head_commit: str = "Unknown",
    ) -> RepositoryPlatform:
        return cls.create(
            repository_root,
            git_root=git_root,
            branch=branch,
            head_commit=head_commit,
        )

    def summary(self) -> dict[str, int | str]:
        return self.intelligence.repository_summary()

    def metrics(self) -> RepositoryMetrics:
        return self.intelligence.repository_metrics()

    def query(
        self,
        source: str,
    ) -> QueryResult:
        if source == "packages":
            return self.query_service.packages()

        if source == "modules":
            return self.query_service.modules()

        if source == "tests":
            return self.query_service.find_tests()

        return self.query_service.where(source, lambda item: True)

    def qa(self) -> QAResult:
        return self.qa_service.run_all()

    def analyze_change(
        self,
        paths: tuple[str | Path, ...],
    ) -> ChangeSet:
        return self.change_analyzer.analyze_files(paths)

    def analyze_impact(
        self,
        paths: tuple[str | Path, ...],
    ) -> ImpactScope:
        return self.impact_analyzer.analyze(paths)

    def find_module(
        self,
        name: str,
    ) -> PythonModule | None:
        return self.index.find_module(name)

    def find_package(
        self,
        name: str,
    ) -> PythonPackage | None:
        return self.index.find_package(name)

    def modules(self) -> tuple[PythonModule, ...]:
        return self.intelligence.modules()

    def packages(self) -> tuple[PythonPackage, ...]:
        return self.intelligence.packages()

    def validate(self) -> dict[str, Any]:
        qa_result = self.qa()

        return {
            "repository_root": str(self.inventory.repository_root),
            "has_inventory": self.inventory is not None,
            "has_graph": self.graph is not None,
            "has_index": self.index is not None,
            "package_count": self.inventory.package_count,
            "module_count": self.inventory.module_count,
            "qa_passed": qa_result.passed,
        }
