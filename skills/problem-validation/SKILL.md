---
name: problem-validation
description: Evaluate whether a customer problem has enough real evidence to justify product investment. Use before committing MVP scope or when a team is unsure whether observed pain is real, frequent and consequential.
---

# problem-validation

## Purpose

Decide whether the problem deserves further product investment.

## Trigger

Use after an idea has a reasonably specific problem hypothesis and before major solution commitment.

**Do not use when:** Do not fabricate interviews, demand, metrics or willingness-to-pay evidence.

## Inputs

### Required

- Problem hypothesis.
- Target customer or segment hypothesis.

### Optional

- Interview notes.
- Behavioral data.
- Support tickets.
- Community/search evidence.
- Payment or switching signals.

## Workflow

1. Define the exact problem, actor, context and consequence.
2. Inventory evidence and classify every item using the evidence model.
3. Test frequency, severity, recurrence and current workaround.
4. Look for behavior stronger than stated preference.
5. Actively search supplied evidence for contradictions.
6. Identify missing evidence that could change the decision.
7. Return a gate and a decision: continue, research, revise, pivot, defer or stop.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Problem statement
- Evidence table
- Contradictory evidence
- Open assumptions
- Validation verdict
- Gate
- Decision
- Next evidence action

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS requires multiple independent signals that the defined problem is real and consequential for the target segment. WARN allows continuation only with explicit unresolved risk. FAIL means required evidence is absent or materially contradicts the hypothesis.

## Stop conditions

- Evidence is invented or unverifiable.
- The problem changes during analysis; revise the hypothesis before judging it.
- Available evidence cannot distinguish problem pain from solution enthusiasm.

## Anti-patterns

- Counting competitor existence as demand validation.
- Using survey intent as equivalent to behavior.
- Calling a problem validated from one anecdote.

## Example

Given three interview summaries, classify the evidence, preserve contradictions and refuse PASS if all signals are only stated interest.
