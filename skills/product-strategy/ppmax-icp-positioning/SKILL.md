---
name: ppmax-icp-positioning
description: Define a narrow ideal customer profile and positioning from validated problem evidence. Use when a product needs a specific audience, value proposition and reason to choose it.
---

# ppmax-icp-positioning

## Purpose

Make the target customer and product promise specific enough to drive scope and distribution.

## Trigger

Use after initial problem/customer evidence exists and before broad MVP scope or launch messaging.

**Do not use when:** Do not define an ICP using only broad firmographics such as “small businesses”.

## Inputs

### Required

- Problem evidence.
- Candidate customer segment.

### Optional

- Market landscape.
- Existing users.
- Distribution access.
- Buying roles.

## Workflow

1. Identify the segment with the strongest pain, frequency, consequence and reachable distribution.
2. Describe the trigger and job to be done.
3. Name current alternatives and why they are insufficient in this context.
4. Separate user, buyer and approver when they differ.
5. Draft a positioning statement grounded in evidence.
6. List exclusion criteria so the ICP stays narrow.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- ICP
- Exclusions
- Trigger
- Job to be done
- Pain/consequence
- Current alternative
- Buyer/user roles
- Value proposition
- Positioning statement
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS when the ICP is specific enough to identify real prospects and changes product/distribution choices. WARN when role or trigger uncertainty remains. FAIL when the ICP is only a broad label or has no evidence connection.

## Stop conditions

- No validated problem evidence exists; route back to validation.
- Multiple segments have incompatible needs; choose or branch rather than average them.

## Anti-patterns

- Everyone-is-a-customer positioning.
- Persona fiction unsupported by evidence.
- Differentiation based only on generic adjectives.

## Example

Replace “SMBs that need AI notes” with a segment such as recruiting agencies with repeated interview-scorecard work and reachable channels.
