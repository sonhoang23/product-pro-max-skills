# idea-to-first-users

> **INACTIVE / HISTORICAL DESIGN REFERENCE.** The named skills were withdrawn from the distributable catalog. No executable `workflow.yaml` exists. This sequence is a conceptual starting point only; do not run it until its skills and workflow are redesigned and validated.

Compose definition, build readiness, verification, launch, distribution and pricing toward first users.

## Steps

1. `ppmax-mvp-scope` — scope-mvp
2. `ppmax-ux-flow` — design-flow
3. `ppmax-architecture-plan` — plan-architecture
4. `ppmax-engineering-readiness` — check-engineering
5. `ppmax-runtime-verification` — verify-runtime
6. `ppmax-launch-readiness` — launch-gate
7. `ppmax-distribution-plan` — plan-distribution
8. `ppmax-pricing-experiment` — test-pricing

## Gate behavior

- PASS: continue to the configured next step.
- WARN: continue only while carrying unresolved evidence and risk forward.
- FAIL: stop automatic progression and resolve, research, revise, pivot, defer or stop.

A workflow never upgrades a skill's evidence level.
