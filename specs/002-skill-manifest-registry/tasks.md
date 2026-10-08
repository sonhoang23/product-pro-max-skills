# Tasks: Skill Manifest Registry

**Input**: `specs/002-skill-manifest-registry/{spec.md,plan.md,research.md,data-model.md,contracts/manifest-and-registry.md,quickstart.md}`
**State**: Phase 1–2 source artifacts and Phase 3 generator T009–T011 committed. Windows logs confirmed T016 2/2 PASS; Windows Python 3.13.3 regression rerun 15/15 PASS at b89abe8; T022 verified for malformed YAML preservation and read-only drift detection. T012 and T021 remain open because their full fixture/snapshot matrices are not yet covered; T013 depends on later migration; T020 still needs complete Product Model gate/decision semantic verification. Runtime/CI verification is not yet evidenced. Plan gate `no-diagram-needed` with recorded source hashes; no implementation or runtime PASS claimed.
**Scope**: Canonical skills only (`skills/`); repository tooling `.agents/` is excluded. Product Model in `model/product-model.json` remains authoritative.

## Runtime Risk Coverage

| Risk | Status | Requirements | Prevention | Tasks | Required evidence |
|---|---|---|---|---|---|
| SR-01 drift | APPLIES | FR-023–026 | Byte-exact read-only check | T011, T012, T022 | Tamper fixture fails, original file unchanged |
| SR-02 identity | APPLIES | FR-005–009 | Full-tree identity inventory, duplicate rejection | T017, T021, T023 | All invalid identity/path fixtures fail |
| SR-03 references | APPLIES | FR-012, FR-017–022 | Model/skill/workflow cross-reference | T018–T021 | Broken references fail with source path |
| SR-04 partial write | APPLIES | FR-024–026 | Prevalidation then atomic replacement | T006, T010, T012, T021, T022 | Corrupt YAML fixture never alters registry |
| SR-05 migration drift | APPLIES | FR-030–031 | Reviewed mapping and parity audit | T023–T028 | 13 skill parity records, repaired links |
| SR-06 tooling leakage | APPLIES | FR-023, FR-028–029 | Strict `skills/` scope | T007, T033, T036 | `.agents/` exclusion fixtures |
| SR-07 network runtime | NOT_APPLICABLE | N/A | File-only interfaces; no network runtime in planned feature | No task; static scope review in T040 | Confirm no new network boundary |

Risk IDs are feature-local design references from `plan.md`, **not** canonical runtime-verification IDs; `.agents/skills/runtime-verification/` is absent. No `NEEDS_UPSTREAM` identified at task planning. CI/test obligations remain unchecked until executed.

## Phase 1: Setup

- [x] T001 Inventory 13 existing `skills/*/SKILL.md` and 3 `workflows/*/workflow.yaml`, record baseline paths, names, triggers, evidence/output semantics, internal links and migration fingerprints in `specs/002-skill-manifest-registry/migration-inventory.md`.
- [x] T002 Inspect existing Python/CI tooling, select supported Python version, and pin a safe YAML parser with duplicate-key rejection in `requirements-registry.txt`; record the CI installation approach in `specs/002-skill-manifest-registry/research.md` without creating the workflow until T038.
- [x] T003 Document exact generator/checker entrypoints and their non-mutating vs atomic-write modes in `specs/002-skill-manifest-registry/quickstart.md`.

## Phase 2: Foundational

