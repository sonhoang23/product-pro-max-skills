# Quality Gates

Quality gates prevent workflows from treating generated artifacts as validated progress.

Canonical gate IDs are defined by `model/product-model.json`.

## PASS

Evidence is sufficient for the workflow to continue without a known blocking condition.

## WARN

The workflow may continue, but material uncertainty or risk must remain visible.

## FAIL

A blocking condition exists or required evidence is missing. The default next action may be research, revise, pivot, defer, stop, or another context-appropriate canonical decision.

## Gate result is not the decision

A gate answers:

**How strong is the evidence or readiness?**

A decision answers:

**What should happen next?**

The same gate result can lead to different decisions in different workflows. Do not add next-action concepts such as `pivot`, `repeat`, or `escalate` to the gate enum.

See `PRODUCT-MODEL.md` for canonical gate and decision vocabularies.

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
