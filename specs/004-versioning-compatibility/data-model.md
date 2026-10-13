# Data Model — Versioning & Compatibility

**Status:** planned technical contract, not an implemented data store. **Authority:** [spec.md](spec.md), [plan.md](plan.md), existing Product/Skill Model. All persisted machine identifiers are English/ASCII.

## 1. VersionedComponent

Stable identity and version authority for each independently consumable surface.

| Field | Type | Rule |
|---|---|---|
| `component_id` | string | Globally unique within compatibility scope; stable across compatible versions; examples: `product-model`, `skill:ppmax-example`, `workflow:idea-to-mvp`, `schema:project-state`, `project-data:project-state` |
| `component_type` | enum | `product_model`, `skill`, `workflow`, `machine_schema`, `project_data` |
| `authority_path` | repository-relative path | Path to owning semantics; does not create another source of truth |
| `version_owner` | string | e.g. `model_version`, `manifest.version`, `workflow.version`, declared schema support-ledger version, `contract_version` for migrated data |
| `version` | SemVer string or null | Null only for legacy/unversioned input, never treated as proven latest |
| `format_version` | string or integer, optional | Serialization marker independent of component SemVer |
| `digest` | SHA-256 hex | File-content integrity; revision alone not behavioral evidence |
| `publication_status` | enum | `unpublished`, `published`, `unknown`; never inferred from version alone |

**Invariants:** Identity is not a folder label; a moved path with stable identity must still assess dependent references. A format marker (`registry_version`, lock `version`) cannot silently become a semantic skill version. Product Model owns gate/decision meanings. No custom lifecycle IDs are introduced by versioning.

## 2. SupportedBaseline

Explicit support ledger entry, proposed in `compatibility/supported-baselines.json`.

| Field | Type | Rule |
|---|---|---|
| `baseline_id` | string | Stable unique immutable reference identity |
| `component_id` | string | References a declared component |
| `version` | SemVer string | Supported historical contract version |
| `source` | object | `{ref, commit_sha, authority_path, sha256}`; immutable committed source preferred |
| `support_status` | enum | `active`, `deprecated`, `unsupported`, `removed` |
| `support_scope` | array | Declared consumer identities/capabilities/constraints; no universal claims |
| `support_policy_ref` | string | Link to actual owner-approved support policy, not an automatic CI claim |
| `effective_from`, `effective_until` | nullable strings | Explicit support window when policy declares it |
| `release_evidence` | nullable object | Proof of publication if published; null otherwise |
| `record_revision` | commit/digest | Evidence record must be traceable and reviewable |

**Invariants:** Empty ledger is valid; cannot assert compatible against missing baseline. Baseline source must exist, resolve to a valid component and match digest. Unsupported/removed cannot be silently used as an active support promise. Lack of publication proof cannot become published. A changed ledger record must not retrospectively relabel previously published evidence.

## 3. ConsumerDependency

Directed edge from consumer to provider.

| Field | Type | Rule |
|---|---|---|
| `consumer_id` | string | Known internal skill/workflow/schema/client/data reader or explicit external known dependency |
| `provider_component_id` | string | Stable referenced component ID |
| `range` | string or null | Explicit accepted version range; null means unknown, not “any” |
| `required_outputs` | string[] | Semantic output names/contract expectations |
| `required_features` | string[] | Features or behavior promises required by consumer |
| `strict_reader` | boolean or `unknown` | Whether unknown fields/enum members are rejected |
| `declared_by` | path/reference | Authoritative consumer source, not derived registry authority |
| `scope` | string | Documented covered usage/baseline (e.g. parser, workflow, project data) |

**Invariants:** Missing provider, dependency loop, invalid range, unknown reader tolerance or unknown external consumer is reported with coverage limits. A valid range is not proof that semantic behavior still works. Registry entries remain read-only projections.

## 4. ProposedChange

A comparison target; not a mutated authoritative artifact.

| Field | Type | Rule |
|---|---|---|
| `component_id` | string | Stable identity |
| `baseline_id` | string or null | Explicit supported baseline; null produces unassessed |
| `candidate_source` | object | ref/path/hash, including dirty-checkout marker if needed |
| `candidate_version` | SemVer string or null | Proposed increment, independently assessed |
| `changed_surfaces` | string[] | Paths/fields/output and semantic promises under assessment |
| `review_evidence` | array | Concrete behavioral/semantic proof links or pending review |

No tool may silently rewrite source artifacts just because a comparison reports breakage.

## 5. CompatibilityAssessment

Emitted by planned read-only CLI.

