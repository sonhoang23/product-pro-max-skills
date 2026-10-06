---
name: market-landscape
description: Map direct competitors, indirect competitors, substitutes, manual workarounds and do-nothing behavior for a product problem. Use when positioning, differentiation or market understanding is needed.
---

# market-landscape

## Purpose

Understand the real set of alternatives a customer can choose instead of the proposed product.

## Trigger

Use after a problem and customer segment are specific enough to define a market context.

**Do not use when:** Do not treat a list of companies as a market analysis.

## Inputs

### Required

- Problem definition.
- Target segment.

### Optional

- Known competitors.
- Research sources.
- Geography or industry constraints.

## Workflow

1. Define the customer job and buying context.
2. Separate direct competitors, indirect competitors, substitutes, manual workarounds and do-nothing.
3. Compare alternatives on dimensions that matter to the target segment.
4. Identify crowded claims and under-served trade-offs.
5. Separate sourced facts from inference.
6. Translate findings into positioning questions, not automatic feature requests.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Market frame
- Alternative categories
- Comparison dimensions
- Evidence/source notes
- Crowded claims
- Possible whitespace
- Risks
- Gate
- Next action

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when the landscape includes non-software alternatives and enough evidence to inform positioning. WARN when sources are partial. FAIL when the segment/problem is too vague to define meaningful alternatives.

## Stop conditions

- The analysis starts optimizing against competitors before customer value is clear.
- External facts are requested without source access; mark them as research needed.

## Anti-patterns

- Feature-table theater.
- Assuming no competitor means no market.
- Ignoring spreadsheets, services, internal tools and doing nothing.

## Example

For invoice follow-up at small agencies, include accounting suites, email/calendar workflows, assistants and tolerating late payment.
