# Tasks: Product Pro Max Design System

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/tokens-and-surfaces.md`, `quickstart.md`  
**State**: Spec/Plan/Tasks Modeling Gates pass; Phase 1 T001–T003 and Phase 2 T004–T011 implemented with isolated Python unit/contract checks on byte-verified sources (2026-10-09). Full checkout regression, browser and GitHub asset QA remain outside this execution evidence; Phase 3–7 not started.  
**Tests**: Explicitly required by FR-014–FR-022 and SC-001–SC-007; do not mark PASS without run-specific evidence.  
**Format**: `- [ ] TNNN [P?] [US?] Action in exact path`; `[P]` denotes safe parallelism only on separate files.

## Runtime Risk Coverage

| Risk ID | Status | Requirement refs | Prevention / validation intent | Tasks | Required evidence |
| --- | --- | --- | --- | --- | --- |
| DS-R01 token drift | APPLIES | FR-001,017,021,027 | deterministic snapshot/revision checks | T006, T009, T014, T015, T047 | token tamper and read-only drift fixtures |
| DS-R02 global profile leak | APPLIES | FR-020,023 | repo-scoped token source with fail-closed resolution | T010, T016, T019, T025 | foreign-home-profile and missing-local-role cases |
| DS-R03 semantic corruption | APPLIES | FR-005,008,018 | dedicated semantic inventory parity | T020, T023, T039, T041, T049 | before/after node/edge/gate/decision/link diff |
| DS-R04 accessibility | APPLIES | FR-013–016 | contrast, focus, long text, viewport checks | T017, T022, T026, T044, T045 | per-theme contrast matrix + keyboard/zoom screenshots |
| DS-R05 offline/GitHub | APPLIES | FR-009,011,013 | self-contained exports; GitHub static SVG | T021, T029, T033, T034, T046 | offline browser and actual GitHub preview |
| DS-R06 migration partial | APPLIES | FR-010,018,019,025 | source snapshot, atomic Atlas update, rollback | T038–T043, T048, T050 | reversible pilot with Atlas/layout/self_check and screenshots |
| DS-R07 false QA | APPLIES | FR-022 | distinct static/browser/manual evidence | T011, T045, T048, T051 | report with separate status per QA layer |
| DS-R08 malformed skin | APPLIES | FR-004,006,021 | strict token validator | T004, T008, T013, T017 | invalid role/theme/color fixtures |
| DS-R09 hosted runtime | NOT_APPLICABLE | FR-024 | no hosted runtime or DB in scope | T052 (scope audit) | verify repo diff contains none |

## Phase 1: Setup and baseline

**Goal**: Capture existing truths before any visual implementation. T001–T003 were completed by an evidence-linked GitHub source inventory, preservation of the approved concept reference and current-HEAD reconciliation. No local validator/browser execution or visual implementation is claimed.

- [x] T001 Inventory current `docs/diagrams/diagram-index.json`, `docs/diagrams/index.html`, `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html` and relevant validation scripts; record pre-migration baseline in `specs/003-product-pro-max-design-system/migration-baseline.md`.
- [x] T002 Preserve the approved one-file HTML concept as a non-authoritative design reference and record version/source in `design-system/README.md`, with explicit separation from executable contracts. [FR-026]
- [x] T003 Confirm the current `main` HEAD, actual existing 003 directories, active feature pointer, roadmap numbering and any existing `.diagram-design` marker before writing to the repo; document reconciliation in `specs/003-product-pro-max-design-system/integration-notes.md`.

## Phase 2: Foundations — shared and blocking

**Goal**: One token source, deterministic generation, independent semantic input. **Phase 2 source + isolated Python tests complete:** see `phase-02-evidence.md` for exact tested blob hashes and verification boundaries. No diagram was modified and no full-checkout/browser QA was claimed.

- [x] T004 [P] Define complete canonical role sets, theme values, Signal Lime brand alias, typography/fallbacks and density values in `design-system/tokens.json`; review accessible official combinations. [FR-001,002,004,006]
- [x] T005 [P] Define surface/role-to-primitive mapping, gate-result/decision separation and required visible labels in `design-system/components.md`. [FR-005,007,008]
- [x] T006 Implement deterministic JSON-to-inline-CSS / SVG-token adapter with revision stamps in `scripts/export_design_tokens.py`, with read-only check and no network access. [FR-009,017,027]
- [x] T007 [P] Write human-maintainer instructions and source precedence in `design-system/README.md`, linking spec/contract without duplicating token values. [FR-020,023]
- [x] T008 Implement token structural/type/required-role/variant/contrast validation in `scripts/verify_design_system.py`; reject unknown theme/density and invalid CSS values. [FR-014,021]
- [x] T009 Add deterministic generation/revision drift tests in `tests/test_design_system_tokens.py`, including no-write check mode. [FR-001,017,027]
- [x] T010 Add wrong-profile, missing-local-tokens and malformed-role negative fixtures in `tests/test_design_system_tokens.py`. [FR-020,021]
- [x] T011 Define distinct semantic-source, static-check, browser-visual, GitHub-render statuses and mandatory evidence fields in `design-system/README.md`. [FR-022]

**Checkpoint**: Token contract validated without touching Product Model or the existing `.agents` global profile.

## Phase 3: User Story 1 — flexible token/theme system (P1)

**Independent test**: Same sample semantic input generates Light/Dark and alternate-accent variants while retaining identical semantic inventory, source path and role IDs.

- [ ] T012 [P] [US1] Create complete sample roles/states for theme permutations in `tests/fixtures/design-system/semantic-sample.json`. [FR-004,006]
- [ ] T013 [US1] Add negative tests for unresolved status, missing state label and insufficient official theme contrast in `tests/test_design_system_tokens.py`. [FR-007,014,021]
- [ ] T014 [US1] Generate default, Light and alternate-accent output snapshots via `scripts/export_design_tokens.py`; document expected revision/fingerprint behavior in `design-system/README.md`. [FR-004,017,027]
- [ ] T015 [US1] Confirm visual-token changes do not alter specimen semantic snapshot or Spec Kit source hash in `tests/test_design_system_tokens.py`. [FR-005,027]
- [ ] T016 [US1] Verify project-specific tokens override global profile without changing installed global preferences; reject absent repo tokens in `tests/test_design_system_tokens.py`. [FR-020]
- [ ] T017 [US1] Verify contrast/fallback/font/density variants with both automated checks and reviewed screenshots, preserving exact evidence in `specs/003-product-pro-max-design-system/qa-evidence.md`. [FR-013,014,016]

**Checkpoint**: All configured themes and density choices resolve predictably; browser evidence reported separately.

## Phase 4: User Story 2 — readable HTML diagrams and Atlas (P1)

**Independent test**: A standalone specimen and a source-equivalent Spec 002 pilot preserve labels, direction, planned state and navigation while changing only presentation.

- [ ] T018 [P] [US2] Specify Signal Protocol visual primitives/limits and orthogonal connector geometry in `design-system/components.md`, reusing `diagram-design-vi` instead of replacing it. [FR-007,023,024]
- [ ] T019 [US2] Implement a repo-aware style resolution adapter in `.agents/skills/diagram-design-vi/SKILL.md` and the smallest necessary mapping reference(s), leaving generic global profiles untouched. [FR-020,023]
- [ ] T020 [P] [US2] Add gate-result vs decision and semantic inventory tests in `tests/test_design_system_diagrams.py` using authoritative example values. [FR-005,008]
- [ ] T021 [US2] Build offline-capable self-contained HTML/SVG sample from `design-system/tokens.json` following visual primitives and source metadata rules, saving only as a test artifact under `tests/fixtures/design-system/`. [FR-007,009]
- [ ] T022 [US2] Add accessible SVG title/desc, status text/icons, visible keyboard focus and reduced-motion affordances in the sample generator and `design-system/components.md`. [FR-013–016]
- [ ] T023 [US2] Audit the sample's edges and gate/result labels against its source inventory in `tests/test_design_system_diagrams.py`. [FR-005,008,018]
- [ ] T024 [P] [US2] Prepare Atlas/Feature Ledger navigation styling as a derived view without changing scope/truth/parent/related semantics, scoped to `docs/diagrams/index.html` and `specs/002-skill-manifest-registry/diagrams.html`. [FR-010]
- [ ] T025 [US2] Validate a second environment with different `~/.diagram-design` profile still chooses Product Pro Max repo tokens; document results in `specs/003-product-pro-max-design-system/qa-evidence.md`. [FR-020]
- [ ] T026 [US2] Run visual QA of HTML diagrams at Light/Dark, 390px, 200% zoom and keyboard focus; record screenshot/test evidence and failures without force-PASS. [FR-014–016,022]

**Checkpoint**: Existing modeling/Atlas authority remains unchanged.

## Phase 5: User Story 3 — Core + Brand Assets (P2)

**Independent test**: Both README theme variants and standalone brand assets render offline/GitHub using approved logo and common visual roles, without JS execution.

- [ ] T027 [P] [US3] Define Signal Path geometry, wordmark lockup and accessible naming/safe-area in `design-system/README.md`. [FR-003]
- [ ] T028 [US3] Create and validate source `assets/brand/signal-path.svg` plus `assets/brand/wordmark.svg` from canonical roles; retain recognizable brand across sizes. [FR-003,012]
- [ ] T029 [US3] Produce standalone `assets/brand/hero-light.svg` and `assets/brand/hero-dark.svg` with consistent logo and theme-specific contrast. [FR-002,011,012]
- [ ] T030 [P] [US3] Document usage in Markdown, diagrams, docs and social variants in `design-system/README.md` without adding generic SaaS button/card chrome. [FR-012]
- [ ] T031 [US3] Integrate SVG hero variants into `README.md` and `README.vi.md` with GitHub-compatible light/dark selection and proper alt/fallback. [FR-011]
- [ ] T032 [US3] Use the same tokens for a docs specimen and a brand cover export; verify identical brand mark treatment without forcing one identical layout. [FR-012,017]
- [ ] T033 [US3] Verify SVG and self-contained outputs offline with no remote fonts, CSS or JS; preserve proof in `specs/003-product-pro-max-design-system/qa-evidence.md`. [FR-009,013]
- [ ] T034 [US3] Inspect actual README image rendering in GitHub Light/Dark and fallback contexts; record exact coverage in `specs/003-product-pro-max-design-system/qa-evidence.md`. [FR-011,022]

**Checkpoint**: Brand assets compatible with GitHub and standalone use.

## Phase 6: User Story 4 — safe migration and compatibility (P2)

**Independent test**: Spec 002 diagram can be opt-in migrated and reverted, with a full semantic/source/navigation parity report.

- [ ] T035 [P] [US4] Record original Spec 002 diagram and Atlas entry snapshot in `specs/003-product-pro-max-design-system/migration-baseline.md`. [FR-018,019]
- [ ] T036 [US4] Define reversible migration/rollback checklist in `specs/003-product-pro-max-design-system/migration-baseline.md`; no bulk migration before pilot signoff. [FR-019,025]
- [ ] T037 [US4] Produce migrated **copy** of `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html` under an isolated temporary path for side-by-side review. [FR-018,019]
- [ ] T038 [US4] Audit source, all text/edge semantics, planned/implemented labels, Atlas/ledger/backlinks for parity using `tests/test_design_system_diagrams.py`. [FR-010,018]
- [ ] T039 [US4] After pilot approval, promote migration to original Spec 002 diagram while keeping a restore path and an unchanged authoritative `spec.md`. [FR-018,019,025]
- [ ] T040 [US4] Apply Atlas/Feature Ledger/registry derived presentation transaction with preserved graph integrity; run existing `scripts/verify-diagram-atlas.py`. [FR-010,018]
- [ ] T041 [US4] Run existing `scripts/verify-diagram-layout.py` and `.agents/skills/diagram-design-vi/scripts/self_check.py` on migrated artifact with correct CLI; inspect connector collisions at browser zoom. [FR-018,019]
- [ ] T042 [US4] Compare screenshots Light/Dark/mobile, keyboard usability, exact source labels and reversibility; document accepted pilot/failures. [FR-015,016,019,022]
- [ ] T043 [US4] Keep all other existing diagrams unchanged until an explicit follow-up migration scope is approved; confirm old diagram HTML still opens. [FR-025]

**Checkpoint**: No previously working diagram is silently reinterpreted or lost.

## Phase 7: QA, documentation and convergence preparation

- [ ] T044 [P] Run per-theme contrast checks with text and meaningful non-text elements, including warning/danger/focus states; attach actual numbers and evidence in `specs/003-product-pro-max-design-system/qa-evidence.md`. [FR-014]
- [ ] T045 Run browser screenshot, responsive (390px), 200% zoom, keyboard and reduced-motion tests of target surfaces; report evidence dimensions separately from static checks. [FR-015,016,022]
- [ ] T046 [P] Validate all standalone outputs in network-off mode and README SVG variants in GitHub-compatible rendering. [FR-009,011,013]
- [ ] T047 [P] Run token/asset deterministic drift checks and revision audits after changes; record result. [FR-017,021,027]
- [ ] T048 Run full diagram Atlas/layout/self_check suites against actual checkout; verify source/registry reachability and no unlisted living diagram. [FR-010,018,022]
- [ ] T049 Compare semantic snapshot across token skin variants and final migrated pilot, proving Gate result and Decision mapping untouched. [FR-005,008,018]
- [ ] T050 Restore originals on any pilot mismatch; do not promote implemented diagram/docs if verification is incomplete. [FR-019,022,025]
- [ ] T051 Write `specs/003-product-pro-max-design-system/qa-evidence.md` with separately reported source/static/browser/GitHub/actual publishing state and evidence provenance. [FR-022]
- [ ] T052 Audit final diff for scope violations (new frontend framework, DB/network service, Product Model/Registry edits, new semantics engine) before any commit. [FR-024]
- [ ] T053 After implementation verification, promote truthful architecture guidance to `docs/ARCHITECTURE.md`, local design docs and README without claiming project-level implemented truth prematurely. [FR-023]
- [ ] T054 Reconcile `specs/ROADMAP-foundation.md` numbering and dependencies before integration; update `.specify/feature.json` when Spec 003 is selected as active; re-check current `main` head. [FR-023]
- [ ] T055 Run Spec Kit analyze/converge and recheck stale design/modeling gates with real artifacts; do not label runtime/browser PASS without evidence. [FR-022,027]

## Dependencies & Execution Order

- Phase 1 → Phase 2 (foundation) → US1 and US2; US3 may develop source art after tokens stabilize; US4 waits for US2 pilot.
- `T004–T011` are core blocking tasks. `T019` needs role mapping; `T024` should not be promoted as implemented docs before acceptance.
- `T037–T043` are deliberately serial and conditional: the promoted migration `T039` requires acceptance of copy and parity first.
- Final Phase 7 is after intended deliverables; docs promotion requires verified implementation.
- `[P]` does not imply independent task semantics; it only marks nonconflicting file operations where specified.

## Requirement Traceability

| Requirement group | Tasks |
| --- | --- |
| FR-001–FR-006 | T004–T017, T049 |
| FR-007–FR-010 | T005, T018–T024, T038–T041 |
| FR-011–FR-013 | T027–T034, T046 |
| FR-014–FR-016 | T008, T017, T022, T026, T042, T044–T046 |
| FR-017–FR-021 | T006, T009–T010, T014–T016, T035–T043, T047 |
| FR-022–FR-027 | T002, T007, T011, T019, T034, T042, T045, T051–T055 |

**Implementation note**: T001–T003 were checked for actual source-inventory and documentation changes, not for earlier specification/planning alone. All other implementation tasks remain unchecked; `ensure-model(tasks)` was completed with a negative Diagram Check before Phase 1. Browser/runtime verification is not implied.
