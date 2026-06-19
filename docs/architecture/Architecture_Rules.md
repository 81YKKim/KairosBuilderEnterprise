# Kairos Builder Enterprise Architecture Rules

## Frozen Layer Order

CLI

↓

Application

↓

Domain

↓

Services

↓

Infrastructure

## Rules

1. CLI contains no business logic.
2. Application coordinates workflows.
3. Domain contains business rules only.
4. Services implement use cases.
5. Infrastructure accesses OS, Git, JSON and Files.
6. PowerShell is only a Windows execution wrapper.
7. Python standard library is preferred.
8. Every Sprint must pass pytest.

## Future Rules

- Circular Dependency Detection
- Import Graph Validation
- Architecture Score
- AI Refactoring Suggestions
- Automatic Documentation
