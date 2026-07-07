# Knowledge Layer

## Role

The Knowledge layer organizes evidence into reusable concepts, relationships, and historical context.

EPIC-02 should define this layer after the Evidence foundation.

## Knowledge Types

- Repository entities
- Package and module relationships
- Test coverage relationships
- QA issue patterns
- Change and impact patterns
- Architecture contracts
- Decision records
- Validation outcomes
- Sprint history
- Evolution history

## Relationship to Perception

Perception answers what exists now.

Knowledge answers what the system knows across evidence, time, and accepted context.

## Relationship to Reasoning

Reasoning consumes Knowledge to form interpretations, identify risks, and produce options. Knowledge must remain structured enough to support multiple AI models and deterministic non-AI consumers.

## Future Knowledge Graph

The Knowledge Graph should consume:

- RepositoryIndex
- RepositoryCache
- Evidence records
- Architecture documents
- Test and validation results
- Accepted human decisions

It must not duplicate scanning, inventory, graph, query, or QA logic.
