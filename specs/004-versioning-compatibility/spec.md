# Feature Specification: Versioning & Compatibility

**Feature Branch**: `main` (specification only; no implementation authorized)
**Created**: 2026-10-10
**Status**: Clarification reviewed (no blocking questions); conceptual Spec Modeling diagram drafted, verification pending; planning, tasks, implementation and runtime verification not started
**Spec modeling (planned truth)**: [Compatibility assessment boundary](spec-diagram/compatibility-assessment.html) · [Feature Diagram Ledger](diagrams.html). Visual is derived from this specification and does not demonstrate an implemented compatibility checker.

**Clarify review (2026-10-10)**: No unanswered behavior/domain question requiring user choice. The supported-baseline policy, strict-reader compatibility, migration safety and evidence distinctions are specified by FR-005, FR-007–FR-009, FR-012–FR-014 and FR-017–FR-029; exact metadata/schema/checker mechanics remain planning decisions. No new user decision was inferred.

**Input**: Approved Spec 004 proposal: define a shared versioning and compatibility policy for Product Model, distributable skills, manifest/registry formats, workflow contracts and durable project data; classify breaking changes, assess dependencies, specify safe migration and deprecation, and make compatibility checks inspectable. Spec 004 defines the contract and policy; subsequent specs own expanded evaluations, governance and releases.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Assign Meaningful Independent Versions (Priority: P1)

As a maintainer, I need to tell what changed and which component's contract changed without treating every repository edit as a new version of every skill.

**Why this priority**: A single repository-wide version hides incompatible changes in separately consumed components, and version numbers alone are not proof of compatibility.

**Independent Test**: Classify a series of edits to Product Model, a distributable skill, a workflow, a machine contract, registry generation and a presentation theme; produce component-specific version recommendations with their reasons.

**Acceptance Scenarios**:

1. **Given** a stable skill has only a documented, behavior-preserving defect correction, **When** a maintainer classifies the change, **Then** a PATCH increment is recommended and its evidence and compatibility limits are stated.
2. **Given** a skill adds genuinely optional functionality to a compatible contract, **When** the change is assessed against supported consumers, **Then** a MINOR increment may be recommended only if prior required behavior still works.
3. **Given** a required output is removed or renamed, **When** the change is classified, **Then** it is considered breaking for affected consumers and requires a MAJOR increment of an already stable version.
4. **Given** only a README label or visual token changes with no contract or behavior impact, **When** versioning is assessed, **Then** the system does not force unrelated Product Model, skill or workflow version increments.
5. **Given** an unpublished or pre-1.0 component, **When** it changes, **Then** its compatibility expectations are explicitly distinguished from published stable guarantees; pre-1.0 does not mean changes may be made silently.

### User Story 2 - Find Consumer Breakage Before Accepting a Change (Priority: P1)

As a maintainer or agent, I need to know which supported consumers will break before changing a canonical model, skill contract or workflow.

**Why this priority**: Seemingly additive changes can still break closed-enum readers, strict schema validators or consumer assumptions.

**Independent Test**: Compare a proposed change against supported, known baselines and declared dependents; distinguish compatible, breaking, review-required and unassessed outcomes, including the affected paths.

**Acceptance Scenarios**:

1. **Given** an existing skill consumer requires an output, **When** that output is removed or its meaning changes, **Then** the impact record identifies the affected consumer and marks compatibility broken.
2. **Given** a new canonical gate or decision value, **When** downstream consumers use exhaustive/closed vocabularies, **Then** compatibility is not automatically declared merely because an item was added.
3. **Given** a new required manifest field, **When** existing manifests and strict readers do not support it, **Then** the proposed contract change is detected as potentially breaking and is not silently called MINOR.
4. **Given** compatible additions with verified readers that tolerate them, **When** the change is assessed, **Then** those readers are reported as compatible while any unverified readers remain unassessed.
5. **Given** a referenced dependency with unknown version or no recorded baseline, **When** compatibility is checked, **Then** the result is explicitly unassessed and cannot be reported as verified compatible.

### User Story 3 - Protect Existing Durable Data During Evolution (Priority: P1)

As a builder with saved project state, evidence and decisions, I want an upgrade not to corrupt or silently reinterpret my existing work.

**Why this priority**: Shared state outlives chats and individual skills; silent semantic rewrites could turn assumptions into facts or erase decision history.

