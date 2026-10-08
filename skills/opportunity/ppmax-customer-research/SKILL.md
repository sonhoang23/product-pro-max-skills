---
name: ppmax-customer-research
description: Plan or synthesize customer research into traceable observations, pains, workarounds and buying signals. Use for interviews, notes, support conversations or qualitative research before product decisions.
---

# ppmax-customer-research

## Purpose

Turn customer conversations into evidence without turning researcher interpretation into fake facts.

## Trigger

Use to design interviews or synthesize existing qualitative customer material.

**Do not use when:** Do not use leading questions to seek confirmation of a preferred solution.

## Inputs

### Required

- Research objective or existing research material.

### Optional

- ICP hypothesis.
- Interview transcripts or notes.
- Current product behavior.
- Decision the research should inform.

## Workflow

1. State the decision the research must inform.
2. If planning research, create non-leading questions focused on past behavior, context, consequence and workaround.
3. If synthesizing, extract observations before themes.
4. Separate verbatim evidence, researcher inference and assumption.
5. Cluster repeated pains, triggers, workarounds and buying/switching signals.
6. Record contradictory or segment-specific patterns.
7. Recommend the next research action only where evidence remains decision-relevant.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Research objective
- Observations
- Repeated patterns
- Workarounds
- Buying/switching signals
- Contradictions
- Inferences
- Open questions
- Next action
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when the research set is sufficient for the specific decision being asked. WARN when useful patterns exist but sampling or contradictions remain. FAIL when material is too thin, too leading or too detached from behavior.

## Stop conditions

- Source material is missing while synthesis is requested.
- The requested conclusion is predetermined and evidence is being cherry-picked.

## Anti-patterns

- Asking “Would you use this?” as primary validation.
- Collapsing quotes and inference.
- Ignoring customers who contradict the thesis.

## Example

Given six interview notes, identify repeated manual workarounds and clearly label any conclusion that is an inference.
