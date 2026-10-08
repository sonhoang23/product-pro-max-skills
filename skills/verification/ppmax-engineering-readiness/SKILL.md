---
name: ppmax-engineering-readiness
description: Audit implementation readiness across security, testing, observability, data safety, migration, rollback and operational risk. Use before declaring a build production-ready.
---

# ppmax-engineering-readiness

## Purpose

Expose engineering risks that feature-complete code can hide.

## Trigger

Use during late implementation, before launch readiness, or when inheriting AI-generated code.

**Do not use when:** Do not mark checks complete from plans alone when runtime or test evidence is required.

## Inputs

### Required

- Implemented system or implementation plan.
- Deployment context.

### Optional

- Test results.
- Threat model.
- Runbooks.
- Migration plan.
- Observability setup.

## Workflow

1. Identify critical data, trust boundaries and failure modes.
2. Review authentication, authorization, secret handling and dependency risk at the level supported by evidence.
3. Check tests against critical behaviors rather than raw percentage.
4. Check logs, metrics, error capture and operational visibility.
5. Check migration, backup, rollback and destructive data paths.
6. Label each item planned, implemented, tested or runtime verified.
7. Produce blocking and non-blocking risks.

## Evidence rules

- Never invent customer, market, test, runtime or revenue evidence.
- Label material claims as provided, observed, researched, measured, inferred or assumed.
- Preserve contradictory evidence.
- If evidence is unavailable, mark it unknown and lower the gate instead of filling the gap with confidence.
- Keep machine-facing semantics stable; present user-facing prose in the user's requested language.

## Output contract

Return these semantic fields:

- Readiness matrix
- Security risks
- Testing gaps
- Observability gaps
- Data/migration risks
- Rollback status
- Evidence state
- Blockers
- Gate

Rendering may be Markdown, YAML or JSON if requested, but facts, assumptions, risks, gate and decision must remain distinguishable.

## Quality gate

PASS requires no known launch-blocking engineering risk and evidence for critical controls. WARN allows explicit non-critical gaps. FAIL when critical security, data-loss, migration or rollback risks are unaddressed.

## Stop conditions

- Required system evidence is unavailable; report unknown rather than guessing.
- A critical security vulnerability is found; route to remediation before launch.

## Anti-patterns

- Equating lint/typecheck with runtime correctness.
- Using coverage percentage as the only signal.
- Calling backup complete without restore considerations.

## Example

A feature-complete app can FAIL because authorization is unverified or a destructive migration has no rollback path.
