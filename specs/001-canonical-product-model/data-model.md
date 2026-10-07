# Data Model: Canonical Product Model

## ProductModel
Contains `model_version`, cycles, tracks, loops, gates, decisions, and project statuses.

## Cycle
Fields: `id`, `label`, `purpose`, ordered `phases`.

## Phase
Fields: `id`, `label`, `purpose`.
Invariant: every phase belongs to exactly one cycle and phase IDs are globally unique.

## Track
Fields: `id`, `label`. Tracks do not imply lifecycle order.

## Loop
Fields: `id`, `label`, `motion`. Loops may cross cycles and phases.

## Gate
Fields: `id`, `label`, `meaning`.
Canonical IDs: `pass`, `warn`, `fail`.

## Decision
Fields: `id`, `label`, `meaning`. Decisions are not project statuses.

## ProjectStatus
Fields: `id`, `label`, `meaning`.
Canonical v1 intent: active, blocked, deferred, stopped, completed.
