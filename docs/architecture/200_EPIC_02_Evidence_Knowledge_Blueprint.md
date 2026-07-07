# EPIC-02 Evidence / Knowledge Blueprint

## Purpose

EPIC-02 establishes the Evidence and Knowledge layers for Builder Enterprise X.

EPIC-01 completed the Perception layer. EPIC-02 must use `RepositoryPlatform` as its primary repository understanding input and must not directly rescan the repository.

## Evidence Layer Purpose

The Evidence layer records traceable facts. It captures what is known from repository perception, tests, diffs, status output, QA checks, impact analysis, architecture documents, and user-approved requirements.

Evidence does not decide. Evidence supports Knowledge, Reasoning, Policy, Decision, Planning, Validation, Learning, Memory, and Evolution.

## Knowledge Layer Purpose

The Knowledge layer organizes accepted evidence into reusable entities, relationships, and context.

Knowledge represents durable understanding across snapshots, validations, decisions, architecture, and history.

## Relationship to EPIC-01 Perception

EPIC-01 provides:

- `RepositoryPlatform`
- Repository summary and metrics
- Packages and modules
- Query facade
- QA results
- Change analysis
- Impact analysis
- Index and cache

EPIC-02 consumes these outputs. It must not duplicate scanner, inventory, graph, intelligence, query, QA, change, impact, or index behavior.

## Relationship to Future Reasoning Layer

The Reasoning layer will consume Evidence and Knowledge to interpret risk, identify options, and explain tradeoffs.

EPIC-02 must produce model-independent, deterministic structures that future reasoning can use without relying on a specific AI provider.

## Evidence Extraction

Evidence Extraction converts source outputs into evidence records.

Initial extraction sources:

- `RepositoryPlatform.summary()`
- `RepositoryPlatform.metrics()`
- `RepositoryPlatform.qa()`
- `RepositoryPlatform.analyze_change(...)`
- `RepositoryPlatform.analyze_impact(...)`
- `RepositoryPlatform.index`
- Test command output
- Git diff/stat/status text supplied as input
- Architecture markdown documents

Extraction rules:

- Preserve source name.
- Preserve source target.
- Preserve evidence type.
- Preserve raw value or normalized value.
- Preserve snapshot identity when available.
- Do not rescan the repository.

## Evidence Model

The Evidence Model should minimally include:

- evidence_id
- evidence_type
- source
- target
- value
- confidence
- snapshot_id
- created_at
- metadata

Evidence must be immutable where possible.

## Knowledge Entity

Knowledge entities are stable concepts derived from accepted evidence.

Initial entity types:

- Repository
- Package
- Module
- Test
- Resource
- QA Issue
- Change
- Impact
- Architecture Layer
- Validation Result
- Sprint
- Decision

Knowledge entity fields should include:

- entity_id
- entity_type
- name
- source_evidence
- attributes

## Knowledge Relationship

Knowledge relationships connect entities.

Initial relationship types:

- repository_contains_package
- package_contains_module
- module_has_test
- change_affects_module
- change_affects_package
- change_affects_test
- qa_issue_targets_entity
- evidence_supports_entity
- evidence_supports_relationship
- architecture_layer_depends_on_layer

Relationship fields should include:

- relationship_id
- relationship_type
- source_entity
- target_entity
- source_evidence
- attributes

## Knowledge Graph

The Knowledge Graph is the normalized relationship model used by future Reasoning, Policy, Decision, Planning, and Evolution layers.

It must:

- Consume Evidence and RepositoryPlatform outputs.
- Preserve deterministic ordering.
- Provide entity and relationship lookup.
- Avoid repository rescans.
- Avoid duplicating EPIC-01 graph behavior.

## Knowledge Query

Knowledge Query provides semantic access to entities and relationships.

Initial query capabilities:

- find_entity(...)
- find_relationship(...)
- entities_by_type(...)
- relationships_by_type(...)
- relationships_for_entity(...)
- evidence_for_entity(...)
- evidence_for_relationship(...)

## Knowledge Cache

Knowledge Cache stores reusable snapshots for future incremental reasoning.

It should include:

- snapshot_id
- created_at
- evidence_count
- entity_count
- relationship_count
- repository_snapshot_id
- validation_state

Snapshot IDs must be stable for equivalent inputs.

## Public API Principles

- Public API first.
- Immutable dataclasses where possible.
- Deterministic ordering.
- Composition over duplication.
- RepositoryPlatform as input.
- No direct scanner use outside EPIC-01 integration.
- No direct Git commands.

## Deterministic Rules

- Sort entities by type then id.
- Sort relationships by type, source, target, then id.
- Sort evidence by source, target, type, then id.
- Stable IDs should derive from normalized content.
- Cache IDs should exclude volatile timestamps.

## Validation Rules

- Evidence extraction tests must verify source traceability.
- Knowledge graph tests must verify entity and relationship counts.
- Query tests must verify deterministic ordering.
- Cache tests must verify stable snapshot IDs.
- Integration tests must verify RepositoryPlatform input.

## No Direct Repository Rescan Rule

EPIC-02 must not rescan repository files. It must consume `RepositoryPlatform` and supplied validation outputs.

If new repository facts are needed, EPIC-01 Perception should be extended first, then EPIC-02 can consume the new public output.

## Proposed Implementation Sequence

- Sprint #011 Evidence Model
- Sprint #012 Evidence Extractor
- Sprint #013 Knowledge Model
- Sprint #014 Knowledge Graph
- Sprint #015 Knowledge Query
- Sprint #016 Knowledge Cache
- Sprint #017 Evidence Validation
- Sprint #018 Knowledge Integration

## Acceptance Criteria

- Evidence and Knowledge architecture documented.
- EPIC-02 has a test-first implementation sequence.
- RepositoryPlatform is the official input.
- No direct repository rescan is allowed.
- Future Reasoning layer has deterministic inputs.
