# Compatibility Assessment — Planned External Contract

**Status:** planned design interface, NOT a working CLI or shipped schema.
**Authority:** [spec.md](../spec.md), [data-model.md](../data-model.md). Examples here are synthetic fixtures, NOT repository release records.

## 1. Scope and source-of-truth

The checker **reads** canonical component and consumer sources. It never writes Product Model, SKILL.md, manifest.yaml, workflow definitions, schemas, registry, lockfiles or user projects while assessing.

| Component | Identity/version source | Compatibility authority |
|---|---|---|
| Product Model | `model/product-model.json: model_version` | Model file + dependent consumers/schemas |
| Skill | `manifest.yaml: id, version` once rolled out | `SKILL.md` behavior, manifest metadata, support policy |
| Workflow | `workflow.yaml: name, version` when published | Workflow's orchestration definition |
| Schema format | `$id` + support-ledger declared contract version | Tracked JSON Schema and strict readers |
| Durable project data | Explicit stored `contract_version` after migration | Project/evidence/decision schemas and source artifacts |

`registry/skills.json` is derived; `skills-lock.json.version` and `registry_version` remain serialization markers. The support ledger records recognized baseline snapshots and support declarations, but must not redefine source-owned behavior or silently create a release.

## 2. Proposed CLI

```shell
# Planned; not runnable until implementation.
python scripts/check_compatibility.py assess \
  --baseline-ledger compatibility/supported-baselines.json \
  --baseline-id model-v1-supported-fixture \
  --candidate-ref HEAD \
  --report-json .tmp-compatibility/report.json
```

Arguments: `assess` subcommand; required ledger, baseline ID and candidate/ref source; optional report output. An explicit alternative `--candidate-root` may allow an isolated fixture directory. No auto-install/network fetch. If a ref or digest is missing, report cannot assert compatible. Assess does not mutate inputs; temporary reports are written only to the user-supplied report destination with deterministic ordering.

**Exit-code contract (planned):**

| Exit | Meaning | CI interpretation |
|---|---|---|
| 0 | `allow`: defined supported-scope checks and required reviews satisfied | Eligible to pass this gate; not runtime/release evidence |
| 1 | `block`: definite incompatibility without sufficient version/migration disposition or other policy violation | Fail |
| 2 | `review`: review-required, incomplete/missing baseline or required consumer facts, unknown behavior | Non-green; do not pretend compatible |
| 3 | Tool/input error: malformed ledger, corrupted artifact, invalid CLI or unreadable checkout | Non-green; distinguish infrastructure/input failure |

A sufficiently bumped MAJOR may correctly describe a **breaking** change but cannot automatically convert it into `compatible`. It can proceed only with explicit policy-covered consumer disposition, migration obligations and review evidence. `review` is not a Product Model `warn` gate.

## 3. Baseline-ledger shape (synthetic fixture)

```json
{
  "ledger_version": 1,
  "policy_ref": "VERSIONING.md",
  "baselines": [
    {
      "baseline_id": "model-v1-supported-fixture",
      "component_id": "product-model",
      "version": "1.0.0",
      "source": {
        "ref": "fixture-base",
        "commit_sha": "0000000000000000000000000000000000000000",
        "authority_path": "model/product-model.json",
        "sha256": "fixture-placeholder-not-valid-digest"
      },
      "support_status": "active",
      "support_scope": ["fixture:strict-project-state-reader"],
      "support_policy_ref": "fixtures/compatibility/policy.md",
      "release_evidence": null
    }
  ]
}
```

This illustrative fixture deliberately uses dummy SHA/hash placeholders; a real validator **must reject** it until fixtures supply valid pinned values. The live repo currently has **no declared published skill baseline**. Product Model `model_version: 1.0.0` is not alone proof of a published, supported release.

## 4. Assessment report shape (synthetic example)

```json
{
  "assessment_id": "fixture-assessment-001",
  "checker_revision": "fixture-revision",
  "policy_version": "draft",
  "baseline": {
    "component_id": "product-model",
    "version": "1.0.0",
    "commit_sha": "fixture-base",
    "sha256": "fixture-hash"
  },
  "candidate": {
    "component_id": "product-model",
    "version": "1.1.0",
    "commit_sha": "fixture-candidate",
    "sha256": "fixture-candidate-hash"
  },
  "covered_consumers": ["fixture:closed-enum-reader"],
  "unassessed_consumers": [],
  "findings": [
    {
      "code": "STRICT_READER_NEW_ENUM",
      "severity": "error",
      "component_id": "product-model",
      "baseline_version": "1.0.0",
      "candidate_version": "1.1.0",
      "authority_path": "model/product-model.json",
      "json_pointer": "/gates/results",
      "affected_consumer_ids": ["fixture:closed-enum-reader"],
      "classification": "breaking",
      "message": "New enum member is not accepted by declared exhaustive consumer",
      "required_action": "Use a breaking-version boundary and declare consumer upgrade/migration"
    }
  ],
  "classification": "breaking",
  "required_bump": "major",
  "version_check": "insufficient",
  "migration_disposition": null,
  "evidence_levels": ["policy_defined", "static_checked"],
  "verdict": "block"
}
```

