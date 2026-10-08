# Foundation Roadmap

This backlog decomposes repository-foundation work into dependency-aware Spec Kit features. Only one feature should be active at a time unless the dependency graph explicitly permits parallel work.

**Roadmap numbering reconciliation (2026-10-08)**: The user selected **Spec 003 — Product Pro Max Design System**. The old `003-versioning-compatibility` is preserved as **004** and the old backlog sequence 004–007 moves to **005–008**. IDs of Spec 001/002, canonical Product Model IDs and skill IDs are unchanged. Re-check `main` before merging.

| Spec | Feature | Goal | Dependency | Status |
| --- | --- | --- | --- | --- |
| 001 | `canonical-product-model` | Canonical ontology for lifecycle, cycles, phases, tracks, loops, gates, decisions and status | None | Complete |
| 002 | `skill-manifest-registry` | Canonical skill metadata, registry, discovery and authoring boundary | 001 | Complete (user-approved local acceptance) |
| 003 | `product-pro-max-design-system` | Signal Protocol tokens, theme-flexible diagrams, README hero, docs and brand assets without changing source semantics | 001, 002 | Spec / plan / tasks drafted; implementation not started |
| 004 | `versioning-compatibility` | Versioning, compatibility, breaking-change, migration and deprecation rules | 001 | Backlog (renumbered from 003) |
| 005 | `quality-validation-evals` | Schema, semantic, workflow and standardized skill evaluation gates | 002, 004 | Backlog (was 004) |
| 006 | `repository-governance` | Proposal, review, ownership, change-governance and product/tooling boundaries | 002, 004 | Backlog (was 005) |
| 007 | `global-discovery-docs` | Global-first docs/catalog/navigation and agent discovery | 002, 003, 004 | Backlog (was 006; design-system dependency added) |
| 008 | `release-lifecycle` | Tags, releases, changelog, depreciation/migration/removal flow | 004, 005 | Backlog (was 007) |

## Dependency Graph

```text
001 Canonical Product Model (complete)
  ├── 002 Skill Manifest Registry (complete)
  │     └── 003 Design System (design stage)
  │            └── 007 Global Discovery & Docs (also requires 004)
  └── 004 Versioning & Compatibility (backlog)
        ├── 005 Quality Validation & Evals (also requires 002)
        ├── 006 Repository Governance (also requires 002)
        ├── 007 Global Discovery & Docs (also requires 002, 003)
        └── 008 Release Lifecycle (also requires 005)
```

## Execution Rule

Do not mark any planned feature complete until its required upstream foundation is implemented, verified and converged. Specification, planning, modeling, code implementation and runtime/visual verification are independent states. Only promote implemented project documentation when checks justify it.

**Current planned feature**: Spec 003 — Product Pro Max Design System. Its specification/planning artifacts can be authored from verified upstream contracts; implementation still requires its own test and QA evidence.
