# Implementation Plan: Product Pro Max Design System

**Branch**: `main` (Spec Kit planning committed at `7e45f67`, no implementation) | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)  
**State**: Planned design, not implemented. HTML showcase is an approved aesthetic reference, not a validated renderer.

## Summary

Establish a repository-owned, replaceable Signal Protocol presentation system. Publish one canonical token contract, a small set of reusable visual treatments, a project-specific adapter to `diagram-design-vi`, and themed, GitHub-compatible brand assets. Preserve Spec 001/002 semantics and the modeling skill's authority; migrate existing visuals only after a verified pilot.

## Technical Context

- **Language/Version**: JSON, CSS/SVG/HTML; Python 3 standard library for deterministic token export/checking (version aligned with existing repo tooling, no new runtime service).
- **Primary Dependencies**: Existing `.agents/skills/diagram-design-vi/`, `speckit-system-modeling-vi`, Diagram Atlas and repo validation scripts; no frontend package.
- **Storage**: Git-tracked static files and generated standalone HTML/SVG; no database/network storage.
- **Testing**: Schema/role validation, deterministic output/negative fixtures, contrast and link audits, existing diagram Atlas/layout/self_check, Chromium browser screenshot/keyboard/mobile and GitHub README render review.
- **Target Platform**: GitHub Markdown/SVG and local/offline browser HTML; Windows/Linux authoring environments.
- **Project Type**: Documentation/design-token pipeline with static exports.
- **Performance Goals**: No runtime network dependency for generated HTML; no client-side framework or asset-loading chain.
- **Constraints**: Maintain source truth and vocabulary, available alternatives for reduced motion and low connectivity, WCAG AA, responsive legibility, reversible pilot, deterministic generation.
- **Scale/Scope**: README, diagrams/Atlas, documentation, brand assets; start with Spec 002 pilot, not mass migration.

## Constitution Check

- **Pre-design**: PASS at planning level. Single presentation source, no independent semantics ontology; evidence and QA reporting separated; added complexity proportional to repo size.
- **Post-design**: PASS at planning level. Modeling selects **WHAT** and source provenance; diagram-design selects **HOW** and consumes token values. Registry/Product Model untouched. All implementation and browser checks still PENDING.
- **Note**: An external brand style guide already exists inside `diagram-design-vi` (VibeToolPro). It must not be silently used as the Product Pro Max source of truth; do not overwrite personal global profiles.

## Project Structure

### Documentation (feature)

```text
specs/003-product-pro-max-design-system/
├── spec.md
├── checklists/{requirements.md,design-quality.md}
├── spec-diagram/presentation-boundary.html
├── diagrams.html
├── plan.md
├── research.md
├── data-model.md
├── contracts/tokens-and-surfaces.md
├── quickstart.md
├── tasks.md
└── analysis.md
```

### Planned implementation (not created by this plan)

```text
design-system/
├── tokens.json                 # sole token-value authority incl. role names/theme values/revision
├── README.md                   # authoring guide + role semantics, no duplicate token values
├── components.md               # node/connector/boundary/gate/evidence visual treatments
└── templates/                 # optional only after pilot demonstrates repeated need
assets/brand/
├── signal-path.svg
├── wordmark.svg
├── hero-light.svg
└── hero-dark.svg
scripts/
├── export_design_tokens.py     # deterministic standalone CSS/HTML variable export
└── verify_design_system.py    # schema, contrast, derivative drift, no-write check
.agents/skills/diagram-design-vi/  # project-scoped resolver/adapter instructions, no new skill
docs/diagrams/                   # derived Atlas/ledger presentation and navigation
specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html  # pilot
```

**Structure Decision**: No installed UI runtime, hosted asset service, new modeling skill or duplicated design-token authority. Keep generated outputs self-contained and source tokens centralized. Add additional files only on demonstrated repeated need.

**Plan modeling**: [Technical token-resolution diagram](plan-diagram/token-resolution.html); derived from this plan, not an additional authority. **Modeling gate `modeled` after local static and focused visual QA; actual implementation/browser publishing acceptance remains pending (see `modeling-acceptance.md`).**

## Phase 0 Research

[research.md](research.md) records repo observations and decisions: native HTML/SVG over framework; project-local token precedence; a generated/pre-rendered CSS variable layer; GitHub-friendly static `<picture>`/SVG; fallback fonts; deterministic snapshots vs live runtime token fetches.

## Phase 1 Design & Contracts

- [data-model.md](data-model.md): stable token identities, theme variants and derived presentation snapshots.
- [contracts/tokens-and-surfaces.md](contracts/tokens-and-surfaces.md): semantic role contract, resolution order, allowed mappings, negative cases, source/derived invariants, GitHub surface differences.
- [quickstart.md](quickstart.md): proposed commands/QA evidence; NOT instructions asserting implementation exists.