**Independent Test**: Evaluate legacy project-state/evidence samples against proposed contract changes, describe needed migration, and simulate missing, incompatible, incomplete and repeated migrations at the requirements level.

**Acceptance Scenarios**:

1. **Given** existing project-state data with a legacy field shape, **When** a contract revision is introduced, **Then** it remains readable under a documented supported contract or requires an explicit migration route.
2. **Given** a migration changes representation, **When** it completes, **Then** original evidence provenance, gate/decision distinction and decision-history meaning are preserved and verifiable.
3. **Given** a migration encounters invalid data or fails partway, **When** its result is reported, **Then** partial completion, affected records and recovery options are visible; no unsupported success claim is made.
4. **Given** a migration is repeated on already migrated input, **When** it runs again, **Then** it does not silently duplicate records or apply the transformation twice.
5. **Given** a new Shared Product Context under Spec 009, **When** it consumes legacy project artifacts, **Then** it must use the same published compatibility/migration rules rather than redefining them.

### User Story 4 - Enforce a Truthful Compatibility Gate (Priority: P1)

As a contributor, I want a checkable change assessment so a new version number cannot conceal unsupported breakage.

**Why this priority**: Deterministic checks catch contract drift; behavioral and semantic claims still need evidence or human review.

**Independent Test**: Evaluate positive and negative fixtures for version increments, canonical IDs, schema compatibility, skill/workflow dependencies and migration coverage; observe actionable outcomes without modifying source artifacts.

**Acceptance Scenarios**:

1. **Given** a change with no breaking impact across the known supported baseline, **When** required checks have evidence, **Then** a compatible outcome includes the evaluated scope and proof.
2. **Given** a known breaking change with an insufficient version increment or absent migration disposition, **When** assessed, **Then** the compatibility gate fails and names the reason.
3. **Given** behavioral equivalence cannot be proven by static comparison, **When** classified, **Then** a review-required/unassessed result is issued instead of pretending it passed behavioral tests.
4. **Given** an incompatible consumer dependency range, **When** composing skills or workflows, **Then** the mismatch is reported with affected component identities and supported versions.
5. **Given** the checker sees no actual runtime or release evidence, **When** it reports, **Then** it does not claim runtime verification, user migration success or a published release.

### User Story 5 - Deprecate and Replace Safely (Priority: P2)

As a skill consumer, I need a clear notice and replacement path when a component or contract is being retired.

**Why this priority**: Deprecation is not removal, and users need time and instructions to adapt while their supported version still works.

**Independent Test**: Review a deprecated field, skill and workflow and determine current usability, replacement, compatibility window, affected consumers, support status and removal preconditions.

**Acceptance Scenarios**:

1. **Given** a currently supported skill is deprecated, **When** its consumers inspect it, **Then** they can distinguish supported-but-deprecated from unsupported or removed.
2. **Given** a replacement is available, **When** a deprecation notice is published, **Then** the replacement, migration obligations and relevant version boundaries are explicit.
3. **Given** a proposed removal without a known consumer assessment or required migration, **When** readiness is checked, **Then** removal is blocked or its exceptional justification and residual risk are explicit.
4. **Given** an urgent safety issue requires a shortened transition, **When** an exception is proposed, **Then** it carries an explicit reason, affected scope, mitigation and appropriate approval instead of silently waiving obligations.

### User Story 6 - Know What Is Supported (Priority: P2)

As an external contributor or AI agent, I need an unambiguous, discoverable answer about current compatibility without mistaking an empty registry or unimplemented future feature for a published release.

**Why this priority**: Consumers cannot make safe upgrade decisions when supported baselines and contract authority are implicit.

**Independent Test**: Inspect authoritative policy and the state of the repository with no currently published distributable skills, then answer what is versioned, which baselines are supported and which checks are planned versus implemented.

**Acceptance Scenarios**:

1. **Given** the canonical model records version 1.0.0 but no distributable skills are published, **When** a user checks support, **Then** model identity is not presented as evidence that skill releases exist.
2. **Given** a registry format version or asset revision, **When** queried, **Then** it is distinguished from a skill release version and from compatibility of behavioral semantics.
3. **Given** a policy is specified but validation is not implemented, **When** a maintainer reports its readiness, **Then** it is labeled planned rather than verified or enforced.

### Edge Cases

