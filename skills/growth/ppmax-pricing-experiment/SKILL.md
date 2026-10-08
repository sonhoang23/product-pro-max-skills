---
name: ppmax-pricing-experiment
description: Turn pricing into a falsifiable hypothesis about value metric, package, segment and willingness to pay. Use before choosing or changing a monetization model.
---

# ppmax-pricing-experiment

## Purpose

Test pricing and monetization assumptions instead of guessing a number from competitors.

## Trigger

Use when a target segment and meaningful product outcome are defined.

**Do not use when:** Do not present a precise price as validated without willingness-to-pay or transaction evidence.

## Inputs

### Required

- ICP.
- Product outcome/value proposition.

### Optional

- Current pricing.
- Competitor pricing.
- Customer interviews.
- Usage data.
- Cost constraints.

## Workflow

1. Identify the customer outcome and plausible value metric.
2. Separate pricing model, packaging and price level.
3. List evidence for willingness to pay and budget ownership.
4. Generate a small number of pricing hypotheses.
5. Design the cheapest ethical experiment that can distinguish them.
6. Define success/failure thresholds before running the experiment.
7. Record what evidence would justify changing the model.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Value metric hypothesis
- Pricing model hypotheses
- Packaging hypothesis
- Evidence
- Experiment design
- Success threshold
- Failure threshold
- Risks
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS means the pricing experiment can produce decision-relevant evidence. WARN when the model is plausible but buyer/budget evidence is incomplete. FAIL when price is selected purely by intuition or superficial competitor copying.

## Stop conditions

- No buyer or value outcome is known; return to ICP/value definition.
- The experiment would mislead customers or create unfair commitments.

## Anti-patterns

- Competitor average equals correct price.
- Picking $19/month because it feels SaaS-like.
- Treating stated willingness to pay as equivalent to purchase behavior.

## Example

Test per-recruiter versus per-interview value metrics with buyer conversations or purchase behavior rather than choosing a tier by aesthetics.
