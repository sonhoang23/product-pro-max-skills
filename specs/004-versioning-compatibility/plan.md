# Implementation Plan: Versioning & Compatibility

**Branch:** main | **Date:** 2026-10-13 | **Spec:** [spec.md](spec.md)
**Status:** PLAN DESIGN ONLY — no checker, migration, publication, runtime verification or task implementation claimed.
**Source gate:** `spec = modeled`; `.modeling-state.json` fingerprint `cf92fc9801e0f34d72c7861df8a03225d93a0170` matches current `spec.md` blob; diagram `spec-diagram/compatibility-assessment.html` present. Existing modeling evidence is scoped to diagram QA.

## Summary

Define independently owned component versions and a fail-closed, evidence-scoped compatibility assessment process for the Product Model, future distributable skill contracts, workflow contracts, machine formats and durable project data. Use a repository-local Python 3.12, file-based, read-only assessor fed by declared supported baselines and explicit consumer dependencies. Separate structural findings from behavioral review, migration disposition and deprecation status. Avoid publishing or altering existing product semantics as a side effect of planning (US1–US6, FR-001–032).

## Technical Context

- **Language/Version:** Python 3.12 (existing GitHub Actions baseline); JSON Schema draft 2020-12 and YAML manifests as existing formats; human-facing policy and examples in English Markdown.
- **Primary Dependencies:** Python standard library for JSON/argparse/pathlib/hashlib/subprocess; existing pinned `PyYAML==6.0.2` and existing safe duplicate-key YAML loader for manifests; no new service or database.
- **Storage:** Versioned repository files and fixture snapshots; generated JSON diagnostics; no server-side persistence. User project-state migrations must operate on explicit opt-in local inputs, never during read-only checking.
- **Testing:** `unittest` negative/positive fixtures, existing `scripts/validate_repo.py`, `scripts/verify_skill_registry_release.py` and registry test families; CI smoke after implementation. Runtime migrations require isolated temporary project directories and double-run/failure injection.
- **Target Platform:** Local Windows and Linux CI; CLI must normalize filesystem paths and use deterministic UTF-8 JSON.
- **Project Type:** Repository contracts + offline CLI validation; no web UI/API.
- **Performance/Scale:** One repository checkout and explicitly declared supported baselines; deterministic finite graph traversal; avoid scanning unknown external integrations. Set measurable runtime budget after initial fixture/profile baseline; no invented benchmark.
- **Constraints:** Read-only default, no network dependency, canonical authority preserved, unknown means unassessed, stable evidence tied to source revision, no implicit publication or retroactive rewrite, no circular dependency acceptance.
- **Scope:** Model `model/product-model.json`; `skills/**/{manifest.yaml,SKILL.md}` (currently no distributable skills); `workflows/**/workflow.yaml` (currently none published); `schemas/*.schema.json`; persisted `.product-pro-max/` artifacts/templates. Existing `registry/skills.json.registry_version=1` and `skills-lock.json.version=1` are format markers, not component versions.

## Constitution Check

**Pre-design:** PASS (design intent). Evidence boundaries, preservation of gate vs decision, canonical Product Model/Skill Model ownership, English machine IDs, minimal surface area, and no promotion of planned truth follow the constitution.

**Post-design:** PASS (design consistency only). No business behavior/ontology rewrite; projections remain derived; CI verdict is not Product Model gate or a publication state; incomplete assessments are non-green. Implementation/runtime compliance remains pending; missing local runtime-verification skill must be synced before downstream tasks.

## Project Structure

### Feature documents (this planning stage)

```text
specs/004-versioning-compatibility/
  spec.md
  .modeling-state.json
  modeling-acceptance.md
  spec-diagram/compatibility-assessment.html
  plan.md                 # this document
  research.md             # choices, alternatives and repository inventory
  data-model.md           # planned data entities/constraints
  contracts/
    compatibility-assessment.md
  quickstart.md           # planned validation; not runnable proof yet
  tasks.md                # NOT created by Plan
```

### Proposed implementation locations (NOT created in Plan)

```text
VERSIONING.md                         # authoritative human policy
compatibility/
  supported-baselines.json            # declared support ledger; no inferred releases
  migrations/                          # opt-in migration descriptors/scripts, if required
schemas/
  compatibility-assessment.schema.json
  supported-baselines.schema.json
scripts/
  check_compatibility.py              # read-only status/report CLI
  compatibility_common.py             # parsing, comparison, graph checks
tests/
  test_compatibility*.py
  fixtures/compatibility/{positive,negative,migration}/
.github/workflows/validate.yml        # add checker gate after fixture proof
SKILL-MODEL.md, SKILL-CONTRACT.md      # later promoted contract updates
PRODUCT-MODEL.md, docs/ARCHITECTURE.md, QUALITY-GATES.md, CONTRIBUTING.md
```

