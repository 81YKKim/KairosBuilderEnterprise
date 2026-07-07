# Policy Layer

## Role

The Policy layer defines which actions are allowed, blocked, restricted, or require human approval.

Policy turns constitutional principles into operational rules.

## Inputs

- Constitution rules
- Evidence records
- Knowledge relationships
- Reasoning outputs
- Repository risk state
- Human approval context

## Responsibilities

- Enforce repository-first behavior.
- Protect existing Generator and Desktop Generator contracts.
- Require validation before completion.
- Gate destructive operations.
- Gate push, publish, release, and deployment operations.
- Define allowed automation boundaries.

## Outputs

- Allow / deny / require approval decisions
- Policy violations
- Required validation gates
- Human approval requirements

## Core Rules

- Evolution, not rewrite.
- Validation over trust.
- Public API first.
- No direct repository rescan when an approved layer already provides the evidence.
- No irreversible action without explicit approval.
