# Perception Layer

## Role

The Perception layer turns repository state into structured, queryable understanding.

## Completed EPIC-01 Capabilities

The current Perception chain is:

```text
RepositoryScanner
→ RepositoryInventory
→ RepositoryGraph
→ RepositoryIntelligence
→ RepositoryQuery
→ RepositoryQA
→ RepositoryChangeAnalyzer
→ RepositoryImpactAnalyzer
→ RepositoryIndex
→ RepositoryPlatform
```

## Responsibilities

- Scan repository files and directories.
- Build normalized inventory.
- Build package and module graph.
- Provide repository intelligence and metrics.
- Provide query facade.
- Diagnose QA issues.
- Analyze change and impact from path inputs.
- Build reusable index and cache snapshots.
- Provide a single public integration entry point.

## Constraints

- Higher layers must not rescan the repository when Perception output is available.
- Query, QA, change, impact, and index layers must consume existing public APIs.
- Ordering must remain deterministic.

## Public Entry Point

`RepositoryPlatform` is the official Perception public entry point.

## Current Validation

- Root tests: `78 passed`
- Legacy Builder tests: `139 passed`
