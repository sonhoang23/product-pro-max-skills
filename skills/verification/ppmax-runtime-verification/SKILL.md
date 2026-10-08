---
name: ppmax-runtime-verification
description: Verify a running product and distinguish implementation claims from test, runtime, browser and production evidence. Use after implementation or whenever an agent claims something works.
---

# ppmax-runtime-verification

## Purpose

Prevent “implemented” from being treated as “verified”.

## Trigger

Use after code changes, before task completion, before launch, or when a runtime issue needs evidence.

**Do not use when:** Do not claim commands, tests, browser flows or production checks were executed unless they actually were.

## Inputs

### Required

- Claim or behavior to verify.
- Available code/runtime context.

### Optional

- Commands.
- URLs.
- Test suite.
- Logs.
- Screenshots.
- Acceptance criteria.

## Workflow

1. Convert the claim into observable acceptance criteria.
2. Classify current evidence as implemented, statically verified, tested, runtime verified, browser verified or production verified.
3. Run or request the strongest feasible verification step.
4. Capture command/result, observable behavior or failure evidence.
5. Test critical negative/error paths when relevant.
6. List what remains unverified.
7. Return gate status without upgrading evidence levels.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Claim
- Acceptance criteria
- Evidence level
- Checks performed
- Observed results
- Failures
- Unverified items
- Gate
- Decision/next action

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS only when required acceptance criteria are observed at the required verification level. WARN when lower-risk criteria remain unverified. FAIL when a required check fails or cannot be performed and missing evidence is blocking.

## Stop conditions

- The environment is unavailable for a required runtime claim; do not simulate success.
- A check could be destructive or unsafe without approval.
- Production verification would expose secrets or sensitive data.

## Anti-patterns

- Saying “should work”.
- Claiming tests pass without execution.
- Treating source inspection as browser/runtime verification.

## Example

Static inspection can prove a route exists; a request/browser check is needed to prove it actually responds as expected.