- The first version for a component is created without a prior baseline: initial version assignment is distinguished from a proven compatibility comparison.
- A pre-1.0 component changes incompatibly; version numbering rules and support expectations are explicit without claiming stable guarantees.
- Changing a canonical phase ID, cycle ownership, gate/decision meaning or decision enumeration affects several schema-derived views.
- A seemingly additive enum value breaks an exhaustive reader; an optional field breaks a strict reader; removing an unused field is not assumed safe without consumer evidence.
- A manifest and SKILL.md disagree about version or changed behavior; registry projection is stale; an unknown skill reference cannot be treated as compatible.
- A skill's trigger exclusion, evidence threshold, output semantics, stopping conditions or side effects change without structural schema changes.
- Dependency version constraints conflict or form a cycle; the referenced component is unpublished, unsupported or not installed.
- Multiple compatibility versions coexist, including two saved projects at different revisions; a newer writer must not silently rewrite an older project's meaning.
- A migration is interrupted, retried, applied out of order, leaves dangling references or irreversibly discards evidence.
- A deprecated capability has no direct replacement, or a user intentionally remains on the older supported version.
- Translation, presentation or documentation-only changes do not alter canonical machine semantics; changing those semantics is not disguised as a visual change.
- Only a Git diff, static validation, proposed migration or draft document exists; runtime/migration success cannot be inferred.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST define an authoritative, discoverable versioning and compatibility policy for every independently consumed canonical contract surface: Product Model, distributable skill behavior/metadata, workflow, machine schema/format and persisted project data.
- **FR-002**: Version ownership MUST be component-specific; a repository revision, registry format version, lockfile revision or presentation token revision MUST NOT automatically represent the behavioral version of every skill or the Product Model.
- **FR-003**: The policy MUST specify stable component identity separately from version, including which identifiers remain stable across compatible changes.
- **FR-004**: Stable component versions MUST use MAJOR.MINOR.PATCH semantics with breaking/incompatible, backward-compatible functional and backward-compatible corrective meanings respectively; compatibility claims MUST be supported by an assessed baseline.
- **FR-005**: The policy MUST explicitly define pre-1.0 semantics, first-version behavior, version increment precedence and when a component can claim a stable 1.0+ compatibility promise.
- **FR-006**: The policy MUST distinguish a versioned component's content/contract version from a versioned serialization format and from a content fingerprint or generated artifact revision.
- **FR-007**: For each change, a maintainer MUST be able to identify the prior supported baseline, proposed state, scope of known dependents, change classification, required increment and evidence or unresolved assumptions.
- **FR-008**: Change classification MUST distinguish compatible, breaking, review-required and unassessed states; unknown information MUST NOT silently default to compatible.
- **FR-009**: Classification MUST assess both structural and semantic compatibility of canonical Product Model IDs, relationships, gate/decision meanings and downstream derived contract expectations.
- **FR-010**: Classification MUST assess skill inputs, outputs, metadata, triggers including exclusions, promised behavior, evidence safeguards, quality gates and stop conditions; unchanged file structure alone MUST NOT prove behavioral compatibility.
- **FR-011**: Classification MUST assess workflow consumer expectations, including referenced skills, required outcomes and dependency requirements, without redefining workflow orchestration authority.
- **FR-012**: Classification MUST account for strict/closed consumers: newly added enum members, fields, outputs or optional features MUST NOT be assumed compatible without evidence of reader tolerance.
- **FR-013**: Breaking and compatibility-relevant changes MUST identify affected known downstream consumers, their required compatibility constraints and actionable impact; unresolved or external dependents MUST be explicitly reported as outside the assessed coverage.
- **FR-014**: When a dependency compatibility constraint is declared, the system MUST evaluate the referenced component identity and version against that constraint and report absent, invalid, unsupported or conflicting versions.
- **FR-015**: Existing authoritative boundaries MUST be preserved: Product Model owns lifecycle IDs; SKILL.md owns behavior; manifest owns discovery metadata; registry is a deterministic projection; workflow definitions own orchestration.
- **FR-016**: Version metadata and compatibility assessments MUST NOT introduce another Product Model, require publishing development skills under .agents, or turn a derived registry into an independently edited authority.
- **FR-017**: Existing valid project-state, evidence and skill-output data MUST remain readable under a supported contract or have an explicit, reviewable migration disposition before an incompatible change is accepted.
- **FR-018**: Migration obligations MUST identify source/target versions, impacted data, prerequisites, expected postconditions, failure modes, recovery/rollback or a clearly documented irreversible/manual exception.
- **FR-019**: A migration MUST preserve provenance, assumptions, decisions and their history unless a separately authorized removal is explicitly justified; transformation MUST NOT manufacture evidence or silently change semantic authority.
- **FR-020**: Re-running, interrupting or failing a migration MUST have a defined, inspectable outcome that does not silently duplicate, discard or claim successful transformation of affected data.
- **FR-021**: The policy MUST define the distinction and allowed transitions among active, deprecated, unsupported and removed, including support expectations and how consumers learn about transitions.
- **FR-022**: Deprecation MUST identify the affected component/field, earliest affected version, replacement or absence thereof, migration guidance, supported transition conditions and removal prerequisites.
- **FR-023**: Removal MUST require an explicit compatibility-impact disposition, including an acknowledged exception path for time-critical security/safety fixes, without claiming that a breaking change is backward-compatible.
- **FR-024**: The compatibility gate MUST reject a known breaking change paired with an insufficient version increment or unresolved blocking migration/dependency obligation.
- **FR-025**: Compatibility diagnostics MUST identify the affected component, baseline/proposed versions, offending change or reference, assessed dependent scope, classification and required next action.
- **FR-026**: Deterministic checks MUST cover structurally decidable violations; semantic or behavioral equivalence that cannot be established mechanically MUST remain review-required until substantiated.
- **FR-027**: Verification records MUST distinguish policy-defined, static-checked, behavior-tested, migrated-in-test, runtime-verified and published states; no stronger state may be asserted without corresponding evidence.
- **FR-028**: Representative compatible, breaking, strict-consumer, missing-baseline, unknown-dependency, deprecation and migration-failure examples MUST be independently assessable with expected outcomes.
- **FR-029**: Compatibility scope MUST be anchored to declared supported baselines and known/declared dependents; unbounded compatibility with all historical or unknown external consumers MUST NOT be asserted.
- **FR-030**: Compatibility policy MUST remain available to future Spec 005 evaluation, Spec 006 governance, Spec 008 release lifecycle and Spec 009 Shared Product Context without implementing those features as part of this spec.
- **FR-031**: Existing repository files with independent version-like fields MUST be audited and normalized or explicitly documented, without mass-rewriting previously recorded historical artifacts merely to match a new field name.
- **FR-032**: Proposed public documentation changes MUST describe planned policy until the matching contracts/checks have implementation evidence; existing project docs MUST NOT be promoted as implemented prematurely.

