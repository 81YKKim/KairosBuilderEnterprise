# Architecture Principles

## Core Principles

1. Repository = Source of Truth
2. Evidence First
3. Architecture First
4. Evolution, not Rewrite
5. Composition over Duplication
6. Deterministic by Default
7. Public API First
8. Validation over Trust
9. AI Model Independence
10. Human-in-the-loop

## Repository = Source of Truth

The system must reason from the actual repository, not assumptions. Source files, tests, docs, Git state, and generated artifacts are evidence. Architecture documents guide intent, but repository state confirms reality.

## Evidence First

Every recommendation, plan, or change should be grounded in evidence. Evidence may include repository intelligence snapshots, tests, contracts, diffs, status output, runtime results, and user-approved requirements.

## Evolution, Not Rewrite

Builder Enterprise X evolves KairosBuilderEnterprise in place. Existing Generator, Desktop Generator, tests, architecture, and history remain protected assets.

## Composition over Duplication

New layers compose existing capabilities. They must not reimplement scanner, inventory, graph, query, QA, change analysis, or impact logic when public APIs already exist.

## Deterministic by Default

Ordering, counts, snapshots, and query results must be stable unless the repository changes.

## Public API First

Each layer exposes a small official API. Downstream layers use public entry points, not private implementation details.

## Validation over Trust

The system does not assume success. Tests, diffs, status, contracts, and explicit validation gates determine completion.

## AI Model Independence

Builder Enterprise X must not depend on a single AI model. Models are replaceable reasoning providers, not the architecture itself.

## Human-in-the-loop

Humans remain the authority for intent, approval, risk acceptance, and irreversible operations.

## Architecture First

Major capability growth begins by defining the architecture, contracts, evidence model, and validation path before implementation.
