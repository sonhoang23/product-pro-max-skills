# Product Pro Max Design System

**Status:** Phase 1 documentation and design-reference registration only (Spec 003).
No token contract, exporter, renderer integration or production brand asset has been implemented.

## Approved concept (reference only)

- **Concept:** Signal Protocol — a one-file HTML visual showcase for theme, accent, density and diagram treatments.
- **Canonical preserved source:** [approved-showcase.html](../specs/003-product-pro-max-design-system/references/approved-showcase.html).
- **Source identity:** Git blob `c556747321f1f31bd6927b8af264a000f32638a3`, present at base commit `d78320a3bcce531db43a6e47ce16ab284ada64b0` on `main`.
- **Reference revision:** `concept-v1` (documentation label bound to the blob above, **not** a released `tokens.json` version).
- **Use:** Review the appearance and interaction direction only. Its sample labels, mock workflow outcomes and CSS declarations are not canonical requirements, role IDs, gate results or decisions. This file is not a schema, token authority or implementation test.

## Source-of-truth hierarchy

1. [Constitution](../.specify/memory/constitution.md) and [Spec 003 requirements](../specs/003-product-pro-max-design-system/spec.md) govern constraints and intended behavior.
2. [Implementation plan](../specs/003-product-pro-max-design-system/plan.md), [data model](../specs/003-product-pro-max-design-system/data-model.md) and [tokens/surfaces contract](../specs/003-product-pro-max-design-system/contracts/tokens-and-surfaces.md) govern planned design and validation.
3. `design-system/tokens.json` will be the **only canonical machine-readable presentation-token value source** after Phase 2 creates it. This README and the approved showcase must not independently define or override token values.
4. Product Model/Skill Registry and Spec Kit artifacts continue to own product semantics. `speckit-system-modeling-vi` decides what a diagram represents; `diagram-design-vi` decides how the derived presentation looks.

## Constraints before implementation

- Local repository tokens must take precedence; never silently fall back to a user-global `~/.diagram-design` profile or VibeToolPro style.
- Keep `Gate result` and `Decision` separate; visuals must not invent or alter edges, nodes, statuses, source references, Atlas metadata or planned/implemented truth.
- No new frontend framework, service, DB, network asset dependency, duplicate model or bulk diagram migration.
- Source/static validator results, actual browser verification and GitHub asset rendering require **separate evidence**. Source review is not runtime PASS.

**Next work (not executed):** Phase 2 starts at T004 with `design-system/tokens.json`. See [tasks.md](../specs/003-product-pro-max-design-system/tasks.md).
