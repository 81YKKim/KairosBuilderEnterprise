# Reasoning Layer

## Role

The Reasoning layer interprets Evidence and Knowledge to identify risks, options, tradeoffs, and recommended next steps.

Reasoning does not execute changes. It produces explainable conclusions that downstream Policy, Decision, and Planning layers can evaluate.

## Inputs

- Evidence records
- Knowledge entities and relationships
- RepositoryPlatform summaries
- QA and impact results
- Architecture constraints
- User intent

## Responsibilities

- Explain why a condition matters.
- Compare possible actions.
- Identify uncertainty and missing evidence.
- Separate facts from interpretation.
- Produce deterministic reasoning traces where possible.
- Remain AI model independent.

## Outputs

- Reasoning reports
- Risk explanations
- Option sets
- Tradeoff summaries
- Evidence references

## Constraints

- Must not rescan the repository directly.
- Must consume Evidence and Knowledge APIs.
- Must not bypass Policy or Decision layers.
- Must preserve human-in-the-loop control for consequential choices.
