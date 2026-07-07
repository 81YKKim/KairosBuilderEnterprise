# Planning Layer

## Role

The Planning layer converts decisions into ordered, testable work.

Plans are not implementation. They define scope, sequence, validation, and rollback awareness.

## Inputs

- Decision records
- Policy gates
- Evidence and Knowledge references
- Repository impact analysis
- User constraints

## Responsibilities

- Break decisions into small steps.
- Preserve test-first workflow.
- Identify files and APIs likely affected.
- Define validation commands.
- Identify commit boundaries.
- Avoid scope creep.

## Outputs

- Task plans
- Sprint plans
- Validation plans
- Risk notes
- Rollback notes

## Constraints

- Must not bypass public APIs.
- Must not plan rewrites unless explicitly authorized.
- Must be deterministic enough to audit.
