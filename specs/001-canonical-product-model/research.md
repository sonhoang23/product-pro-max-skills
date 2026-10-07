# Research: Canonical Product Model

## Decisions

1. **One machine-readable identifier authority** — use canonical JSON so dependency-free validation and AI agents can consume it directly.
2. **Lifecycle hierarchy is cycle → ordered phases** — tracks and loops remain separate cross-cutting collections.
3. **Gate, decision, and project status are separate vocabularies** — they answer readiness, next action, and durable state respectively.
4. **Normalize project state before compatibility policy** — replace ambiguous legacy `stage` semantics with explicit `cycle` and `phase`; Spec 003 will define future migration guarantees.
5. **Protect the model immediately** — extend the existing validator with semantic drift checks instead of waiting for broader Spec 004 eval work.
6. **No diagram required** — complete ontology inventory is clearer and more searchable as structured data and compact tables than as a dense visual.