## Token Resolution / Flexibility Strategy

1. Resolve the repository-local `design-system/tokens.json` for this repository first; explicitly fail on missing/invalid required roles.
2. Identify requested surface and theme; use the approved default per surface (hero Dark, diagrams Light) unless deliberately overridden.
3. Resolve semantic role aliases and density into concrete presentation values. The Signal Lime brand-accent alias may change without changing `pass`, `warn`, `fail`, or a workflow decision label.
4. Render one canonical visual primitive grammar for each surface. Embed resolved CSS/SVG in standalone HTML, preserving a recorded token revision; no global network/theme fetch at view time.
5. Generate static GitHub-compatible SVG for README hero Light/Dark. README selects variant using supported Markdown/HTML; it never requires JavaScript.
6. Validate content snapshot and navigation independently from visual snapshot. Token updates invalidate **visual presentation freshness** only, never authoritative Spec Kit source semantics or runtime evidence.

**Boundary**: `speckit-system-modeling-vi` continues to resolve authoritative artifacts, diagram necessity, planned/implemented state and Atlas entries. `diagram-design-vi` resolves geometry/style under this repo's token adapter. Do not create a new modeling authority.

## Runtime Risk Design

| Risk ID | Status | Requirement refs | Evidence/trigger | Prevention design | Verification strategy |
| --- | --- | --- | --- | --- | --- |
| DS-R01 token drift | APPLIES | FR-001, FR-017, FR-021, FR-027 | Tokens change while generated CSS/assets remain stale | embed token revision + deterministic read-only check; explicit regenerate step | tamper/revision fixtures and byte-diff tests |
| DS-R02 fallback brand leak | APPLIES | FR-020, FR-023 | global `diagram-design` style overrides repo brand | project-first resolver; missing/invalid local token file is a visible error | isolated home profile + missing token fixtures |
| DS-R03 semantic corruption | APPLIES | FR-005, FR-008, FR-018 | gate result becomes decision; diagram arrow changed | side-by-side semantic snapshots and authoring boundary in contract | compare source/output labels, edges, source refs before/after |
| DS-R04 inaccessible variants | APPLIES | FR-013–FR-016 | contrast, zoom, focus, mobile clipping | role-level contrast checks plus browser keyboard/viewport gates | Light/Dark contrast matrix, 390px & 200% zoom checks |
| DS-R05 offline/GitHub failure | APPLIES | FR-009, FR-011, FR-013 | remote font/JS/CSS or blocked SVG feature | local fallback stacks; self-contained exports; static README SVG variants | offline open and GitHub rendering checks |
| DS-R06 incomplete migration | APPLIES | FR-010, FR-018, FR-019, FR-025 | broken Atlas link, lost metadata, partially swapped visual | copy-first pilot, full ledger/registry transaction, rollback on mismatch | Atlas/layout/self_check/browser; linked-source inventory diff |
| DS-R07 false verification claim | APPLIES | FR-022 | static source check reported as browser pass | evidence record with separate source/static/browser/manual fields | assertions for explicit unavailable/pending states |
| DS-R08 unsupported skin | APPLIES | FR-004, FR-006, FR-021 | missing theme roles or unsafe color value | strict role completeness and fail-closed validation | malformed token and contrast-negative fixtures |
| DS-R09 hosted runtime | NOT_APPLICABLE | FR-024 | static export-only architecture | no service/network/database boundary planned | source audit confirms no hosted runtime |

**Runtime companion**: `.agents/skills/runtime-verification/SKILL.md` was not found in prior repo audit. Above are feature-local DS risk IDs, not canonical catalog IDs. Review of current checkout required before implementation.

## Project Docs Promotion Plan

After implementation and verification, update `docs/ARCHITECTURE.md` with the presentation-only boundary, style Atlas, and README/brand surfaces. New `design-system/` documents must not represent shipped capability before implementation. Planned Spec 003 diagram may appear in Atlas explicitly as `planned` now. `model/product-model.json`, `registry/skills.json`, and established Spec 001/002 contracts remain unchanged.

## Roadmap / Integration Plan

Roadmap numbering and dependencies were reconciled on `main` in commit `7e45f67`: previous 003 `versioning-compatibility` becomes 004, old 004–007 become 005–008. `.specify/feature.json` now selects Spec 003. Recheck current HEAD before implementation; these planning artifacts do not imply the local modeling gates passed.

## Complexity Tracking

None. Every planned module addresses a specific confirmed surface or verification need; additional component families/themes are deferred.
