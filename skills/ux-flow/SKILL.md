---
name: ux-flow
description: Design or audit an end-to-end product flow including success, error, empty, loading, permission and recovery states. Use before UI implementation or when an existing flow feels incomplete.
---

# ux-flow

## Purpose

Ensure critical user goals work across normal and failure states, not just the happy path.

## Trigger

Use when a concrete user goal and MVP scope exist.

**Do not use when:** Do not turn the skill into visual styling or brand design unless explicitly requested.

## Inputs

### Required

- User goal.
- MVP scope or feature boundary.

### Optional

- Existing screens.
- Platform constraints.
- Accessibility requirements.
- Known error cases.

## Workflow

1. Define entry and success conditions.
2. Map the shortest happy path.
3. Add empty, loading, error, permission and interrupted states.
4. Add recovery paths for failures users can reasonably fix.
5. Check destructive/irreversible actions and loss of work.
6. Check accessibility implications where relevant.
7. Remove steps that do not contribute to the user goal.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- User goal
- Happy path
- State matrix
- Error/recovery paths
- Edge cases
- Accessibility notes
- Open questions
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when every critical user goal has a complete path and recoverable failures are addressed. WARN when non-critical edge cases remain. FAIL when a critical path dead-ends or depends on undefined behavior.

## Stop conditions

- Product rules are missing for a critical state; resolve the rule instead of inventing UX.
- The requested flow exceeds agreed MVP scope.

## Anti-patterns

- Designing only screenshots.
- Hiding errors behind generic toasts.
- Ignoring empty and permission states.

## Example

For upload → generate → review → export, cover invalid files, slow processing, generation failure, missing rubric, permissions and retry.