**Structure decision:** Extend Python and repository file-contract patterns; do not introduce a service, release automation, independent registry authority or new Product Model.

## Architectural Boundaries

1. **Authority map:** `model/product-model.json.model_version` owns model version; sibling `SKILL.md` owns skill behavior and `manifest.yaml` owns metadata/version once explicitly migrated; `workflow.yaml.version` owns future workflow versions; a schema's canonical `$id` + a separately declared contract version in the support ledger identify a machine format until its source has a stable version marker; persisted project data gets an explicit `contract_version` via opt-in migration. A support ledger records *policy/support/evidence*, never edits or overrides owning artifacts.
2. **Component inventory:** Assign stable identities for model, skill, workflow, schema and project data. Do not map repo SHA, generated registry projection, lockfile, or design tokens to skill behavior versions.
3. **Declared baseline:** Compare candidate to an immutable `ref+path+digest` with explicit supported consumer scope and support state; no baseline or missing historical blob => `unassessed`, not compatible. First version and pre-1.0 follow explicit policy (see research).
4. **Assessment pipeline:** validate snapshot provenance → extract canonical components → validate references and version constraints → perform deterministic structural diffs + strict-reader scenarios → require reviewer evidence for semantics/behavior → attach migration/deprecation disposition → determine verdict. Static-compatible findings cannot claim behavioral/runtime proof.
5. **Consumer edges:** model → schemas/templates/workflows; skills → dependent skills/workflows; schema/format → strict readers and project-state writers/readers; project-state → persisted user artifacts and future Spec 009. Unknown external consumers remain outside declared coverage and visible.
6. **Compatibility outcome:** `compatible | breaking | review_required | unassessed`; CI disposition `allow | block | review` independent of Product Model `pass|warn|fail` gates. Breaking + inadequate version bump/missing mandatory migration => block; unresolved required review/unknown baseline => non-green review result (fail CI until handled).
7. **Migration:** Dry-run/preflight first; enumerate input versions and consumers; backup/copy-on-write/checkpoint/receipt; preserve evidence provenance and decision history; detect interrupted/duplicate application; no destructive rewrite or implicit `generate` side effects. An unsupported legacy input cannot silently be coerced.
8. **Deprecation:** `active → deprecated → unsupported → removed` with explicit policy-boundary and exception review; deprecation is not removal; no release tag/changelog generation (Spec 008).
9. **Rollout:** Stage legacy-aware readers/diagnostics before adding strict skill `version` and project `contract_version` requirements. Registry remains generated from manifests, and unknown manifest fields currently reject: expand parser/contract + negative fixtures first; avoid first-time mass edits and no fictitious releases.

## Phase 0 — Research

See [research.md](research.md). Records decisions and rejected alternatives about version ownership, baseline support, strict readers, pre-1.0, offline checking, SemVer scope, failure-safe migrations and evidence.

## Phase 1 — Design Contracts

- [data-model.md](data-model.md): component, supported baseline, consumer dependency, assessment and diagnostic, migration and deprecation schemas/invariants.
- [contracts/compatibility-assessment.md](contracts/compatibility-assessment.md): CLI command/result examples, classification/exit semantics, migration and status transitions.
- [quickstart.md](quickstart.md): planned reproducible validation matrix and evidence checklist, explicitly not executable yet.

## Runtime Risk Design

**Catalog source:** reviewed `sonhoang23/oh-my-skill@main:skills/runtime-verification` v1.12.0, `references/lifecycle-profile.md`, `catalog-index.md`, relevant `environment.md` and `verification-tooling.md`. The consumer path `.agents/skills/runtime-verification/SKILL.md` is now **PRESENT**, synced from canonical `oh-my-skill` at commit `fcd9a5b8db9c37673b9bb92d69bf6056af30ec3a` (v1.12.0). Design inventory below was rechecked against installed `lifecycle-profile.md`, `catalog-index.md`, `environment.md`, and `verification-tooling.md`. This is a read-only design-mode evaluation, **not** runtime execution or acceptance.