- [x] T004 Define only foundational canonical entities, relation types (`prerequisite`, `complements`, `produces-input-for`), workflow authority and manifest-vs-SKILL.md responsibility in `SKILL-MODEL.md`, preserving `model/product-model.json` as lifecycle/gate/decision authority.
- [x] T005 Specify required sibling `manifest.yaml` contract, field types, ASCII identity, uniqueness, `primary_cycle` membership, phase ownership, optional gate/decision `semantic_kind`, error policy and exact path rules in `SKILL-CONTRACT.md`.
- [x] T006 Create shared safe YAML decoding, duplicate-key/unsafe-tag rejection, normalized UTF-8/JSON output and actionable error structures in `scripts/skill_registry_common.py`; validate all input before any output mutation.
- [x] T007 Implement repository inventory for distributable `skills/<cycle>/<id>/SKILL.md` + `manifest.yaml`, explicitly excluding `.agents/`, in `scripts/skill_registry_common.py`; reject legacy/unpaired paths rather than silently ignoring them.
- [x] T008 Implement Product Model cycle/phase ownership, track, gate/decision vocabulary loaders and workflow ID discovery from `workflows/*/workflow.yaml` in `scripts/skill_registry_common.py`; unknown and ambiguous workflow IDs must fail closed.

## Phase 3: US1 — Discover the Right Skill (P1, MVP)

**Independent test**: From `registry/skills.json` alone, locate candidate skills by lifecycle, trigger, inputs/outputs and relation; generator produces identical bytes on repeat and detects hand edits read-only.

- [x] T009 [US1] Implement canonical manifest-to-registry projection of every FR-025 discovery field, canonical path and deterministic sorting in `scripts/generate_skill_registry.py`, with `registry_version: 1` only as encoding marker.
- [x] T010 [US1] Implement `generate` mode of `scripts/generate_skill_registry.py`: prevalidate full catalog, serialize stable UTF-8 JSON and atomically replace `registry/skills.json` only on complete success (SR-04).
- [x] T011 [US1] Implement read-only `check` mode in `scripts/generate_skill_registry.py`: regenerate in memory, compare byte-for-byte with `registry/skills.json`, identify drift or incomplete coverage and never write (SR-01).
- [ ] T012 [US1] Add clean-registry, two-run byte-identical and tampered-registry fixtures plus read-only filesystem snapshot assertions in `tests/test_skill_registry.py`; capture invocation/exit/output evidence (SR-01, SR-04).
- [ ] T013 [US1] After T023–T029 (US4 migration and verification) and T017–T022 (US3 integrity), produce `registry/skills.json` from fully migrated valid manifests in `registry/skills.json`, with one entry per distributable skill and zero `.agents/` entries; block until migration tasks complete.

## Phase 4: US2 — Understand Contracts and Relationships (P1)

**Independent test**: Two different manifest fixtures expose the same contract and typed relationships without parsing behavioral prose.

- [x] T014 [US2] Extend the foundational model (T004) with precise, nonduplicative trigger include/exclude, semantic input `{name, description, required: boolean}`, output `{name, description, semantic_kind?}`, typed skill/workflow relationship interpretation in `SKILL-MODEL.md` without defining execution logic.
- [x] T015 [US2] Implement manifest field/schema checks for required nonempty English description, positive/negative trigger arrays, unique semantic input/output names, booleans, canonical relationship types and workflow roles in `scripts/skill_registry_common.py`.
- [x] T016 [US2] Add two contrasting manifest contract fixtures and assert uniform interpretation of required/optional inputs, outputs, triggers and typed relations in `tests/test_skill_manifest_contract.py`.

## Phase 5: US3 — Registry Integrity (P1)

**Independent test**: Valid full catalog passes; each missing/duplicate/invalid identity, phase, reference and modified registry fails with source-specific diagnostics and no mutation.

