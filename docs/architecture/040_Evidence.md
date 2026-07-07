# Evidence Layer

## Role

The Evidence layer converts observed facts into traceable, reusable proof units.

EPIC-02 begins here.

## Evidence Sources

- RepositoryPlatform summaries and metrics
- Repository queries
- QA results
- Change analysis
- Impact analysis
- Index and cache snapshots
- Test output
- Git diff and status output
- Contract checks
- Runtime validation
- User-approved requirements

## Evidence Requirements

Evidence must be:

- Traceable to a source
- Deterministic where possible
- Timestamped or snapshot identified when persisted
- Separated from interpretation
- Usable by future Knowledge, Reasoning, Policy, and Decision layers

## Evidence First Workflow

1. Observe repository or validation output.
2. Normalize into evidence records.
3. Preserve source references.
4. Attach confidence or validation status when applicable.
5. Pass evidence to Knowledge and Reasoning layers.

## Non-goals

Evidence does not decide. It records facts. Decisions belong to the Decision layer after Reasoning and Policy have evaluated the evidence.
