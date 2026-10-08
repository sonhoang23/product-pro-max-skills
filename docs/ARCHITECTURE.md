# Architecture

## Authority model

Product Pro Max separates authoritative contracts from derived views.

```text
Product Model IDs + relationships
        │
        ├── machine authority: model/product-model.json
        └── human semantics:  PRODUCT-MODEL.md
                 ↓
        schemas / templates / workflows
                 ↓
        README / examples / diagrams / translations
```

Derived views must not silently redefine canonical shared semantics.

## Canonical product structure

The lifecycle hierarchy is:

```text
Product lifecycle
  └── Cycle
       └── Phase
```

Cross-cutting concepts are intentionally outside that hierarchy:

- **Track** — a discipline that can operate across multiple phases.
- **Loop** — a repeatable learning or operating motion that can cross phases/cycles.
- **Gate** — an evidence/readiness judgment.
- **Decision** — a next action selected after interpreting evidence and gate results.
- **Project status** — durable execution state.

Canonical identifiers and relationships live in `model/product-model.json`.

## Canonical operating primitives

Product work uses five core primitives:

```text
Skill → Artifact → Evidence → Gate → Decision
```

### Skill
A narrow agent capability with an explicit trigger, workflow, and output contract.

### Artifact
A durable output such as a validation brief, scope decision, architecture decision, or runtime report.

### Evidence
Traceable support for a claim, including provenance and evidence class.

### Gate
A readiness/evidence judgment. Canonical results are `pass`, `warn`, and `fail`.

### Decision
A next action such as `continue`, `research`, `revise`, `pivot`, `repeat`, `backtrack`, `defer`, `stop`, or `escalate`.

Gate results and decisions are different concepts and must not share one enum.

## Workflows

A workflow composes existing skills. Workflow files should orchestrate; they should not duplicate skill logic.

A workflow can map the same gate result to different next steps depending on context. The Product Model defines canonical gate/decision vocabulary; each workflow defines its route.

## Project state

Chat sessions are replaceable. Product state is not.

The recommended `.product-pro-max/` directory persists assumptions, evidence, decisions, artifacts, lifecycle state, and a product passport.

Canonical lifecycle state uses:

- `cycle`
- `phase`
- `status`

The project-state schema rejects a phase paired with a cycle that does not own it.

## Repository boundaries

- `skills/`: canonical distributable Product Pro Max skills.
- `workflows/`: compositions of canonical skills.
- `model/`: canonical shared product semantics.
- `schemas/`: machine-readable dependent contracts.
- `templates/`: durable state templates.
- `.agents/`: repository-development skills/tooling, not distributable product content by default.
- `.specify/` and `specs/`: Spec Kit development workflow and feature authority.

## Agent compatibility

Canonical distributable skills live at `skills/<primary-cycle>/ppmax-<slug>/SKILL.md`, beside `manifest.yaml`. `scripts/install.py` discovers these nested canonical directories and copies them into a target Agent Skills directory named by canonical ID.

Platform-specific adapters should transform installation layout rather than duplicate canonical skill logic.

## Registry discovery boundary

`manifest.yaml` is the authoritative per-skill discovery metadata; `registry/skills.json` is its deterministic derived projection. The manifest can declare multiple lifecycle associations while directory placement has exactly one primary cycle. `SKILL.md` owns execution behavior, not the registry. `workflows/*/workflow.yaml` owns orchestration, whereas manifest workflow links expose discovery relationships. `.agents/` tooling is excluded from distributable discovery. The registry checker rejects missing or invalid manifests, identifiers and references, and byte-level drift without writing files.

## Global-first rule

Canonical logic and machine identifiers are English and ASCII-safe. User-facing labels may be localized, but localization cannot change machine-facing values or create a second semantic authority.

## MVP exclusions

The MVP intentionally excludes hosted dashboards, marketplaces, autonomous long-running orchestration, framework-specific engineering packs, and proprietary skill formats.
