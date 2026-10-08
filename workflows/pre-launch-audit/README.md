# pre-launch-audit

Audit whether an implemented MVP is coherent, operationally ready and runtime verified for its intended launch scope.

## Steps

1. `ppmax-ux-flow` — audit-flow
2. `ppmax-architecture-plan` — review-architecture
3. `ppmax-engineering-readiness` — check-engineering
4. `ppmax-runtime-verification` — verify-runtime
5. `ppmax-launch-readiness` — launch-gate

## Gate behavior

- PASS: continue to the configured next step.
- WARN: continue only while carrying unresolved evidence and risk forward.
- FAIL: stop automatic progression and resolve, research, revise, pivot, defer or stop.

A workflow never upgrades a skill's evidence level.
