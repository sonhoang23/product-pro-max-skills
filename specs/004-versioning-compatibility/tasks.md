# Tasks: Versioning & Compatibility

**Branch:** `main` | **Feature:** `specs/004-versioning-compatibility` | **State:** implementation in progress; Phases 1–2 complete; US1 T010–T019 source complete, Modeling Gate verified before docs promotion (29/75 checked; Phase 4 US2 T020–T029 source+tests+Modeling Gate complete; docs-promotion CI PASS at fc43559 (Validate + Skill Registry).

**Inputs:** [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/compatibility-assessment.md](contracts/compatibility-assessment.md), [quickstart.md](quickstart.md).

**Gate:** `spec = modeled`, `plan = no-diagram-needed` (fresh); canonical `runtime-verification` v1.12.0 synced. This checklist is NOT implementation/test evidence.

## Format: `[ID] [P?] [Story] Description`

Task IDs are append-only (`T001`–`T075`); T074/T075 are added to Phase 5 without renumbering previous tasks. Execute by dependency/phase, not ID order alone. `[P]` means independent work within a phase, not permission to bypass prerequisites.

## Runtime Risk Coverage

Source: synced `.agents/skills/runtime-verification/` from `oh-my-skill` commit `fcd9a5b8db9c37673b9bb92d69bf6056af30ec3a`. Review in `tasks` mode; no new canonical Risk IDs or `NEEDS_UPSTREAM` identified. **Do not mark Risk PASS during task creation.**

| Risk ID | Status | Requirement refs | Prevention design | Task IDs / N/A | Required evidence |
|---|---|---|---|---|---|
| ENV-003 | APPLIES | FR-025–028 | Normalize paths across Windows and Linux | T049, T052 | Native Windows + Linux Python 3.12 path/diagnostic parity, with OS, command, revision and exit proof; NOT_RUN |
| VERIFY-003 | APPLIES | FR-007–008, FR-027–029 | Bind evidence to commit/digests; rerun stale proof | T047, T071 | Source revision/digest mutation invalidates prior PASS; evidence refreshed on final commit; NOT_RUN |
| VERIFY-008 | APPLIES | FR-024–028 | Fail fast on invalid setup/fixture baseline | T028, T048 | Invalid fixture prerequisites fail fast with root-cause path before evaluating impact; NOT_RUN |
| VERIFY-004 | APPLIES | FR-025–027 | Unexpected warnings never count as clean PASS | T050 | Inject unexpected warning with child exit 0; no clean verified claim without scoped classification; NOT_RUN |
| API-001 | NOT_APPLICABLE | No OpenAPI client | Offline file-based checker | N/A: surface absent | Boundary does not exist |
| DB-002 | NOT_APPLICABLE | No database migration journal | Explicit file-level data migration | N/A: surface absent | Boundary does not exist |
| STARTUP-001 | NOT_APPLICABLE | No service/port | Offline CLI | N/A: surface absent | Boundary does not exist |

**Deferred trigger checks:** ENV-001, ENV-004, VERIFY-001 and VERIFY-010 only if implementation introduces install, wrapper, or runner concurrency; VERIFY-002/ENV-005 if actual environment incident occurs. No frontend/auth/DB/network boundary is added by this CLI.

## Phase 1 — Setup

**Goal:** Inventory current sources; prepare isolated fixtures.

**Independent Test:** Source inventory and fixture conventions are explicit.

- [x] T001 Inventory existing model/skill/workflow/schema/project-state owners, `registry_version` and lockfile marker in `specs/004-versioning-compatibility/implementation-inventory.md`.
- [x] T002 [P] Define synthetic supported/unsupported fixtures and immutable-ref conventions in `tests/fixtures/compatibility/README.md`.
- [x] T003 [P] Document offline read-only source/ledger scope in `compatibility/README.md`.

**Checkpoint:** Record actual evidence; no automated PASS inferred.

---

## Phase 2 — Foundational

**Goal:** Typed offline parsing and explicit supported baseline ledger.

**Independent Test:** Invalid or missing ledger is diagnosed; empty ledger never means published.

- [x] T004 Define strict ledger and source provenance contract in `schemas/supported-baselines.schema.json`.
- [x] T005 Implement typed component, baseline, consumer dependency and diagnostic models in `scripts/compatibility_common.py`.
- [x] T006 Implement safe ledger loading, digest/ref comparison, duplicate rejection and normalized relative paths in `scripts/compatibility_common.py`.
- [x] T007 Create honest empty default support ledger (no published skills) in `compatibility/supported-baselines.json`.
- [x] T008 Test missing/malformed baseline, path traversal, duplicate ID, bad SHA and empty ledger in `tests/test_compatibility_foundation.py`.
- [x] T009 Align expected validation commands without claimed PASS in `specs/004-versioning-compatibility/quickstart.md`.

**Checkpoint:** Record actual evidence; no automated PASS inferred.

---

## Phase 3 — US1: Independent Component Versions (P1, MVP)

**Goal:** Distinct source-owned versions and SemVer policy.

**Independent Test:** PATCH/MINOR/MAJOR/pre-1.0/initial examples pass; style/lock/version marker changes do not bump unrelated components.

- [x] T010 [P] [US1] Define stable/pre-1.0/initial version cases and expected bump matrix in `tests/test_compatibility_versions.py`.
- [x] T011 [US1] Implement SemVer validation, precedence and incompatible/compatible/patch recommendation in `scripts/compatibility_common.py`.
- [x] T012 [US1] Implement owner lookup for model, manifest, workflow, schema and project-data versions in `scripts/compatibility_common.py`.
- [x] T013 [US1] Extend strict manifest parser for a planned canonical `version` field while detecting unversioned legacy manifests in `scripts/skill_registry_common.py`.
- [x] T014 [US1] Test duplicate YAML keys, unknown keys, added version and legacy readers in `tests/test_skill_manifest_contract.py`.
- [x] T015 [US1] Check future workflow version semantics without fabricating a published workflow in `tests/test_compatibility_versions.py`.
- [x] T016 [US1] Author versioning, 0.x, first-baseline and publication evidence policy in `VERSIONING.md`.
- [x] T017 [US1] Test higher-precedence bump and unrelated `registry_version`/`skills-lock.json.version`/README differences in `tests/test_compatibility_versions.py`.
- [x] T018 [US1] After US1 tests and fresh `implementation:phase-03` Modeling Gate, promote implemented model version policy in `PRODUCT-MODEL.md`.
- [x] T019 [US1] After US1 tests and fresh `implementation:phase-03` Modeling Gate, promote implemented skill authority rules in `SKILL-MODEL.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 4 — US2: Consumer Impact (P1)

**Goal:** Known-reader strictness, dependency graph and semantics-aware comparison.

**Independent Test:** Closed enum, added required field, removed output, changed canonical ID, unknown baseline or consumer and conflicts get bounded verdicts.

- [x] T020 [P] [US2] Add strict/lenient, closed-enum, changed-ID and missing-consumer fixture definitions in `tests/fixtures/compatibility/README.md`.
- [x] T021 [US2] Test tolerant/strict reader and removed output/unknown baseline expectations in `tests/test_compatibility_consumers.py`.
- [x] T022 [US2] Enumerate canonical known consumers and version-constrained dependency edges in `scripts/compatibility_common.py`.
- [x] T023 [US2] Diff schema requiredness, output names, Product Model IDs/relationships and expected file shapes in `scripts/compatibility_common.py`.
- [x] T024 [US2] Check strict reader support before treating additive enum, optional field or new metadata as compatible in `scripts/compatibility_common.py`.
- [x] T025 [US2] Check version ranges, unsupported provider, missing dependency, conflicting range and cycle in `scripts/compatibility_common.py`.
- [x] T026 [US2] Keep semantic trigger/exclusion, evidence rules, stopping conditions and gate/decision changes review-required without behavioral proof in `scripts/compatibility_common.py`.
- [x] T027 [US2] Emit impacted consumer, source path, offending change, classification and next action in `scripts/compatibility_common.py`.
- [x] T028 [US2] Fail-fast invalid fixture setup (VERIFY-008); assert unknown external readers remain unassessed in `tests/test_compatibility_consumers.py`.
- [x] T029 [US2] After US2 tests and fresh `implementation:phase-04` Modeling Gate, promote demonstrated strict-reader and dependency rules in `SKILL-CONTRACT.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 5 — US3: Durable Data Migration (P1)

**Goal:** Explicit, recoverable data evolution.

**Independent Test:** Legacy/repeated/interrupted/missing-source fixtures preserve assumptions, provenance and decision history.

- [ ] T030 [P] [US3] Create isolated legacy/mixed, interrupted and missing-data scenarios in `tests/fixtures/compatibility/migration/README.md`.
- [ ] T031 [US3] Define migration source/target/receipt/status/recovery schema in `schemas/compatibility-migration.schema.json`.
- [ ] T032 [US3] Test legacy record parse and no loss of decision history or provenance in `tests/test_compatibility_migrations.py`.
- [ ] T033 [US3] After T031/T074/T075, implement source/target preflight, explicit legacy-unversioned classification and default dry-run in `scripts/migrate_project_contract.py`.
- [ ] T034 [US3] Implement backups/copy-on-write/atomic replacement with reviewed irreversibility exception in `scripts/migrate_project_contract.py`.
- [ ] T035 [US3] Implement idempotency key, repeated input detection and applied/already_applied/partial/failed receipts in `scripts/migrate_project_contract.py`.
- [ ] T036 [US3] Verify canonical evidence provenance, assumptions and decision histories after transform in `scripts/migrate_project_contract.py`.
- [ ] T037 [US3] Inject interrupted-write, retry, out-of-order, mutated-source and partial failure tests in `tests/test_compatibility_migrations.py`.
- [ ] T038 [US3] Assert assess and dry-run never mutate originals; apply requires explicit command in `tests/test_compatibility_migrations.py`.
- [ ] T039 [US3] Document recovery, legacy support and never-mass-rewrite guidance in `compatibility/migrations/README.md`.
- [ ] T074 [US3] After T012/T031, add opt-in `contract_version` to `schemas/project-state.schema.json` and `templates/project-state/project.yaml` for newly created state; preserve unversioned legacy reads, history and source authority (FR-017–020, FR-031).
- [ ] T075 [US3] After T074, test new/legacy/mixed-version template/schema behavior and no silent rewrite in `tests/test_compatibility_migrations.py`; include `scripts/validate_repo.py` contract integrity evidence before T033/T040.
- [ ] T040 [US3] After T074/T075 and US3 tests plus fresh `implementation:phase-05` Modeling Gate, promote implemented durable-data behavior to `docs/ARCHITECTURE.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 6 — US4: Enforce Compatibility Gate (P1)

**Goal:** Deterministic read-only classification, diagnostics and CI blocking.

**Independent Test:** Known breaking change with weak bump/migration blocks; unknown review non-green; evidence not overstated.

- [ ] T041 [P] [US4] Test expected CLI codes 0 allow/1 block/2 review/3 invalid and missing-migration cases in `tests/test_compatibility_gate.py`.
- [ ] T042 [US4] Define schema for baseline/candidate, revision, consumer scope, diagnostics and proof level in `schemas/compatibility-assessment.schema.json`.
- [ ] T043 [US4] Implement explicit assess command, candidate root/ref and optional report path in `scripts/check_compatibility.py`.
- [ ] T044 [US4] Implement aggregate classification compatible/breaking/review_required/unassessed without Product Model gate conflation in `scripts/compatibility_common.py`.
- [ ] T045 [US4] Block insufficient MAJOR/MINOR/PATCH bump or unresolved known breaking migration/dependency in `scripts/check_compatibility.py`.
- [ ] T046 [US4] Emit deterministic human/JSON reports and machine-readable error codes without touching source files in `scripts/check_compatibility.py`.
- [ ] T047 [US4] Test stale baseline/candidate commit/hash invalidation and evidence refresh (VERIFY-003) in `tests/test_compatibility_gate.py`.
- [ ] T048 [US4] Test invalid source/consumer fixture setup fails fast (VERIFY-008) in `tests/test_compatibility_gate.py`.
- [ ] T049 [US4] Test diagnostics and path equivalence on native Windows and Linux Python 3.12 (not simulated-only separators; ENV-003) in `tests/test_compatibility_gate.py`.
- [ ] T050 [US4] Test unexpected warning prevents clean PASS despite exit 0 (VERIFY-004) in `tests/test_compatibility_gate.py`.
- [ ] T051 [US4] Check read-only integrity using source/registry/project-fixture pre/post hashes in `tests/test_compatibility_gate.py`.
- [ ] T052 [US4] Integrate positive/negative compatibility checks in Python 3.12 CI `.github/workflows/validate.yml` after fixture validation, including native `windows-latest` parity for T049/ENV-003 alongside Linux.
- [ ] T053 [US4] After US4 CI and fresh `implementation:phase-06` Modeling Gate, promote verified checker vs Product Model gate semantics to `QUALITY-GATES.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 7 — US5: Deprecation (P2)

**Goal:** Safe support transitions and removal exceptions.

**Independent Test:** Supported-deprecated differs from unsupported/removed; early removal blocks.

- [ ] T054 [P] [US5] Add no-replacement, old-supported, unsupported and emergency fixtures to `tests/test_compatibility_deprecation.py`.
- [ ] T055 [US5] Define deprecation notice support window/replacement/consumer/exception fields in `schemas/compatibility-deprecation.schema.json`.
- [ ] T056 [US5] Check active→deprecated→unsupported→removed progression and required notices in `scripts/compatibility_common.py`.
- [ ] T057 [US5] Block removal without impacted-consumer/migration disposition unless exception authorized in `scripts/check_compatibility.py`.
- [ ] T058 [US5] Test emergency security exception retains breaking verdict and approved mitigation in `tests/test_compatibility_deprecation.py`.
- [ ] T059 [US5] Test status boundaries, replacement missing, migration instructions and support windows in `tests/test_compatibility_deprecation.py`.
- [ ] T060 [US5] After US5 tests and fresh `implementation:phase-07` Modeling Gate, promote verified deprecation policy in `VERSIONING.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 8 — US6: Discover Supported Scope (P2)

**Goal:** Truthful support inspection in repository docs and checker.

**Independent Test:** Model 1.0.0/empty registry/lock marker distinguish existence from published release.

- [ ] T061 [P] [US6] Test no published skills, registry marker and model version examples in `tests/test_compatibility_support.py`.
- [ ] T062 [US6] Expose baseline/published-status summary with known coverage and unknown readers in `scripts/check_compatibility.py`.
- [ ] T063 [US6] Test policy-defined, static, behavioral, migrated-in-test, runtime and published evidence distinctions in `tests/test_compatibility_support.py`.
- [ ] T064 [US6] After US6 tests and fresh `implementation:phase-08` Modeling Gate, promote versioning boundaries into `docs/ARCHITECTURE.md`.
- [ ] T065 [US6] After US6 tests and fresh `implementation:phase-08` Modeling Gate, document contributor verification and publishing limits in `CONTRIBUTING.md`.
- [ ] T066 [US6] After US6 tests and fresh `implementation:phase-08` Modeling Gate, expose policy link and truthful current state in `README.md`.
- [ ] T067 [US6] After US6 tests and fresh `implementation:phase-08` Modeling Gate, align translated public status without translating IDs in `README.vi.md`.
- [ ] T068 [US6] Run project Diagram Check; update `docs/diagrams/diagram-index.json` only for proven need or log no-diagram decision in `specs/004-versioning-compatibility/verification.md`.

**Checkpoint:** Finish story tests and confirm fresh implementation modeling before any project-doc promotion.

---

## Phase 9 — Integration and Convergence

**Goal:** Collect only current revision-bound proof.

**Independent Test:** SC-001–010 checked; no unverified runtime, project migration or publishing claim.

- [ ] T069 Run complete positive/negative acceptance matrix from `specs/004-versioning-compatibility/quickstart.md`, recording commands and counts in `specs/004-versioning-compatibility/verification.md`.
- [ ] T070 Record repository/registry/migration/checker suites, warnings and final exit status in `specs/004-versioning-compatibility/verification.md`.
- [ ] T071 Recheck HEAD/input hashes, invalidate and rerun stale gate evidence (VERIFY-003) in `specs/004-versioning-compatibility/verification.md`.
- [ ] T072 Audit US1–US6, FR-001–032, SC-001–010 and Risk→Task→Proof trace in `specs/004-versioning-compatibility/analysis.md`.
- [ ] T073 Run modeling and convergence; document blocked/unverified runtime and publishing proofs in `specs/004-versioning-compatibility/verification.md`.

**Checkpoint:** Record actual evidence; no automated PASS inferred.

## Dependencies & Execution Order

- Phase 1 → Phase 2 blocks all stories.
- US1 independently establishes version owners and SemVer; MVP = Phase 1–3.
- US2 depends on US1 component identities; US3 can run in parallel after US1 version owners. Explicit US3 path: T012/T031 → T074 → T075 → T033/T040; earlier T032 test scaffolding cannot claim PASS without T075.
- US4 needs US1/US2 and US3 migration-disposition interfaces before enforcing gate. T045 relies on T031/T033/T074/T075 proof, and T049/T052 need native Windows/Linux evidence.
- US5 needs US1 support/version and US2 consumer impact; US6 integrates supported baselines, proof status and published/unpublished distinctions.
- Final Phase 9 follows selected completed story set, full tests, fresh implementation modeling and convergence. T071 invalidates affected earlier proof after later edits.
- Project docs promotion tasks follow each story's verification and fresh `implementation:phase-XX` gate; no planned truth promoted as implemented.

## Parallel Examples

- T002 ∥ T003 after source inventory (distinct fixture/compatibility docs).
- US1 version matrix test T010 can be drafted while policy is written, without claiming code pass.
- US2 consumer tests and US3 migration tests may be developed independently after US1; never edit `scripts/compatibility_common.py` concurrently.
- US4 schema task and CLI tests can be developed independently; T049–T053 require working CLI.
- US5 notice tests and schema can be prepared in parallel. US6 support fixtures may start before discovery CLI.

## Requirement Coverage

| Scope | Phase | Evidence |
|---|---|---|
| US1 / FR-001–006, FR-031 | 2–3 | Per-component version ownership and bump matrix |
| US2 / FR-007–016, FR-029 | 4 | Strict-reader and dependency-impact scenarios |
| US3 / FR-017–020, FR-031 | 5 (includes T074/T075) | Legacy migration, versioned project-state schema/template, preservation |
| US4 / FR-024–028 | 6 | CLI diagnostics/exit and native Windows/Linux CI parity |
| US5 / FR-021–023 | 7 | Deprecation/removal/exception fixtures |
| US6 / FR-027, FR-029–032 | 8 | Honest support and documentation discovery |
| SC-001–010 | 3–9 | Recorded acceptance matrix and proof in `verification.md` |

## Delivery Strategy

MVP = T001–T019. Then US2/US3 (T074/T075 appended), US4, US5, US6 and final convergence. Total: 75 unchecked tasks. Spec 005 evals, Spec 006 governance, Spec 008 release automation and Spec 009 shared-context implementation are excluded.
