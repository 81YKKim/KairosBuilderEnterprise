# Validation Layer

## Role

The Validation layer determines whether work is acceptable.

Validation is stronger than trust, assumptions, or successful code generation.

## Inputs

- Test results
- Diff output
- Git status
- Contract checks
- Runtime checks
- QA results
- Impact analysis

## Responsibilities

- Run required validation.
- Record pass/fail results.
- Identify residual risks.
- Prevent false completion claims.
- Provide evidence for Decision, Learning, and Memory layers.

## Outputs

- Validation reports
- Failed check details
- Passing baselines
- Residual risk notes

## Required Pattern

1. Run tests.
2. Inspect diff.
3. Inspect status.
4. Commit only passing scoped work when requested.

## Constraints

- Completion claims require validation evidence.
- Test failures must not be ignored.
- Validation commands are part of repository evidence.
