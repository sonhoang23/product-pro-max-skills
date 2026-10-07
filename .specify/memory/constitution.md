# Product Pro Max Skills Development Constitution

## Core Principles

### I. Evidence Before Confidence
Claims MUST distinguish observed or provided evidence from assumptions and inference. Confidence MUST increase only when traceable evidence supports it. Missing or contradictory evidence MUST remain visible.

### II. Verification Before Done
Implemented, statically checked, tested, runtime verified, browser verified, and production verified are distinct states. Contributors and agents MUST NOT claim a stronger verification state than the evidence demonstrates.

### III. Product Outcome Over Artifact Production
A document, diagram, schema, code diff, or analysis is not progress by itself. Every artifact MUST reduce risk, improve a decision, enable execution, or verify an outcome.

### IV. Users Over Features
Scope MUST prefer the smallest coherent change that tests or improves the most important product outcome. Skill count, document count, and feature count are not success metrics.

### V. Distribution Is Part of the Product
Product work MUST consider how intended users can realistically discover, adopt, and benefit from the result when distribution is relevant to the lifecycle phase.

### VI. Reversible Decisions Under Uncertainty
STOP, PIVOT, REPEAT, BACKTRACK, DEFER, and ESCALATE are valid outcomes. Weak evidence MUST NOT be hidden merely to keep a workflow moving.

### VII. Never Invent Evidence
Interviews, metrics, quotes, research findings, runtime results, test execution, competitor behavior, and operational observations MUST NOT be fabricated.

### VIII. Deterministic Checks Where Practical
Mechanically verifiable claims SHOULD use schemas, validators, tests, commands, or directly observable runtime evidence when a reliable deterministic check is practical.

### IX. Complexity Must Match Product Stage
Architecture, process, governance, metadata, and automation MUST remain proportionate to demonstrated needs. Added complexity requires a concrete constraint or scale problem.

### X. Durable State Over Chat Memory
Important assumptions, evidence, decisions, contracts, and lifecycle state MUST be persisted in repository artifacts when they are expected to survive a conversation or agent session.

### XI. Composable, Bounded Skills
Each canonical skill MUST have one clear responsibility, explicit inputs and outputs, and a defined boundary. A new skill MUST NOT duplicate an existing responsibility that can be solved with a small extension.

### XII. Canonical Contracts Before Derived Views
Shared product semantics MUST have an explicit canonical source. README text, diagrams, examples, schemas, templates, and localized documentation MUST NOT silently redefine canonical semantics.

### XIII. Global-First, Machine-Readable by Default
Canonical repository logic and machine identifiers MUST use English and stable ASCII identifiers. User-facing output MAY follow the user's language. Important shared contracts SHOULD have machine-readable forms.

## Foundation Constraints

- Repository product surfaces and repository-development tooling MUST remain conceptually separate.
- Canonical machine identifiers MUST be stable within a declared compatibility boundary.
- Gate results and workflow decisions MUST remain separate concepts.
- Planned truth and implemented truth MUST be labeled distinctly.
- Project-level documentation MUST describe implemented truth unless explicitly marked as roadmap or proposal material.
- Global-first documentation MUST favor explicit terminology, stable paths, searchable headings, and standalone examples.

## Development Workflow

Work MUST follow the authority chain:

```text
constitution
  > spec.md
    > plan.md + design artifacts
      > tasks.md
        > implementation state
```

Derived diagrams and navigation artifacts do not create new requirements. If implementation exposes a required semantic change, the authoritative upstream artifact MUST be updated.

For Spec Kit work:
1. specify requirements and measurable outcomes;
2. resolve material ambiguity;
3. satisfy the Lazy Modeling Gate for the upstream phase;
4. plan implementation and contracts;
5. create traceable tasks;
6. implement and verify required evidence;
7. promote verified shared semantics to project-level documentation;
8. converge intended and implemented state before declaring completion.

## Governance

This constitution governs development of Product Pro Max Skills. The public `CONSTITUTION.md` remains the product-system principles document; this file governs repository change delivery.

Amendments require an explicit reason, impact analysis, and a migration plan when an existing contract would become invalid.

Constitution versions use semantic versioning: MAJOR for incompatible governance changes, MINOR for new principles or materially expanded governance, PATCH for clarification only.

Compliance with MUST statements is required before a feature can converge.

**Version**: 1.0.0 | **Ratified**: 2026-10-07 | **Last Amended**: 2026-10-07