- [x] T017 [US3] Enforce ID `ppmax-<slug>`, namespace `product-pro-max`, ASCII kebab-case, manifest/frontmatter/path agreement, unique IDs/slugs, no duplicate mappings and strict missing-manifest errors in `scripts/skill_registry_common.py` (SR-02).
- [x] T018 [US3] Validate every lifecycle `{cycle, phase?}` plus `tracks` against `model/product-model.json`, including primary-cycle membership, phase ownership and no repeated associations in `scripts/skill_registry_common.py` (SR-03).
- [x] T019 [US3] Validate related skill IDs exist, no self-links/duplicate or contradictory relations, only canonical relation types; validate workflow IDs against `workflows/*/workflow.yaml` without reimplementing orchestration in `scripts/skill_registry_common.py` (SR-03).
- [ ] T020 [US3] Verify gate/decision `semantic_kind` against explicitly documented allowed vocabulary in `specs/002-skill-manifest-registry/contracts/manifest-and-registry.md`: `evidence`, `gate`, `decision` (the example already uses `evidence`); for `gate`/`decision` check compatibility with `model/product-model.json` and do not conflate the two; reject unknown kinds in `scripts/skill_registry_common.py`.
- [ ] T021 [US3] Add failing fixture matrix for missing manifest, bad YAML/duplicate keys, duplicate ID/slug, mismatched frontmatter, path/cycle mismatch, unknown/incorrect phase, track, related skill, workflow and gate/decision kind in `tests/test_skill_registry_invalid.py` (SR-02, SR-03, SR-04).
- [x] T022 [US3] Add tests proving malformed input leaves preexisting `registry/skills.json` unchanged and `check` never writes in `tests/test_skill_registry_invalid.py` (SR-01, SR-04).

## Phase 6: US4 — Lifecycle Folder Organization and Migration (P1)

**Independent test**: Every legacy skill has one canonical path, unchanged bounded behavior and repaired workflow links; a multi-cycle skill remains discoverable beyond its folder.

- [ ] T023 [US4] Create reviewed old-path→canonical-path + primary-cycle mapping for all 13 existing skills in `specs/002-skill-manifest-registry/migration-inventory.md`, resolving collisions before file moves (SR-05).
- [ ] T024 [US4] Move all 13 distributable `skills/<legacy-name>/SKILL.md` to `skills/<primary-cycle>/ppmax-<slug>/SKILL.md`, updating frontmatter `name` only as required and preserving bounded behavior, evidence, triggers, outputs and workflow responsibilities (SR-05).
- [ ] T025 [US4] Write sibling `skills/<primary-cycle>/ppmax-<slug>/manifest.yaml` for each of the 13 migrated skills, with one valid primary cycle, optional additional lifecycle associations/tracks and complete trigger/input/output metadata.
- [ ] T026 [US4] Repair old skill path/name references in `workflows/idea-to-mvp/workflow.yaml`, `workflows/idea-to-first-users/workflow.yaml` and `workflows/pre-launch-audit/workflow.yaml`, preserving invocation order and responsibility.
- [ ] T027 [US4] Audit remaining legacy skill references in `README.md`, `README.vi.md` and `workflows/*/README.md`; record any intentionally retained compatibility mention separately in `specs/002-skill-manifest-registry/migration-inventory.md`.
- [ ] T028 [US4] Compare pre/post behavior fingerprints, exact workflows, trigger/evidence/output rules and link resolution for all 13 migrated skills in `specs/002-skill-manifest-registry/migration-inventory.md`; mark unresolved semantic differences explicitly (SR-05).
- [ ] T029 [US4] Verify canonical folder grouping is navigable while cross-cycle applicability remains in manifests; add wrong-folder and multi-lifecycle fixtures in `tests/test_skill_manifest_contract.py`.
- [ ] T030 [US4] After migration verification and fresh implementation modeling gate for this phase, promote implemented navigability and identity conventions to `README.md` and `README.vi.md`; do not promote proposed behavior.

## Phase 7: US5 — Canonical Skill Authoring (P1)

**Independent test**: Creation/update through `skill-creator-vi` yields valid canonical pairs and rejects bad metadata; `.agents/` stays excluded.

- [ ] T031 [US5] Update `.agents/skills/skill-creator-vi/SKILL.md` to read `SKILL-MODEL.md` and `SKILL-CONTRACT.md` as authority and require `ppmax-` naming, canonical cycle/path and sibling manifest without becoming a source of truth.
- [ ] T032 [US5] Add contributor-facing manifest/template generation workflow and validation invocation to `.agents/skills/skill-creator-vi/SKILL.md`; keep `.agents/` itself outside registry.
- [ ] T033 [US5] Test new skill and update-existing-skill authoring cases, identity mismatch rejection, missing metadata and `.agents/` exclusion in `tests/test_skill_creator_contract.py` (SR-06).
- [ ] T034 [US5] After verified authoring behavior and fresh implementation modeling gate for this phase, audit `SKILL-MODEL.md` and `SKILL-CONTRACT.md` against implemented authoring; correct documented drift only, without redefining the canonical contract.

