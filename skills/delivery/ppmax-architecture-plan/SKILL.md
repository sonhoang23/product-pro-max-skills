---
name: ppmax-architecture-plan
description: Create a proportionate software architecture plan from product constraints, risks and verification needs. Use before significant implementation or when architecture choices need explicit trade-offs.
---

# ppmax-architecture-plan

## Purpose

Choose the simplest architecture that satisfies current product constraints while preserving necessary reversibility.

## Trigger

Use after MVP scope and core flows are sufficiently defined.

**Do not use when:** Do not introduce enterprise patterns, microservices or infrastructure without a constraint that justifies them.

## Inputs

### Required

- MVP scope.
- Core flows.
- Known technical constraints.

### Optional

- Existing stack.
- Team skills.
- Compliance/security requirements.
- Expected load.
- Integration constraints.

## Workflow

1. Extract architectural drivers from product requirements and constraints.
2. Identify system boundaries and data crossing them.
3. Choose the simplest viable components and persistence model.
4. Document material trade-offs and rejected alternatives.
5. Define failure boundaries, migration/rollback considerations and security-sensitive areas.
6. Define how critical architecture assumptions will be verified.
7. Record decisions as concise ADR-style entries.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Drivers
- Proposed architecture
- Boundaries
- Data model direction
- Key decisions/trade-offs
- Rejected alternatives
- Risks
- Verification plan
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when every significant component maps to a current requirement and material risks have verification paths. WARN when reversible uncertainty remains. FAIL when architecture is driven mainly by hypothetical scale or undefined requirements.

## Stop conditions

- Critical product scope is changing too rapidly for irreversible decisions.
- A regulated/security constraint is unknown and could change the design.

## Anti-patterns

- Resume-driven architecture.
- Microservices by default.
- Treating a diagram as proof the architecture works.

## Example

For a small MVP, prefer a modular monolith unless independent scaling, isolation or team boundaries justify more complexity.
