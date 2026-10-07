# Tasks: Canonical Product Model

**Input**: Design documents from `specs/001-canonical-product-model/`

## Runtime Risk Coverage

| Risk ID | Status | Requirement refs | Prevention design | Task IDs / reason N/A | Required evidence |
| --- | --- | --- | --- | --- | --- |
| N/A | NOT_APPLICABLE | — | No application runtime boundary is introduced | Repository-development runtime companion is not installed; deterministic contract validation covers this feature | Validator + installer dry-run |

## Phase 1: Canonical Contract
- [x] T001 [US1] Create canonical ontology data in `model/product-model.json`
- [x] T002 [US1] Define structural schema in `schemas/product-model.schema.json`
- [x] T003 [US1] Create normative human explanation in `PRODUCT-MODEL.md`

## Phase 2: Machine Contract Synchronization
- [x] T004 [US2] Align gate and decision enums in `schemas/skill-output.schema.json`
- [x] T005 [US2] Replace legacy stage semantics with canonical cycle/phase/status contract in `schemas/project-state.schema.json`
- [x] T006 [US2] Align default state in `templates/project-state/project.yaml`
- [x] T007 [US2] Add Product Model invariants and drift checks in `scripts/validate_repo.py`
- [x] T008 [US2] Run `python scripts/validate_repo.py` and preserve passing evidence

## Phase 3: Project Docs Promotion
- [x] T009 [US3] Promote canonical navigation and lifecycle summary into `README.md`
- [x] T010 [US3] Promote hierarchy and authority into `docs/ARCHITECTURE.md`
- [x] T011 [US3] Clarify gate-result vs decision semantics in `QUALITY-GATES.md`
- [x] T012 [US3] Reference canonical output semantics from `SKILL-CONTRACT.md`
- [x] T013 [US3] Add localized navigation to the canonical model in `README.vi.md`
- [x] T014 [US3] Run validator and installer dry-run

## Phase 4: Convergence
- [x] T015 Compare constitution, spec, plan, tasks, Product Model, dependent schemas, templates, validator, and promoted docs; resolve any actionable gap before declaring Spec 001 converged

## Verification Evidence

- GitHub Actions run `37562964123` passed for core Product Model contract implementation (`356fe97`).
- GitHub Actions job `112604598658` passed both repository contract validation and installer dry-run for promoted docs commit (`d97fb6c`).
- Convergence review found no missing, partial, contradictory, or unrequested behavior within Spec 001 scope.
- No diagram was created because the ontology inventory is more legible and searchable as structured data and tables; all modeling gates therefore resolve to `no-diagram-needed`.

## Dependencies & Execution Order
Phase 1 establishes authority. Phase 2 synchronizes machine contracts. Phase 3 runs only after Phase 2 validation. Phase 4 runs after documentation promotion and final validation.
