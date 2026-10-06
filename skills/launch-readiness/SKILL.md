---
name: launch-readiness
description: Run a cross-functional launch gate over product, UX, engineering, analytics, onboarding, support, discoverability and rollback. Use immediately before exposing an MVP to target users.
---

# launch-readiness

## Purpose

Decide whether the product is safe and useful enough to launch to the intended audience.

## Trigger

Use after core MVP functionality exists and runtime verification has begun.

**Do not use when:** Do not require enterprise polish for a small controlled beta; readiness must match launch scope.

## Inputs

### Required

- Launch scope/audience.
- Current product state.
- Known verification evidence.

### Optional

- Analytics plan.
- Support path.
- Onboarding.
- SEO/discovery needs.
- Rollback plan.

## Workflow

1. Define launch audience and blast radius.
2. Check core outcome and blocking UX states.
3. Check engineering/runtime evidence and known defects.
4. Check analytics for critical activation/conversion events.
5. Check onboarding, support and failure communication.
6. Check rollback or containment options.
7. Classify every issue as BLOCK, WARN or PASS.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Launch scope
- PASS items
- WARN items
- BLOCK items
- Evidence gaps
- Rollback/containment
- Go/no-go decision
- Next actions

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS means no BLOCK items for the defined launch scope. WARN is allowed only when risks are explicit and acceptable. FAIL/BLOCK means do not launch until the blocker is resolved or scope is reduced.

## Stop conditions

- A critical security/data-loss/runtime blocker exists.
- Launch audience is undefined, making acceptable risk impossible to judge.

## Anti-patterns

- Treating launch as a marketing date.
- Blocking a private beta on irrelevant enterprise requirements.
- Ignoring rollback because the MVP is small.

## Example

A five-user design-partner beta may tolerate manual support but not unverified authorization or data-loss risk.
