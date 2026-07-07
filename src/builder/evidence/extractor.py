from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from builder.evidence.model import (
    Evidence,
    EvidenceCollection,
    EvidenceSeverity,
    EvidenceSource,
    EvidenceType,
)
from builder.repository.integration import RepositoryPlatform


@dataclass(frozen=True, slots=True)
class EvidenceExtractor:
    platform: RepositoryPlatform

    def extract_all(self) -> EvidenceCollection:
        return EvidenceCollection(
            items=(
                self.extract_packages().items
                + self.extract_modules().items
                + self.extract_tests().items
                + self.extract_resources().items
            )
        )

    def extract_packages(self) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                Evidence.create(
                    evidence_type=EvidenceType.PACKAGE,
                    source=EvidenceSource(
                        source_id=f"package:{package.name}",
                        source_type=EvidenceType.PACKAGE,
                        path=package.path,
                        name=package.name,
                    ),
                    summary=f"Package discovered: {package.name}",
                    details=f"Repository package path: {package.path.as_posix()}",
                    severity=EvidenceSeverity.INFO,
                    metadata={
                        "layer": "perception",
                    },
                )
                for package in self.platform.packages()
            )
        )

    def extract_modules(self) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                Evidence.create(
                    evidence_type=EvidenceType.MODULE,
                    source=EvidenceSource(
                        source_id=f"module:{module.name}",
                        source_type=EvidenceType.MODULE,
                        path=module.path,
                        name=module.name,
                    ),
                    summary=f"Module discovered: {module.name}",
                    details=f"Repository module path: {module.path.as_posix()}",
                    severity=EvidenceSeverity.INFO,
                    metadata={
                        "package": module.package,
                    },
                )
                for module in self.platform.modules()
            )
        )

    def extract_tests(self) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                Evidence.create(
                    evidence_type=EvidenceType.TEST,
                    source=EvidenceSource(
                        source_id=f"test:{test.path.as_posix()}",
                        source_type=EvidenceType.TEST,
                        path=test.path,
                        name=test.name,
                    ),
                    summary=f"Test discovered: {test.name}",
                    details=f"Repository test path: {test.path.as_posix()}",
                    severity=EvidenceSeverity.INFO,
                    metadata={
                        "layer": "validation",
                    },
                )
                for test in self.platform.query("tests").items
            )
        )

    def extract_resources(self) -> EvidenceCollection:
        return EvidenceCollection(
            items=tuple(
                self._resource_evidence(path)
                for path in self._resource_paths()
            )
        )

    def _resource_paths(self) -> tuple[Path, ...]:
        return tuple(
            path
            for suffix in sorted(self.platform.index.resources_by_suffix)
            for path in self.platform.index.resources_by_suffix[suffix]
        )

    def _resource_evidence(
        self,
        path: Path,
    ) -> Evidence:
        evidence_type = EvidenceType.DOCUMENT

        return Evidence.create(
            evidence_type=evidence_type,
            source=EvidenceSource(
                source_id=f"resource:{path.as_posix()}",
                source_type=evidence_type,
                path=path,
                name=path.stem,
            ),
            summary=f"Resource discovered: {path.as_posix()}",
            details=f"Repository resource path: {path.as_posix()}",
            severity=EvidenceSeverity.INFO,
            metadata={
                "suffix": path.suffix,
            },
        )
