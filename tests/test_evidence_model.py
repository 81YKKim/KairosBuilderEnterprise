from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from builder.evidence.model import (
    Evidence,
    EvidenceCollection,
    EvidenceSeverity,
    EvidenceSource,
    EvidenceType,
)


def test_evidence_source_creation():
    source = EvidenceSource(
        source_id="source:repository:src/builder/repository",
        source_type=EvidenceType.REPOSITORY,
        path=Path("src/builder/repository"),
        name="RepositoryPlatform",
    )

    assert source.source_id == "source:repository:src/builder/repository"
    assert source.source_type == EvidenceType.REPOSITORY
    assert source.path == Path("src/builder/repository")
    assert source.name == "RepositoryPlatform"


def test_evidence_creation_uses_stable_evidence_id():
    source = EvidenceSource(
        source_id="source:module:src/builder/repository/integration.py",
        source_type=EvidenceType.MODULE,
        path=Path("src/builder/repository/integration.py"),
        name="builder.repository.integration",
    )

    first = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=source,
        summary="RepositoryPlatform integrates perception services.",
        details="Public entry point composes EPIC-01 services.",
        severity=EvidenceSeverity.INFO,
        metadata={
            "epic": "EPIC-01",
            "sprint": "010",
        },
    )
    second = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=source,
        summary="RepositoryPlatform integrates perception services.",
        details="Public entry point composes EPIC-01 services.",
        severity=EvidenceSeverity.INFO,
        metadata={
            "sprint": "010",
            "epic": "EPIC-01",
        },
    )

    assert first.evidence_id == second.evidence_id
    assert first.evidence_type == EvidenceType.MODULE
    assert first.severity == EvidenceSeverity.INFO
    assert first.metadata == {
        "epic": "EPIC-01",
        "sprint": "010",
    }


def test_evidence_collection_count_and_filters():
    repository_source = EvidenceSource(
        source_id="source:repository:root",
        source_type=EvidenceType.REPOSITORY,
        path=Path("."),
        name="root",
    )
    module_source = EvidenceSource(
        source_id="source:module:alpha",
        source_type=EvidenceType.MODULE,
        path=Path("src/sample/alpha.py"),
        name="sample.alpha",
    )
    repository_evidence = Evidence.create(
        evidence_type=EvidenceType.REPOSITORY,
        source=repository_source,
        summary="Repository has source files.",
        details="RepositoryPlatform summary produced evidence.",
        severity=EvidenceSeverity.INFO,
    )
    module_warning = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=module_source,
        summary="Module has no matching test.",
        details="QA missing_tests produced warning.",
        severity=EvidenceSeverity.WARNING,
    )
    module_error = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=module_source,
        summary="Module violates policy.",
        details="Policy evidence produced error.",
        severity=EvidenceSeverity.ERROR,
    )

    collection = EvidenceCollection(
        items=(
            module_warning,
            repository_evidence,
            module_error,
        )
    )

    assert collection.count == 3
    assert collection.by_type(EvidenceType.MODULE).items == (
        module_error,
        module_warning,
    )
    assert collection.by_source(module_source.source_id).items == (
        module_error,
        module_warning,
    )
    assert collection.errors().items == (module_error,)
    assert collection.warnings().items == (module_warning,)
    assert collection.infos().items == (repository_evidence,)


def test_evidence_collection_returns_deterministic_ordering():
    source = EvidenceSource(
        source_id="source:module:sample",
        source_type=EvidenceType.MODULE,
        path=Path("src/sample.py"),
        name="sample",
    )
    zeta = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=source,
        summary="Zeta",
        details="Zeta detail",
        severity=EvidenceSeverity.INFO,
    )
    alpha = Evidence.create(
        evidence_type=EvidenceType.MODULE,
        source=source,
        summary="Alpha",
        details="Alpha detail",
        severity=EvidenceSeverity.INFO,
    )

    collection = EvidenceCollection(items=(zeta, alpha))

    assert collection.items == tuple(
        sorted(collection.items, key=lambda item: item.evidence_id)
    )


def test_evidence_models_are_immutable():
    source = EvidenceSource(
        source_id="source:document:architecture",
        source_type=EvidenceType.DOCUMENT,
        path=Path("docs/architecture/000_Master_Architecture.md"),
        name="Master Architecture",
    )
    evidence = Evidence.create(
        evidence_type=EvidenceType.DOCUMENT,
        source=source,
        summary="Architecture defines Evidence First.",
        details="Master architecture includes Evidence layer.",
        severity=EvidenceSeverity.INFO,
    )
    collection = EvidenceCollection(items=(evidence,))

    with pytest.raises(FrozenInstanceError):
        source.name = "Changed"

    with pytest.raises(FrozenInstanceError):
        evidence.summary = "Changed"

    with pytest.raises(FrozenInstanceError):
        collection.items = ()