The report is deterministic for identical source + policy + checker. Wall-clock timestamp (if any) is display-only and excluded from content digest. Actual JSON Schema validation and checker output are implementation obligations; this is a planned contract, not observed output.

## 5. Decision table

| Evaluated change | Known consumer result | Classification | Minimum handling |
|---|---|---|---|
| Stable behavior-preserving correction | Verified old required behavior holds | compatible | PATCH; scope/evidence required |
| Compatible optional feature | Readers explicitly tolerant and behavior verified | compatible | MINOR |
| Required output removed/renamed | Known reader depends on it | breaking | MAJOR for stable + migration/dependency disposition |
| Enum member added | Strict exhaustive reader | breaking | Breaking boundary, reader migration |
| Required manifest key added | Old strict manifest reader rejects | breaking | Reader expansion/legacy handling before writer rollout |
| Behavior or evidence threshold changed, same file shape | No behavioral equivalence proof | review_required | Human review and relevant behavior tests |
| Missing or unknown baseline | Cannot anchor comparison | unassessed | Declare baseline/evidence; never compatible |
| Unknown external consumers | Out of assessment scope | unassessed for those consumers | State limited coverage; do not claim universal compatibility |
| Correct MAJOR but unresolved project-data migration | Known break remains | breaking | Block until disposition and safety obligations met |
| Pre-1.0 incompatible change | Prior declared support exists | breaking | At least MINOR boundary + notice and explicit migration/reader assessment |
| Initial version, no previous supported baseline | No comparison possible | unassessed | May assign initial version; do not claim backward compatibility |

## 6. Diagnostic requirements

Each violation must include: component stable ID, old/new version, source path or JSON pointer, offending condition, affected known consumers, current classification and next safe action. If unknown, identify which baseline/consumer/behavior evidence is missing. Do not emit an unqualified "All compatible" when any required evidence remains unassessed. Invalid YAML must preserve duplicate-key/unsafe-tag failures from canonical reader.

Dependency graph tests: invalid SemVer constraints, missing/unknown targets, cycles, conflicting ranges, unsupported versions and stale registry projections all have distinct diagnostics. Generated registry itself stays read-only and must be checked by existing registry validation, not promoted to a versioning authority.

## 7. Migration interface and transactional safety

**Assessment command:** Read-only. Emits `migration_required` diagnostic and references a planned migration descriptor; does not execute migration.

**Future migration CLI:** Only an explicit subcommand with input path/source/target and requested action may transform user-owned files; default `dry-run`. Preflight enumerates affected records and expected transforms; execution requires valid backup/restore or documented irreversible exception. Record stable `migration_id` + input digest and receipt in an explicit output location. On repeat, validate existing receipt/output and no-op; do not double-apply. On partial failure, preserve untouched originals where possible and report exact failed records/recovery procedure. Never invent provenance, collapse assumptions into confirmed evidence or discard decision history.

Synthetic cases to cover: legacy no-version input, missing record, mixed two supported versions, interrupted write, second run, out-of-order step, dangling reference, changed digest after preflight, manual/irreversible exception, partial recovery.

## 8. Deprecation notice and removal preconditions

A machine-readable deprecation notice must identify: component/field identity, first affected version, `active | deprecated | unsupported | removed`, replacement or explicit no replacement, current support window, known impacted consumers, migration requirements and earliest permissible removal. A removal without fulfilled prerequisites is blocked or handled through an explicitly approved emergency exception. The exception never changes `breaking` classification to `compatible`.

## 9. Evidence levels and interface stability

Reports distinguish policy defined, structural/static check, behavioral test, migration-in-test, real runtime verification and publication. Never promote a level without its own revision-bound evidence. A green static CLI result is not user project migration success, skill execution success or a release. The checker must not publish tags, changelogs or release notes.

**Integration after implementation:** Existing `scripts/validate_repo.py`, registry integrity checker, CI workflow and selected documents may reference the checker only after their own tests are confirmed. Spec 005 evals, Spec 006 approvals and Spec 008 releases remain separate.
