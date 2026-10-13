# Versioning and Compatibility Policy

**Status (2026-10-13):** Component-version ownership, SemVer parsing and legacy manifest reading are implemented in Spec 004 US1. A compatibility assessor, support-baseline gate, migrations, deprecation enforcement, publishing and release automation **are not implemented**. Do not treat this policy as a claim of runtime compatibility or published skill releases.

## Version authorities

| Surface | Canonical version source | Scope |
|---|---|---|
| Product Model | `model/product-model.json.model_version` | Lifecycle IDs, relations and gate-vs-decision meanings |
| Distributable skill | `skills/<cycle>/<id>/manifest.yaml.version` when declared | `SKILL.md` retains *behavior* authority, `manifest.yaml` owns metadata/version |
| Workflow | `workflows/<id>/workflow.yaml.version` when present | Workflow orchestration contract; no published executable workflows currently |
| Machine schema/format | Canonical `$id` + explicitly declared support-ledger version | Source schema content and known reader constraints; not automatically inferred from a schema filename |
| Persisted project data | `contract_version` when explicitly introduced | Legacy-unversioned input stays detectable; opt-in migration remains future work |

**Never substitute** Git SHA, registry projection `registry_version`, `skills-lock.json.version`, presentation token revisions or README edits for another component's contract version. Components change version independently.

## Stable SemVer

For stable components, use `MAJOR.MINOR.PATCH` (with SemVer 2.0.0 optional prerelease/build identifiers):
- **MAJOR:** incompatible change to a supported public contract.
- **MINOR:** independently assessed, backward-compatible capability addition.
- **PATCH:** independently assessed behavior-preserving correction.
- A breaking, feature and fix change together require the highest applicable increment.
- A version string alone never proves behavioral equivalence; strict readers may break on additive enums/fields.
- Build metadata does not change SemVer precedence and is not a public-version increment.

For `0.y.z`, incompatible change requires **at least a MINOR boundary** plus explicit consumer notice/support and migration disposition where relevant; new compatible capability uses MINOR; a correction uses PATCH. Pre-1.0 is not blanket permission to reuse old `0.y.z` semantics silently. Moving to `1.0.0` establishes a new stable promise only after reviewed contract, supported scope and evidence.

## First version and supported baselines

The first version is an **identity assignment**, not a successful backward-compatibility comparison. The checker may assert compatibility only against an explicitly declared supported historical baseline with immutable Git commit/source path/SHA-256, component identity, support status and consumer scope. An absent/unresolved source, unknown reader tolerance or unassessed semantics means `unassessed` or `review_required`, never auto-green.

The source ledger is intended at `compatibility/supported-baselines.json`; its current `baselines: []` is honest. It does not publish anything. `model_version: 1.0.0` does not imply a released skill. No distributable skills are currently published.

## Read-only comparison versus compatibility verdict

Implemented today: parse and order versions, recommend/check a version increment from an already-reviewed impact, inspect source-owned version metadata, validate local immutable Git-baseline provenance. **Not implemented:** structural/semantic impact classification, known-consumer graph, product compatibility gate, migration executor, behavioral/runtime proof and release lifecycle. A sufficiently bumped MAJOR may still represent **breaking** behavior and cannot be relabeled `compatible`.

Future independent compatibility outcomes: `compatible | breaking | review_required | unassessed`; CI dispositions: `allow | block | review`. These are **not** Product Model gate results `pass | warn | fail`, workflow decisions or publication status.

## Migration and deprecation (policy, not commands)

Stored project data and evidence/decision history must remain readable under a supported contract or obtain an explicit reviewable migration disposition. Future migration requires opt-in source/target versions, preflight, dry-run, backup/recovery, idempotence receipts and history/provenance checks; a checker must not auto-rewrite existing project state. Support states `active → deprecated → unsupported → removed` require declared affected scope, support window, replacement or explicit absence, migration guidance and removal prerequisites. Security exceptions require recorded authority/mitigation and retain the breaking classification. No release/tag/changelog automation here (Spec 008).

## Verification evidence boundary

Implementation/testing/checked/runtime/migrated-in-test/published are separate. Re-evaluate evidence against the exact final revision and known consumers. `specs/004-versioning-compatibility/verification.md` records concrete test/CI evidence. Future Spec 005 evaluation and Spec 006 governance are separate authorities.
