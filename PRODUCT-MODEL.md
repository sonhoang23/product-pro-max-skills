# Product Model

Product Pro Max uses one canonical model for shared product-lifecycle semantics.

**Machine authority:** `model/product-model.json`

The JSON model owns canonical IDs and relationships. This document explains how to read them. README pages, schemas, templates, workflows, examples, diagrams, and translations are derived views and must not redefine the model.

## Structural model

```text
PRODUCT LIFECYCLE
    ↓
CYCLES
    ↓
PHASES

TRACKS  ── cross-cutting disciplines
LOOPS   ── repeatable learning/operating motions
GATES   ── evidence/readiness judgments
DECISIONS ── next actions after interpreting evidence
```

The lifecycle is ordered, but it is not a mandatory waterfall. A project can skip phases that are not relevant, repeat loops, backtrack, defer, pivot, or stop when evidence justifies it.

## Cycles and phases

| Cycle | Canonical phases |
| --- | --- |
| Opportunity | `discovery`, `validation` |
| Product Strategy | `positioning`, `business-model` |
| Product Definition | `scope`, `requirements`, `experience-design`, `measurement-design` |
| Delivery | `technical-design`, `implementation-planning`, `build`, `integration` |
| Verification | `product-qa`, `runtime-verification`, `security-reliability`, `ux-validation` |
| Go-to-Market | `launch-preparation`, `distribution` |
| Growth | `acquisition`, `activation`, `engagement`, `monetization`, `retention`, `referral`, `expansion` |
| Operations | `product-operations`, `optimization`, `maintenance` |
| Learning & Evolution | `evidence-review`, `strategy-review`, `portfolio-decision` |
| End of Life | `deprecation`, `migration`, `sunset` |

Every phase belongs to exactly one cycle in Product Model v1.

## Tracks

Tracks are disciplines, not lifecycle states:

`product`, `engineering`, `ux`, `research`, `data`, `marketing`, `growth`, `sales`, `revenue`, `operations`, `security`, `support`.

Several tracks can progress during the same phase.

## Loops

Loops can cross cycle and phase boundaries. Canonical loops are:

- `evidence-loop`
- `discovery-loop`
- `delivery-loop`
- `experiment-loop`
- `growth-loop`
- `gtm-loop`
- `revenue-loop`
- `reliability-loop`
- `strategy-loop`

Their exact motions live in `model/product-model.json`.

## Gates are not decisions

A **gate** answers: *How strong is the evidence or readiness?*

Canonical gate results:

- `pass` — sufficient evidence/readiness, no known blocker;
- `warn` — work may continue but material uncertainty remains visible;
- `fail` — a blocker exists or required evidence is missing.

A **decision** answers: *What should happen next?*

Canonical decisions:

`continue`, `research`, `revise`, `pivot`, `repeat`, `backtrack`, `defer`, `stop`, `escalate`.

A gate result does not imply exactly one decision. Context determines the valid next action.

## Project status

Durable project status is separate again:

`active`, `blocked`, `deferred`, `stopped`, `completed`.

For example, a workflow may return `warn` and decide to `research` while the project remains `active`.

## Identifier rules

Canonical machine IDs:

- use English;
- use lowercase ASCII;
- use kebab-case for multiple words;
- remain untranslated in localized documentation and UI when they are contract values.

Human labels may be localized.

## Nested lifecycles

Features, experiments, campaigns, pricing changes, and other product bets may run smaller lifecycles inside the main product lifecycle. Nested lifecycles reuse the same principles but do not create new top-level canonical phase IDs unless the Product Model itself is amended.

## Change rule

When shared lifecycle semantics change:

1. change `model/product-model.json`;
2. align dependent schemas/templates;
3. run repository validation;
4. only then update derived documentation.

Do not add a canonical lifecycle term only to README, a diagram, an example, or a dependent schema.