| Risk ID | Status | Requirement refs | Evidence/trigger | Prevention design | Verification strategy |
|---|---|---|---|---|---|
| ENV-003 | APPLIES | FR-025–028; N/A — CLI technical boundary | Local Windows + Linux CI, path-specific diagnostics and baseline traversal | Normalize paths with pathlib and POSIX relative report paths; never compare OS-native separator strings | Fixtures with Windows-style and POSIX-style paths; CLI diagnostics stable across target OS |
| VERIFY-003 | APPLIES | FR-007–008, FR-027–029 | Assessment evidence can outlive baseline/candidate revision | Bind evidence to base commit, source digest, candidate commit and file set; stale/dirty tree blocks verified claims; recompute on affected changes | Mutate source after a recorded pass; demand stale/review verdict and refreshed proof |
| VERIFY-008 | APPLIES | FR-024–028 | Multi-step fixtures must create valid baseline/consumers before checking impact | Assert fixture preconditions (valid source, IDs, references and support ledger) before asserting downstream diff | Malformed prerequisite fails at setup boundary with root-cause path |
| VERIFY-004 | APPLIES | FR-025–027 | CLI/test commands may exit 0 but still emit unexpected contract/parser warnings | Explicit diagnostic taxonomy; unexpected warnings in scoped checks prevent clean verified-compatible CI verdict | Inject unexpected parser/consumer warnings; assert non-green result and recorded reason |
| API-001 | NOT_APPLICABLE | N/A — architecture boundary | No OpenAPI/service runtime-generated client is used in this feature | Registry is static manifest projection; test its own drift separately, not via API process-revision pattern | Architecture/entrypoint audit |
| DB-002 | NOT_APPLICABLE | N/A — architecture boundary | Planned migration is file-based, without DB migration journal/SQL chain | Use file preflight/atomic replace/receipts, not database migration tooling | Architecture/fixture audit |
| STARTUP-001 | NOT_APPLICABLE | N/A — architecture boundary | No server process/port is part of this offline checker | Require locally pinned files/refs, no endpoint probing | CLI help/dependency audit |

**Feature-specific risks (not canonical catalog IDs):** strict YAML unknown-field rejection during version-field rollout; closed-enum additivity; human semantic approval incorrectly treated as machine-proof; migration interrupted after file replacement; absent externally deployed consumer inventory; conflicting support lifecycle and version range. Each has a named fixture/negative path in the contract and quickstart.

**Catalog freshness condition:** local canonical consumer copy was synced before Tasks (16 files); before task generation check its installed version/source and re-evaluate false-N/A, preserving canonical Risk IDs. No `NEEDS_UPSTREAM` domain ambiguity identified in Spec 004; missing **local tooling** is recorded as downstream prerequisite rather than invented requirements.

## Verification and evidence gates (planned, not run)

1. Structural schema/manifest/workflow/project-state and version precedence fixtures.
2. Semantic diff review-required for gates/decisions, skill stopping rules or contract meaning with unchanged syntax.
3. Consumer dependency/range graph, strict enum/field readers, missing/unknown baseline/consumer fixtures.
4. Migration dry-run, provenance/history preservation, repeat, interrupted write, rollback/irreversibility and legacy data fixtures.
5. Diagnostic content, machine-readable report, status transitions and non-green CI failures for unknown evidence.
6. Full repository validation, affected tests and CI on final revision. Track invocation, target, revision, exit, fixture counts, warning classification. No current PASS claimed.

## Project Docs Promotion Plan

After implementation plus relevant static/runtime evidence and fresh implementation modeling: promote policy to `VERSIONING.md`, update `PRODUCT-MODEL.md`, `SKILL-MODEL.md`, `SKILL-CONTRACT.md`, `QUALITY-GATES.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, then `README.md`/`README.vi.md` for discovery as appropriate. Review `schemas/`, `templates/`, `workflows/` for actual contract impact. Run Diagram Check for any material architecture diagram update. **No project-level docs or diagrams modified by Plan.**

## Boundaries and sequencing

- Spec 001/002 contracts remain authoritative; Spec 003 design is unrelated; Spec 009 is future consumer.
- This spec implements compatibility policy/checker only. Spec 005 owns broad evals; Spec 006 owns governance/reviewer workflow; Spec 008 owns release/tag/changelog automation.
- **Before Tasks:** local `runtime-verification` is synced and design risk inventory rechecked; ensure Plan Modeling Gate via `speckit-system-modeling-vi`, then create tasks and analyze. No claim of having invoked a filesystem-local script or of implementation evidence.
- No implementation or CI execution is claimed by these artifacts.
