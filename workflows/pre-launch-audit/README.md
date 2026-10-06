# pre-launch-audit

Audit whether an implemented MVP is coherent, operationally ready and runtime verified for its intended launch scope.

## Steps

1. `ux-flow` — audit-flow
2. `architecture-plan` — review-architecture
3. `engineering-readiness` — check-engineering
4. `runtime-verification` — verify-runtime
5. `launch-readiness` — launch-gate

## Gate behavior

- PASS: continue to the configured next step.
- WARN: continue only while carrying unresolved evidence and risk forward.
- FAIL: stop automatic progression and resolve, research, revise, pivot, defer or stop.

A workflow never upgrades a skill's evidence level.
