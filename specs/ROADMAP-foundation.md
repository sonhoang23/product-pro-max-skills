# Foundation Roadmap

This backlog decomposes repository-foundation work into dependency-aware Spec Kit features. Only one feature should be active at a time unless the dependency graph explicitly permits parallel work.

| Spec | Feature | Goal | Dependency | Status |
| --- | --- | --- | --- | --- |
| 001 | `canonical-product-model` | Establish one canonical ontology for lifecycle, cycles, phases, tracks, loops, gates, decisions, and project status | None | Active |
| 002 | `skill-manifest-registry` | Define skill metadata and a machine-readable registry for human and agent discovery | 001 | Backlog |
| 003 | `versioning-compatibility` | Define versioning, compatibility, breaking-change, migration, and deprecation rules | 001 | Backlog |
| 004 | `quality-validation-evals` | Expand validation into schema, semantic, workflow, and standardized skill evaluation gates | 002, 003 | Backlog |
| 005 | `repository-governance` | Clarify product/tooling boundaries and proposal, review, ownership, and change-governance workflows | 002, 003 | Backlog |
| 006 | `global-discovery-docs` | Build global-first docs architecture, catalog/navigation, terminology, examples, and agent-readable discovery | 002, 003 | Backlog |
| 007 | `release-lifecycle` | Define operational release, changelog, tag, deprecation, migration, and removal flow | 003, 004 | Backlog |

## Dependency Graph

```text
001 Canonical Product Model
        |
        +--> 002 Skill Manifest & Registry
        |        |
        |        +--> 004 Quality Validation & Evals
        |
        +--> 003 Versioning & Compatibility
                 |
                 +--> 007 Release Lifecycle

002 + 003
   |
   +--> 005 Repository Governance
   |
   +--> 006 Global Discovery & Docs
```

## Execution Rule

Do not create the next numbered spec until its required upstream foundation is implemented, verified, and converged. Backlog entries are not authoritative feature requirements until their own `spec.md` exists.
