# EPIC-03 Reasoning Blueprint

## Purpose

EPIC-03 establishes the Reasoning layer for Builder Enterprise X.

Reasoning sits between Knowledge and Policy.

Knowledge provides accepted facts and relationships. Reasoning interprets those facts into evidence-backed inferences, constraints, confidence, conflicts, and explanations. Policy then limits which actions are allowed or forbidden. Decision chooses from Reasoning and Policy outputs.

Reasoning does not execute work, modify code, scan the repository, or plan implementation steps.

## Position in the Architecture

Builder Enterprise X evolves through the architecture stack:

- Constitution
- Kernel
- Perception
- Evidence
- Knowledge
- Reasoning
- Policy
- Decision
- Planning
- Execution
- Validation
- Learning
- Memory
- Evolution

EPIC-01 completed repository perception through `RepositoryPlatform`.

EPIC-02 completed the Evidence / Knowledge integration path:

`RepositoryPlatform -> EvidenceExtractor -> EvidenceCollection -> KnowledgeExtractor -> KnowledgeCollection -> KnowledgeGraph -> KnowledgeQuery -> KnowledgeCache`

EPIC-03 consumes that path. It must not bypass or rebuild it.

## Reasoning Layer Purpose

The Reasoning layer converts Knowledge into explainable interpretation.

It answers questions such as:

- What facts support this conclusion?
- What constraints are relevant?
- What risks or conflicts exist?
- What confidence should be assigned?
- What evidence is missing?
- Which conclusions should be passed to Policy and Decision?

Reasoning is not a general chat layer. It is a deterministic, evidence-backed interpretation layer for software development operations.

## Inputs

Reasoning may consume:

- `KnowledgePlatform`
- `KnowledgeQuery`
- `KnowledgeGraph`
- `KnowledgeCache`
- Evidence references
- Knowledge entities
- Knowledge relationships
- Repository summaries already captured by EPIC-01 and EPIC-02
- Future Policy rules supplied as input
- User-approved intent or task context supplied as input

Reasoning must not consume:

- Direct filesystem scans
- Direct Git commands
- Raw repository traversal outside `RepositoryPlatform`
- Unverified model-generated facts

## Outputs

Reasoning produces structured outputs for Policy, Decision, Planning, Validation, and human review.

Initial output concepts:

- `ReasoningResult`
- `Inference`
- `ConstraintResult`
- Confidence score
- Conflict list
- Explanation
- Evidence references

Reasoning output must preserve the evidence path that supports each conclusion.

## ReasoningResult

`ReasoningResult` is the top-level reasoning response.

It should include:

- result_id
- question or objective
- inferences
- constraint_results
- conflicts
- confidence_score
- explanation
- evidence_ids
- metadata

The result must be immutable where possible and deterministic for equivalent inputs.

## Inference

An `Inference` is a conclusion derived from Knowledge and Evidence.

It should include:

- inference_id
- statement
- inference_type
- source_entity_ids
- source_relationship_ids
- evidence_ids
- confidence_score
- metadata

An inference is invalid if it cannot cite evidence or knowledge references.

## Constraint Result

A `ConstraintResult` records whether a reasoning constraint is satisfied.

It should include:

- constraint_id
- name
- passed
- severity
- target
- evidence_ids
- explanation

Policy rules can later consume constraint results, but the Reasoning layer must not make final action decisions.

## Confidence Score

Confidence scores express how strongly the available evidence supports an inference.

Rules:

- Confidence must be derived from explicit evidence and knowledge references.
- Confidence must not be inflated by model fluency.
- Missing evidence lowers confidence.
- Conflicting evidence lowers confidence.
- Policy approval does not increase reasoning confidence.

Initial score range:

- `0.0` means unsupported.
- `1.0` means fully supported by available accepted evidence.

## Conflict List

Conflicts identify incompatible facts, rules, assumptions, or conclusions.

Initial conflict examples:

- Knowledge says a module exists, but no evidence supports it.
- A package has modules but no matching test evidence.
- Two inferences recommend incompatible directions.
- A future policy rule disallows an inferred action.
- Required evidence is missing.

Conflict records should include:

- conflict_id
- severity
- statement
- involved_inference_ids
- involved_evidence_ids
- explanation

## Explanation

Explanation is a structured account of why a reasoning result exists.

It should include:

- concise conclusion
- supporting facts
- evidence references
- assumptions
- uncertainty
- conflicts
- rejected alternatives when available

Explanation must remain traceable and model independent.