| Field | Type | Rule |
|---|---|---|
| `assessment_id` | string | Stable report identity derived from pinned inputs/assessment config |
| `checker_revision` | ref/digest | Exact validator implementation revision |
| `policy_version` | string | Version of assessed policy |
| `baseline`, `candidate` | objects | Same component ID, explicit versions and source provenance |
| `covered_consumers` | array | Known consumer identities evaluated |
| `unassessed_consumers` | array | Unknown/external/unresolved consumer scopes stated explicitly |
| `findings` | array | Diagnostics with severity, path, rule, affected consumers, suggested next action |
| `classification` | enum | `compatible`, `breaking`, `review_required`, `unassessed` |
| `required_bump` | enum or null | `patch`, `minor`, `major`; null for no/baseline-unknown recommendation |
| `version_check` | enum | `sufficient`, `insufficient`, `not_assessable` |
| `migration_disposition` | reference or null | Explicit migration outcome when required |
| `evidence_levels` | array | `policy_defined`, `static_checked`, `behavior_tested`, `migrated_in_test`, `runtime_verified`, `published`; independent claims with references |
| `verdict` | enum | `allow`, `review`, `block` — independent of Product Model gate results |
| `generated_at` | optional timestamp | Display metadata only, excluded from deterministic content digest |

**Classification rules:** `breaking` if a known supported consumer breaks; `review_required` if structural checks are insufficient to assert behavior; `unassessed` if required baseline/dependency/coverage facts are absent. Mixed results use conservative priority: known breaking cannot be hidden by review/unknown; missing required coverage makes overall verdict non-green even if local structural checks pass. `compatible` requires assessed scope and adequate evidence. A known breaking change with a correctly bumped MAJOR is still a breaking classification; it may proceed only with fulfilled migration/deprecation/support obligations and appropriate review, never relabeled compatible.

## 6. Diagnostic

Each finding is actionable and machine-readable:

`{code, severity, component_id, baseline_version, candidate_version, authority_path, json_pointer?, affected_consumer_ids, classification, message, required_action, evidence_ref?}`

Severity is `error | warning | info`. Do not use Product Model gate result enum for compatibility classification.

## 7. MigrationDisposition

| Field | Type | Rule |
|---|---|---|
| `migration_id` | string | Stable ID for source → target semantics and implementation |
| `component_id`, `source_version`, `target_version` | strings | Immutable migration pair and owning contract |
| `input_scope` | paths/formats | Enumerated records impacted; absent source is not assumed |
| `preconditions` | array | Validation/checksums/authority prerequisites |
| `transform` | description or script ref | Explicit, reviewable, never auto-executed by checker |
| `postconditions` | array | Canonical integrity, referential preservation and semantic invariants |
| `recovery` | object | Backup/copy-on-write/checkpoint/rollback or approved irreversible manual procedure |
| `history_invariants` | array | Evidence origin, assumptions, decisions, timestamps and provenance remain unaltered semantically |
| `idempotency_key` | string | Stable per input record/source/target and migration ID |
| `exception` | nullable object | Explicit authorized reason, risk, mitigation for irreversibility |

**ExecutionReceipt** (only when a migration is explicitly run in later implementation):
`{migration_id, input_id, original_digest, output_digest?, status, attempted_at, backup_ref?, checkpoint_ref?, errors, recovery_action?}`

Receipt status: `not_started | applied | already_applied | partially_applied | failed | recovered`. Failed/interrupted is never `applied` even if some files changed. Never overwrite the only original evidence copy. A second run either confirms matching output and returns `already_applied` or reports mismatch; it must not duplicate decisions/evidence.

## 8. DeprecationNotice

`{notice_id, component_id, earliest_affected_version, current_support_status, deprecated_since, supported_until?, replacement_component_id?, replacement_absent_reason?, affected_consumers, migration_ref?, removal_preconditions, exception_ref?}`

Transition policy: `active → deprecated → unsupported → removed`; emergency exception requires separately recorded approval, residual risk and consumer mitigation. Versions may coexist. A notice does not itself publish a release or prove successful migration.

## 9. Existing schema impacts and rollout

- `model/product-model.json.model_version` stays source-owned; keep all canonical IDs stable unless change classified and migrated.
- `manifest.yaml`: add version contract only after parser and fixtures recognize new field. `SKILL.md` behavior remains canonical; no duplicate mandatory frontmatter version.
- `workflow.yaml`: existing schema has `version`, but no published instances; do not invent deployment.
- `schemas/*.schema.json`: preserve `$id` and scope schema-compatible changes; allow baseline ledger to record independently meaningful schema contract versions, explicitly tied to hashes.
- `schemas/project-state.schema.json` and `templates/project-state/`: accept legacy-unversioned objects only with explicit legacy classification; include `contract_version` in future outputs via an opt-in, tested rollout. Other durable evidence/decision records retain semantics/history.
- `registry/skills.json` and `skills-lock.json`: maintain existing integer format markers; never bulk-convert to skill SemVer.

## 10. Integrity and traceability

US1 → VersionedComponent/ProposedChange (FR-001–006, FR-031).
US2 → SupportedBaseline/ConsumerDependency/CompatibilityAssessment (FR-007–016, FR-029).
US3 → MigrationDisposition/ExecutionReceipt (FR-017–020).
US4 → CompatibilityAssessment/Diagnostic/Evidence (FR-024–028).
US5 → DeprecationNotice (FR-021–023).
US6 → Support ledger/discovery policy (FR-001, FR-027, FR-029–032).
