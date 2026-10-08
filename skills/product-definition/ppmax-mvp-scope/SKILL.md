---
name: ppmax-mvp-scope
description: Reduce a product idea to the smallest coherent MVP that tests the critical product hypothesis. Use when deciding what to build now, later or explicitly not at all.
---

# ppmax-mvp-scope

## Purpose

Cut scope until every included capability is necessary to test the most important hypothesis.

## Trigger

Use after a problem/ICP hypothesis is clear enough to define the product test.

**Do not use when:** Do not use MVP as shorthand for low quality or a miniature full roadmap.

## Inputs

### Required

- Critical product hypothesis.
- Target user/ICP.
- Desired user outcome.

### Optional

- Constraints.
- UX flow.
- Existing product/code.
- Validation evidence.

## Workflow

1. State the single critical hypothesis the MVP must test.
2. Define the minimum end-to-end user outcome.
3. List candidate capabilities and map each to the hypothesis.
4. Remove capabilities that do not materially affect the test.
5. Create explicit now, later and not-building lists.
6. Define success, failure and kill criteria.
7. Check that remaining scope is still a coherent user experience.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Critical hypothesis
- MVP outcome
- Must build now
- Later
- Explicitly not building
- Success criteria
- Failure/kill criteria
- Risks
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when scope can test the hypothesis end to end and every must-have has a reason to exist. WARN when dependencies create unavoidable extra scope. FAIL when scope is still roadmap-shaped or cannot produce a meaningful test.

## Stop conditions

- The hypothesis is undefined.
- Features keep being added without connection to the test.
- Removing scope destroys the core outcome; redesign the experiment instead.

## Anti-patterns

- Calling every requested feature must-have.
- Using MVP to justify broken UX.
- Building infrastructure for hypothetical future scale.

## Example

For an interview-scorecard product, keep transcript → rubric scorecard → reviewer correction → export; defer generic meeting assistant features.
