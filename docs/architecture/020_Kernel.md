# Kernel Layer

## Role

The Kernel layer coordinates Builder Enterprise X capabilities. It is the operating core, not a replacement for domain layers.

## Responsibilities

- Compose public APIs from lower layers.
- Enforce constitutional constraints.
- Coordinate perception, evidence, reasoning, planning, execution, validation, and evolution.
- Avoid duplicating layer-specific logic.
- Preserve deterministic workflows.

## Kernel Principles

- Thin orchestration.
- Public API composition.
- No hidden repository scans.
- Explicit inputs and outputs.
- Validation before state-changing completion.

## Current Kernel Boundary

The current implementation does not yet introduce a full kernel. EPIC-01 provides the Perception entry point through `RepositoryPlatform`. Future Kernel work should consume `RepositoryPlatform` rather than bypass it.

## Future Kernel Inputs

- RepositoryPlatform
- Evidence bundles
- Knowledge graph snapshots
- User intent
- Policy constraints
- Validation results

## Future Kernel Outputs

- Decisions
- Plans
- Execution requests
- Validation requirements
- Learning records