### Key Entities

- **Versioned Component**: Stable identity, component type, contract/behavior authority and independently meaningful version.
- **Supported Baseline**: A recorded earlier component/contract state and declared support scope against which compatibility can actually be assessed.
- **Consumer Dependency**: A known consumer, its referenced component identity, required interface/behavior and acceptable version constraints.
- **Compatibility Assessment**: Proposed change versus a baseline and known consumer set, with classification, coverage, reasoning, evidence and unresolved risks.
- **Change Classification**: Compatible, breaking, review-required or unassessed change category; this is distinct from Product Model gate results pass/warn/fail and workflow decisions.
- **Migration Disposition**: Defined treatment of old data or consumers, including upgrade obligations, retained history, recovery and exceptional non-reversibility.
- **Deprecation Notice**: Affected capability, replacement/support window, migration obligations and removal preconditions.
- **Verification Evidence**: The limited, verifiable basis of a compatibility conclusion (static, behavioral, runtime or published evidence).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For 100% of canonical component categories in scope, a contributor can identify version authority, version meaning, supported baseline policy and whether a change to that component affects another component's version.
- **SC-002**: A reviewer classifies every defined positive/negative example of PATCH, MINOR, MAJOR and pre-1.0 change consistently with the published policy, including explanatory evidence.
- **SC-003**: All test fixtures of known removal/rename of required outputs, invalid lifecycle references, and strict-consumer additions are reported as breaking or requiring review, never silently compatible.
- **SC-004**: Every evaluated dependency mismatch or absent/unknown baseline produces an actionable result and identifies its assessment limit.
- **SC-005**: 100% of representative legacy project-state/evidence fixtures either remain readable with documented semantics or receive an explicit migration disposition without silent history loss.
- **SC-006**: Migration edge-case fixtures cover interrupted, repeated, partial, irreversible and missing-source cases with documented outcomes and no unsupported success claim.
- **SC-007**: Every deprecated example clearly identifies support status, version boundary, replacement or its absence, consumer migration guidance and removal prerequisites.
- **SC-008**: A change with an inadequate version bump or unresolved known breaking dependency is rejected by the compatibility gate in every negative fixture.
- **SC-009**: Every compatibility assessment distinguishes static/semantic review evidence from behavior, runtime and publication evidence; 0 assessments claim verification not performed.
- **SC-010**: A new maintainer can use the documented policy and examples to identify the correct component version and next safe upgrade action for all primary user stories without relying on chat history.

