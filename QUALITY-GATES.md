# Quality Gates

Quality gates prevent workflows from treating generated artifacts as validated progress.

## PASS

Evidence is sufficient for the workflow to continue without a known blocking condition.

## WARN

The workflow may continue, but material uncertainty or risk must remain visible.

## FAIL

A blocking condition exists or required evidence is missing. The default next action is research, revise, pivot, defer or stop.

## Gate design rules

A gate must define:

- what is being judged;
- required evidence;
- blocking conditions;
- warning conditions;
- what PASS permits;
- what FAIL prevents;
- valid next actions.

## Integrity rules

Do not:

- pass a gate because an artifact exists;
- pass runtime verification from static inspection alone;
- pass validation using invented customer evidence;
- silently downgrade blockers;
- convert uncertainty into arbitrary numeric scores.