## Phase 8: US6 — Global-First Boundaries (P2)

**Independent test**: ASCII machine IDs stay stable in localized views; similarly named development skills never appear in registry.

- [ ] T035 [US6] Enforce English ASCII machine identifiers across manifest and registry while allowing localized documentation labels without changing IDs in `scripts/skill_registry_common.py`.
- [ ] T036 [US6] Add localized-label and `.agents/` lookalike skill fixtures proving no ID fork or dev-tool registry leakage in `tests/test_skill_registry_invalid.py` (SR-06).
- [ ] T037 [US6] After verified registry behavior and fresh implementation modeling gate for this phase, document global-first discovery contract and dev-tool boundary in `docs/ARCHITECTURE.md`.

## Phase 9: Polish and Cross-Cutting Verification

- [ ] T038 Wire pinned parser installation and safe `generate --check` / fixture tests into `.github/workflows/skill-registry.yml`; require exact CI logs before marking runtime tests complete.
- [ ] T039 Run all planned commands from `specs/002-skill-manifest-registry/quickstart.md`, record Python/parser versions, inventory count, byte hashes, negative-case exit statuses and logs in `specs/002-skill-manifest-registry/verification.md`; no unsupported PASS claims.
- [ ] T040 After verified implementation and fresh implementation modeling, run project-level Diagram Check; update `docs/diagrams/` and any index only if semantic change merits an architecture diagram, recording a reasoned no-diagram-needed decision otherwise in `specs/002-skill-manifest-registry/verification.md`.
- [ ] T041 Audit FR-001–FR-032, SR-01–SR-07 and unresolved migration/CI evidence against `specs/002-skill-manifest-registry/spec.md`, `plan.md` and `tasks.md`; leave unverified tasks unchecked.

## Dependencies and Execution Order

- Phase 1 → Phase 2 → US1 core generation (T009–T012); the full registry build T013 is blocked by US3 integrity T017–T022 and US4 migration T023–T029; T013 is a deferred US1 completion checkpoint after these workstreams.
- US2 manifest semantics and US3 integrity must be wired before full-catalog generation; US4 uses their validators and existing inventory.
- US5 authoring integration begins after contract validation; US6 follows canonical identity enforcement. Phase 9 requires all included stories.
- Project-document promotion T030, T034, T037 and diagram assessment T040 require verified implementation and fresh `implementation:phase-XX` modeling gate of the corresponding phase; keep unchecked otherwise.

## Parallel Opportunities

- Once Phase 2 is complete: US2 contract fixtures (T016) can be authored separately from US1 registry serialization (T009) and US4 migration mapping (T023), but integration waits for validators.
- US5 authoring tests (T033) and US6 localization fixtures (T036) may be prepared in distinct files, then run after their prerequisites.
- Do **not** parallel-edit `scripts/skill_registry_common.py`, `SKILL-MODEL.md`, or `tests/test_skill_registry_invalid.py` without coordinating merges.

## Implementation Strategy

1. Establish inventory and shared validation foundation.
2. MVP: implement US1 generator/checker over fixtures, prove deterministic bytes and read-only drift detection; do not claim a populated registry until US4 migration.
3. Complete US2 and US3 contract/reference validation; migrate 13 skills under US4 with parity review and regenerate complete registry.
4. Finish US5 authoring, US6 global-first assertions and project-doc promotion only after fresh verified gates.
5. Run CI/quickstart, collect evidence, perform Diagram Check and converge without expanding into later-spec versioning, evaluations, catalog UI or ranking.
