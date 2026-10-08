---
name: ppmax-idea-pressure-test
description: Stress-test a product idea before implementation by exposing assumptions, risks, alternatives and missing evidence. Use when a builder has an idea and is deciding whether it deserves deeper validation.
---

# ppmax-idea-pressure-test

## Purpose

Expose the weakest parts of an idea before implementation creates sunk cost.

## Trigger

Use when a user presents a product idea, feature concept or venture and wants to know whether it deserves deeper validation.

**Do not use when:** Do not use as a substitute for customer research, market research or runtime verification.

## Inputs

### Required

- A concise idea or proposed solution.

### Optional

- Target customer hypothesis.
- Known evidence.
- Constraints, unfair advantages or distribution access.

## Workflow

1. Restate the idea as a problem hypothesis and solution hypothesis.
2. List critical assumptions across problem, customer, behavior, distribution, feasibility and willingness to pay.
3. Identify the three assumptions that can kill the idea fastest.
4. Generate credible alternative explanations and substitute solutions.
5. Separate what is known from what is merely plausible.
6. Recommend the cheapest next evidence-producing action.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Problem hypothesis
- Solution hypothesis
- Critical assumptions ranked by risk
- Known evidence
- Unknowns
- Failure modes
- Cheapest next test
- Gate and decision

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS only when the problem and customer are specific enough to validate and no obvious contradiction makes further work irrational. WARN when validation can proceed but material unknowns remain. FAIL when the idea is contradictory, unsafe or too vague to test.

## Stop conditions

- No identifiable user or problem can be stated.
- The request jumps to implementation while critical assumptions remain completely unexamined; route to validation first.

## Anti-patterns

- Treating enthusiasm as evidence.
- Scoring an idea with arbitrary precision.
- Automatically recommending implementation.

## Example

Input: “Build an AI meeting notes SaaS.” Surface differentiation, ICP, switching and distribution assumptions; do not propose a stack yet.
