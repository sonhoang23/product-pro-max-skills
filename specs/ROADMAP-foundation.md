# Foundation Roadmap

This backlog decomposes repository-foundation work into dependency-aware Spec Kit features. Only one feature should be active at a time unless the dependency graph explicitly permits parallel work.

**Roadmap numbering reconciliation (2026-10-08)**: The user selected **Spec 003 — Product Pro Max Design System**. The old `003-versioning-compatibility` is preserved as **004** and the old backlog sequence 004–007 moves to **005–008**. IDs of Spec 001/002, canonical Product Model IDs and skill IDs are unchanged. Re-check `main` before merging.

| Spec | Feature | Goal | Dependency | Status |
| --- | --- | --- | --- | --- |
| 001 | `canonical-product-model` | Canonical ontology for lifecycle, cycles, phases, tracks, loops, gates, decisions and status | None | Complete |
| 002 | `skill-manifest-registry` | Canonical skill metadata, registry, discovery and authoring boundary | 001 | Complete (user-approved local acceptance) |
| 003 | `product-pro-max-design-system` | Signal Protocol tokens, theme-flexible diagrams, README hero, docs and brand assets without changing source semantics | 001, 002 | Phases 1–7 implemented, 55/55 tasks complete, native Chromium keyboard 200% zoom verified; final convergence gate checked |
| 004 | `versioning-compatibility` | Versioning, compatibility, breaking-change, migration and deprecation rules | 001 | **Spec clarified (no blocking questions), modeling diagram drafted 2026-10-10; diagram QA and modeling gate pending; plan/implementation not started** |
| 005 | `quality-validation-evals` | Schema, semantic, workflow and standardized skill evaluation gates | 002, 004 | Backlog (was 004) |
| 006 | `repository-governance` | Proposal, review, ownership, change-governance and product/tooling boundaries | 002, 004 | Backlog (was 005) |
| 007 | `global-discovery-docs` | Global-first docs/catalog/navigation and agent discovery | 002, 003, 004 | Backlog (was 006; design-system dependency added) |
| 008 | `release-lifecycle` | Tags, releases, changelog, depreciation/migration/removal flow | 004, 005 | Backlog (was 007) |
| 009 | `shared-product-context` | Progressive shared context for research-first/idea-first work; workspace/opportunity/product scope, evidence/decision integrity and cross-skill handoff | 001, 002 | **Spec drafted 2026-10-09; implementation deferred; modeling/plan/tasks not started** |

## Dependency Graph

```text
001 Canonical Product Model (complete)
  ├── 002 Skill Manifest Registry (complete)
  │     └── 003 Design System (implemented; 55/55 complete; converged static repo scope)
  │            └── 007 Global Discovery & Docs (also requires 004)
  └── 004 Versioning & Compatibility (backlog)
        ├── 005 Quality Validation & Evals (also requires 002)
        ├── 006 Repository Governance (also requires 002)
        ├── 007 Global Discovery & Docs (also requires 002, 003)
        └── 008 Release Lifecycle (also requires 005)

001 + 002 (complete)
  └── 009 Shared Product Context (specification drafted; implementation deferred)
        ├── Compatible with existing project-state and evidence contracts
        └── Later skills consume the context protocol only after implementation
```

## Execution Rule

Do not mark any planned feature complete until its required upstream foundation is implemented, verified and converged. Specification, planning, modeling, code implementation and runtime/visual verification are independent states. Only promote implemented project documentation when checks justify it.

**Current specification focus**: Spec 004 — Versioning & Compatibility (requirements recorded; implementation not started). Spec 009 remains drafted with implementation explicitly deferred. Spec 003 convergence remains as previously accepted from documented source checks, official full-checkout CI, native Chromium UI zoom, GitHub reader previews and reversible Spec 002 migration; no production publishing or screen-reader certification claimed.
