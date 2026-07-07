# Constitution Layer

## Role

The Constitution layer defines non-negotiable system rules for Builder Enterprise X.

It answers:

- What is the source of truth?
- What is protected?
- What may the system do autonomously?
- What requires human approval?
- What validation gates must pass?

## Constitutional Rules

- The repository is the source of truth.
- Existing Generator and Desktop Generator contracts are protected.
- Evolution happens in place; rewrites require explicit authorization.
- Python changes require full clean file-level fixes.
- Tests must remain green before completion claims.
- Git history is preserved.
- Push operations require explicit instruction.
- Destructive actions require explicit approval.

## Authority Boundaries

The system may:

- Read repository state.
- Create additive implementation under approved scope.
- Add tests first.
- Run validation.
- Commit approved passing work.

The system must not:

- Create a new repository unless explicitly asked.
- Rewrite stable production subsystems without scope.
- Trust generated plans without repository evidence.
- Push unless explicitly instructed.

## Outputs

- Rules
- Constraints
- Approval boundaries
- Validation gates
- Protected subsystem list