## Components

### Reasoning Model

Defines immutable domain objects:

- `ReasoningResult`
- `Inference`
- `ConstraintResult`
- `ReasoningConflict`
- `ReasoningExplanation`

### Inference Engine

Derives inferences from `KnowledgePlatform`, `KnowledgeQuery`, and `KnowledgeGraph`.

It must not create facts that are absent from Knowledge or Evidence.

### Rule Engine

Evaluates deterministic reasoning rules.

Initial rule examples:

- Every inference must cite evidence.
- Missing tests increase uncertainty.
- Unsupported architecture claims are rejected.
- Repository facts must originate from `RepositoryPlatform` through EPIC-02.

### Constraint Engine

Checks reasoning constraints before results are passed downstream.

It may evaluate future Policy rules as input, but it does not own Policy.

### Confidence Scoring

Assigns confidence to inferences and results.

The scoring system must be simple, explainable, deterministic, and testable.

### Conflict Resolver

Identifies conflicts and ranks them.

Resolution means making conflicts explicit, not silently choosing an action.

### Explanation Builder

Creates concise, evidence-backed explanations from inferences, constraints, conflicts, and confidence scores.

### Reasoning Integration

Provides the single public entry point for EPIC-03.

It composes:

- Knowledge input
- Inference Engine
- Rule Engine
- Constraint Engine
- Confidence Scoring
- Conflict Resolver
- Explanation Builder

## Public API Principles

The Reasoning public API should be small, stable, and compositional.

Candidate entry point:

`ReasoningPlatform`

Candidate factory:

- `build(knowledge_platform)`
- `create(knowledge_platform)`

Candidate public methods:

- `reason_about(objective)`
- `infer(objective)`
- `evaluate_constraints(...)`
- `score_confidence(...)`
- `conflicts(...)`
- `explain(...)`
- `validate()`

The API must accept already-built Knowledge inputs. It must not rebuild `RepositoryPlatform`, Evidence, Knowledge, Graph, Query, or Cache.

## Principles

### Evidence-Backed Only

Every inference must reference Evidence, Knowledge entities, or Knowledge relationships.

### No Hallucinated Facts

Reasoning may infer from accepted facts. It must not invent repository facts, architecture claims, test results, commits, branches, or file contents.

### Deterministic by Default

Equivalent inputs should produce equivalent IDs, ordering, scores, conflicts, and explanations.

### Explainable Reasoning

Each result must explain why it exists and which evidence supports it.

### No Direct Repository Scan

Reasoning consumes `KnowledgePlatform` and its public APIs only.

### No Direct Code Modification

Reasoning produces interpretation. It does not edit files.

### No Decision Execution

Reasoning can describe options and risks. Decision and Execution layers own selection and action.

### No Planning Logic

Reasoning does not create implementation plans. Planning consumes Decision output later.

## Relationship to Knowledge

Knowledge answers:

- What exists?
- What is related?
- What evidence supports it?

Reasoning answers:

- What does that imply?
- How strong is the support?
- What conflicts or gaps exist?
- What explanation should downstream layers receive?

## Relationship to Policy

Policy answers:

- What is allowed?
- What is forbidden?
- What requires human approval?

Reasoning can evaluate supplied policy-like constraints, but it must not become the Policy layer.

## Relationship to Decision

Decision answers:

- Which option should be selected?

Reasoning may produce ranked or explained options, but it must not finalize action selection.

## Validation Rules

Reasoning tests must verify:

- No direct repository scan.
- No direct Git command.
- KnowledgePlatform input is reused.
- Inferences require evidence references.
- Conflicts are deterministic.
- Confidence scores are deterministic.
- Explanations cite evidence.
- Existing EPIC-01 and EPIC-02 tests remain green.

## Proposed Implementation Sequence

- Sprint #019 Reasoning Model
- Sprint #020 Inference Engine
- Sprint #021 Rule Engine
- Sprint #022 Constraint Engine
- Sprint #023 Confidence Scoring
- Sprint #024 Conflict Resolver
- Sprint #025 Explanation Builder
- Sprint #026 Reasoning Integration

## Acceptance Criteria

EPIC-03 is complete when:

- Reasoning has a single public entry point.
- Reasoning consumes `KnowledgePlatform`.
- Reasoning does not scan repositories.
- Reasoning does not modify code.
- Reasoning does not execute decisions.
- All inferences are evidence-backed.
- Confidence, conflicts, and explanations are deterministic.
- Root and Builder tests remain green.
