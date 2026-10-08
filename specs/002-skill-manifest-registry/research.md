# Research — Skill Manifest Registry

## Decisions

### R1 — Canonical authority and serialization
**Decision:** Every distributable skill owns a sibling `manifest.yaml`; `SKILL.md` owns behavior, while `model/product-model.json` owns lifecycle/gate/decision vocabulary. Generate a deterministic JSON registry at `registry/skills.json` from manifests.
**Rationale:** Human-editable metadata with a machine-consumable, drift-checkable discovery artifact (FR-003–004, FR-023–025).
**Alternatives:** Hand-maintained registry (drift); registry-as-source (contradicts FR-024); frontmatter-only metadata (blurs behavior and canonical metadata).

### R2 — Validation and generator
**Decision:** Use Python 3 standard library for structural/cross-reference validation plus an explicit YAML parser dependency declared and pinned in repository tooling at implementation time. Separate `generate` (write deterministic derived registry) from `check` (read-only compare expected bytes, strict fail).
**Rationale:** Existing verification scripts use Python; deterministic CI-friendly pipeline; parser choice must not silently accept duplicate YAML keys or unsafe tags.
**Alternatives:** Regex YAML parsing (unsafe); runtime-only discovery (no aggregate registry); mutable registry in validator (masks drift).
**Implementation prerequisite:** Confirm available dependency manager / CI installation strategy before writing tooling. Do not claim runnable commands until implemented.

### R3 — Lifecycle modeling
**Decision:** `primary_cycle` is one valid Product Model cycle. `lifecycle` is a list of explicit objects: `cycle` plus optional `phase`, with separate `tracks` list. Validate cycle ownership for every phase; deduplicate semantic links.
**Rationale:** Supports many-to-many assignment without multiplying physical folders (FR-008–012).
**Alternative:** Nested phase directory trees (misrepresents cross-cutting membership).

### R4 — Identity and migration
**Decision:** Normalize `namespace: product-pro-max`, `slug`, `id: ppmax-<slug>`, folder, and `SKILL.md` frontmatter name. Inventory each pre-existing `skills/*/SKILL.md` first; create migration mapping and check behavioral parity before removal of old paths.
**Rationale:** Prevent accidental renames, collisions, broken links and behavioral drift (FR-005–007, FR-030–031).
**Alternative:** Rename on discovery without review (risks broken references).

### R5 — Relationships and workflow authority
**Decision:** Controlled relation types `prerequisite`, `complements`, `produces-input-for` with directed semantics for prerequisite/produces-input-for and nondirectional semantics for complements; prohibit self-reference unless future authoritative contract permits. Workflow relationships use an existing repo workflow ID/path and a membership descriptor only; never duplicate ordering/execution logic.
**Rationale:** Strict semantics, reference integrity, no hidden orchestration (FR-018–022).
**Alternative:** Free-text relation types (non-machine-readable). Validate actual workflow inventory before choosing definitive workflow identifiers; unknown references fail closed.

### R6 — Registry contract and scope
**Decision:** Include all fields required by FR-025, stable ordering by skill ID and normalized arrays. Exclude `.agents/**`. Empty registry is allowed only when no distributable skills exist; missing manifests are errors.
**Rationale:** Single authority and full coverage (FR-023–027).
**Alternative:** Partial catalog (violates completeness).

### R7 — Deferred policy
**Decision:** Do not introduce compatibility/deprecation versions, scoring/evals, release states, catalog UI, or ranking semantics.
**Rationale:** Owned by Specs 003–007 (FR-032).

## Phase 1 Toolchain Discovery (2026-10-08)

- Existing CI `.github/workflows/validate.yml` uses `actions/setup-python@v5` with Python **3.12**, then standard-library `scripts/validate_repo.py` and installer dry-run. No current registry parser or `requirements-registry.txt` existed before Phase 1.
- Selected `PyYAML==6.0.2` in root `requirements-registry.txt`; the future parser MUST subclass `yaml.SafeLoader` to reject duplicate mapping keys, prohibit unsafe YAML constructors/tags, and report file/line diagnostics. `yaml.safe_load` alone does not reject duplicates.
- T038 will introduce `.github/workflows/skill-registry.yml` with Python 3.12, `python -m pip install -r requirements-registry.txt`, registry check and negative-fixture tests. The existing workflow is unchanged in Phase 1.
- `specs/002-skill-manifest-registry/migration-inventory.md` records 13 flat skills and 3 workflow definitions with proposed mappings, source blob fingerprints and baseline trigger/exclusion summaries. Actual migration/semantic-parity verification remains pending.
- This is a source/configuration review, not proof that dependency installation or tests have run.

## Open implementation probes (not upstream ambiguity)
- Confirm existing skills inventory and workflow definitions before implementing migration/reference validation.
- Confirm Python YAML dependency availability and CI environment before selecting an exact package pin.
- Runtime-verification companion `.agents/skills/runtime-verification/SKILL.md` was not present at planning time; runtime design risks are explicitly captured in `plan.md` without claiming canonical Risk IDs.
