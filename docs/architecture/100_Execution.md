# Execution Layer

## Role

The Execution layer performs approved repository operations.

Execution is controlled, scoped, and validated. It is not autonomous permission to change anything.

## Inputs

- Approved plans
- Policy approvals
- Human instructions
- Validation requirements
- Repository state

## Responsibilities

- Modify files only within approved scope.
- Preserve existing architecture.
- Use full clean fixes for Python files.
- Avoid duplicating existing layer logic.
- Produce diffs for review.
- Commit only after validation passes when requested.

## Outputs

- File changes
- Generated artifacts
- Test results
- Diff summaries
- Commits

## Constraints

- No push unless explicitly requested.
- No destructive action without explicit approval.
- No direct rewrite of protected Generator or Desktop Generator contracts without scope.