## Assumptions

- This repo is in foundation development; the canonical Product Model currently declares `model_version: 1.0.0`, while no distributable skills are currently published. A stored version is not itself publication evidence.
- `registry_version: 1` is an existing registry representation marker; `skills-lock.json` and presentation-token revisions serve different concerns. Their formats may require classification, not blind conversion to SemVer.
- Versioned artifacts may have distinct consumers and supported baselines; new skill metadata fields must be introduced with explicit migration/compatibility handling because currently unknown manifest fields are rejected.
- Stable SemVer applies to versioned stable interfaces; for pre-1.0 components, incompatible changes require an explicit declared policy (including a MINOR-level boundary where appropriate), not an implied guarantee of backwards compatibility.
- Compatibility is assessed relative to declared known/supported consumers, not every possible unpublished external integration.
- Automated structural comparison cannot prove all behavioral semantics; human review and later standardized skill evaluations remain necessary.
- The safest default for unassessed changes is to withhold a compatible claim, not to treat every unknown as a proven breaking change.
- Spec 001 Product Model and Spec 002 Skill Model are canonical upstream authorities. Spec 009 will later require compatibility with existing durable project data but is not an implementation dependency.

## Policy Decisions Recorded for Later Stages

- **D-001**: Component-specific version ownership; no monolithic repository version as a substitute for skill/model/workflow contract versions.
- **D-002**: MAJOR.MINOR.PATCH for stable versions; explicit pre-1.0 and baseline rules.
- **D-003**: Compatibility is a verified property relative to supported consumers, not inferred from the version string.
- **D-004**: Additive structural changes require strict-consumer and semantic assessment, not automatic MINOR classification.
- **D-005**: No consumer-impact visibility means unassessed scope, never universal compatibility.
- **D-006**: Migration preserves evidence/decision history; failure, retries and exceptions must be observable.
- **D-007**: Deprecation is a supported transition state distinct from unsupported and removed.
- **D-008**: Rule enforcement and evidence scope belong to Spec 004; release/tag/changelog automation belongs to Spec 008.

## Out of Scope

- Publishing releases, tags, generated release notes, changelogs and end-to-end release automation (Spec 008).
- Broad skill quality scoring, behavioral evaluation suites or comparative benchmarks (Spec 005).
- Review-owner assignments, change-approval workflows, proposal and maintainer governance (Spec 006).
- Building a marketplace, hosted compatibility service or long-running upgrade orchestrator.
- Inventing/renaming canonical lifecycle vocabulary or changing registry authority defined by Specs 001 and 002.
- Implementing Spec 009 shared storage, concurrency and cross-skill handoff; only preserve a compatible future boundary.
- Performing speculative migrations on user projects or bulk removal of legacy state as a side effect of specification.

## Project Docs Impact

Promotion candidates **only after implementation and verification**:

- `docs/ARCHITECTURE.md` — component version authorities, compatibility assessment and migration boundary.
- `SKILL-MODEL.md` and `SKILL-CONTRACT.md` — skill/manifest version and dependency compatibility requirements.
- `PRODUCT-MODEL.md` — versioned Product Model compatibility rules without a second ontology.
- `CONTRIBUTING.md` and `QUALITY-GATES.md` — compatible/breaking checks and evidence expectations.
- `README.md` and `README.vi.md` — discoverability after policy implementation.
- Relevant `schemas/`, `templates/` and workflow references require contract impact review; planned changes do not imply automatic edits.

**Roadmap relation**: Depends on Spec 001; consumes Spec 002 authority when assessing skills. Unblocks policy dependencies for Specs 005, 006, 007 and 008 only after appropriate implementation and verification. Spec 009 remains specification-only and independent.
