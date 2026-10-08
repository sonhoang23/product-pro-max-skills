# Skill Registry Requirements Checklist: Skill Manifest Registry

**Purpose**: Review the completeness, clarity, consistency, measurability and scenario coverage of Spec 002 requirements and planned contracts before task breakdown.
**Created**: 2026-10-08
**Feature**: [spec.md](../spec.md)
**Review ownership**: Reviewer-owned. An `[x]` indicates that the requirement-quality criterion has been reviewed and satisfied, **not** that implementation is complete.
**Scope**: Standard-depth author/reviewer quality gate covering canonical identity, metadata authority, Product Model references, registry integrity, migration and authoring. Does not validate implementation or runtime behavior.

## Requirement Completeness

- [ ] CHK001 Is the division of authority between Skill Model, Skill Contract, SKILL.md, manifest.yaml and generated registry explicitly defined without competing sources? [Completeness, Spec §FR-001–004, FR-024]
- [ ] CHK002 Are every mandatory discovery field and its semantic purpose specified for both per-skill manifests and aggregate registry entries? [Completeness, Spec §FR-013–016, FR-025]
- [ ] CHK003 Are positive and negative trigger descriptors sufficiently specified for agents to distinguish eligible use from exclusions? [Completeness, Spec §FR-014]
- [ ] CHK004 Are workflow reference targets and their authoritative inventory/location identified sufficiently to resolve every declared workflow relationship? [Gap, Spec §FR-021–022]
- [ ] CHK005 Are gate/decision output semantics explicitly constrained to the Spec 001 Product Model rather than defined afresh in skill metadata? [Completeness, Spec §FR-017]
- [ ] CHK006 Is the required behavior of skill-creator-vi defined for both new and updated distributable skills, including how violations are surfaced? [Completeness, Spec §FR-028–029]

## Requirement Clarity

- [ ] CHK007 Are namespace, slug, ID prefix and canonical filesystem path rules precise enough to reject ambiguous or colliding skill identities? [Clarity, Spec §FR-005–009]
- [ ] CHK008 Are the differences between primary_cycle and broader lifecycle associations clear, including phase ownership and cross-cutting tracks? [Clarity, Spec §FR-008–012]
- [ ] CHK009 Are required versus optional inputs and output semantic descriptors objectively distinguishable from informal prose? [Clarity, Spec §FR-015–017]
- [ ] CHK010 Are the controlled skill relation types and direction of each relationship defined without ambiguity? [Clarity, Spec §FR-018–020]
- [ ] CHK011 Are workflow relationship roles discovery-only and clearly separated from execution ordering or orchestration authority? [Clarity, Spec §FR-021–022]
- [ ] CHK012 Does the contract distinguish an empty valid collection from missing, malformed or semantically incomplete required manifest metadata? [Gap, Spec §FR-003, FR-026]

## Requirement Consistency

- [ ] CHK013 Do spec, plan, data-model and manifest/registry contract agree on field names, shapes, identity conventions, lifecycle semantics and registry authority? [Consistency, Spec §FR-003–012, FR-023–025]
- [ ] CHK014 Do registered lifecycle associations consistently resolve to canonical Product Model cycle, phase and track IDs, preserving phase/cycle ownership? [Consistency, Spec §FR-012]
- [ ] CHK015 Are the definition and handling of self-links, duplicate relationships and contradictory relations consistent between edge cases and the planned contract? [Consistency, Spec §FR-018–020]
- [ ] CHK016 Are all planned technical choices clearly marked as design decisions rather than silently introduced normative product requirements? [Consistency, Spec §FR-032]
- [ ] CHK017 Do the feature's migration requirements preserve trigger intent, evidence rules, outputs and behavioral responsibility without conflicting with the new naming rules? [Consistency, Spec §FR-030–031]

## Acceptance Criteria Quality

- [ ] CHK018 Are the 100% identity, coverage, reference and metadata criteria objectively measurable against a defined canonical skill inventory? [Measurability, Spec §SC-001–007]
- [ ] CHK019 Does the failure-detection criterion enumerate representative invalid fixtures with an unambiguous fail outcome and identifiable reason? [Measurability, Spec §SC-008, FR-026]
- [ ] CHK020 Is read-only registry drift detection defined separately from write/generation, so checking cannot silently repair incorrect derived state? [Measurability, Spec §FR-023–026]
- [ ] CHK021 Are migration semantic-parity outcomes and their permissible exceptions traceable enough for independent review? [Measurability, Spec §SC-011, FR-030–031]

## Scenario & Edge Case Coverage

- [ ] CHK022 Are ordinary discovery, multi-lifecycle discovery, authoring and registry regeneration scenarios covered without requiring consumers to inspect every SKILL.md? [Coverage, Spec §User Stories 1–5]
- [ ] CHK023 Are invalid YAML, duplicate mapping keys, absent manifest/frontmatter, identity mismatches and duplicate IDs explicitly covered by rejection requirements? [Coverage, Spec §FR-026]
- [ ] CHK024 Are unresolved skill/workflow references, invalid Product Model references, wrong cycle/phase pairings and non-canonical relations covered? [Coverage, Spec §FR-012, FR-020–022, FR-026]
- [ ] CHK025 Are partial/failed registry generation and recovery expectations defined so invalid input cannot replace the last valid derived artifact? [Gap, Spec §FR-024–026; Plan §Runtime Risk Design SR-04]
- [ ] CHK026 Are stale or directly edited registries and missing/extra canonical directories included in drift/coverage requirements? [Coverage, Spec §FR-023–026]
- [ ] CHK027 Are the legacy flat-skill migration and exclusion of similarly named .agents/ development tooling expressly addressed? [Coverage, Spec §FR-028–031]

## Non-Functional, Dependencies & Scope

- [ ] CHK028 Are deterministic ordering, stable serialization and cross-platform machine ID expectations precise enough to reproduce derived registry output? [Measurability, Spec §FR-006, FR-023–027]
- [ ] CHK029 Is the trust boundary for manifest parsing and canonical reference resolution clear without committing to an unnecessary implementation stack in the spec? [Clarity, Spec §FR-003, FR-026]
- [ ] CHK030 Is Spec 001 clearly authoritative for product lifecycle/gate/decision concepts while Specs 003–007 retain their stated ownership of deferred versioning, eval, governance, catalog and release features? [Dependency, Spec §FR-012, FR-017, FR-032]
- [ ] CHK031 Are English machine identifiers and localized presentation separated so translations cannot create alternate canonical IDs? [Consistency, Spec §FR-027]
- [ ] CHK032 Are planned-truth assertions separated from implementation/runtime evidence and are missing verification steps left visible rather than labeled PASS? [Assumption, Constitution §§I–II, VII, XII]

## Review notes

- All 32 items intentionally remain unchecked until reviewer evaluation; creating a checklist does not establish PASS.
- The existing [requirements.md](requirements.md) is the specify-stage checklist and is not modified here.
- Potential review focus: workflow authority inventory (CHK004), empty-versus-missing metadata (CHK012), contradictory relation semantics (CHK015), failure recovery (CHK025) and deterministic encoding (CHK028).
- The plan's SR-01 through SR-06 are **feature-local risk IDs**, not certified runtime-verification catalog identifiers.
- The implementation command reads checklist state as a gate but must not change reviewer-owned markers. No tasks, analyze or implementation was performed.
