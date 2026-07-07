# Decision Layer

## Role

The Decision layer selects one valid action from the options produced by Reasoning and constrained by Policy.

Decision is explicit. It should be traceable to evidence, policy, and human intent.

## Inputs

- Reasoning options
- Policy results
- Evidence references
- Knowledge context
- User requirements

## Responsibilities

- Choose a path of action.
- Record why alternatives were not selected.
- Preserve confidence and uncertainty.
- Identify required validation.
- Defer to humans when authority is required.

## Outputs

- Decision records
- Selected action
- Rejected alternatives
- Validation requirements
- Approval requirements

## Constraints

- Must not execute directly.
- Must not invent evidence.
- Must remain explainable and auditable.
