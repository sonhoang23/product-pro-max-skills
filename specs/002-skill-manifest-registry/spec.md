# Feature Specification: Skill Manifest Registry

**Feature Branch**: `main`

**Created**: 2026-10-07

**Status**: Draft

**Input**: Define a global-first, machine-readable metadata contract and registry for canonical Product Pro Max skills so humans and AI agents can discover, inspect, relate, and compose skills using stable lifecycle, trigger, input/output, related-skill, and workflow semantics built on Spec 001.

## User Scenarios & Testing

### User Story 1 - Discover the Right Skill Without Reading the Whole Repository (Priority: P1)

As a builder or AI agent, I need one machine-readable catalog of canonical skills so I can identify relevant skills from product context without opening every `SKILL.md`.

**Why this priority**: Discovery is the primary value of the feature. A registry that cannot reliably answer “which skill fits this situation?” does not solve the foundation problem.

**Independent Test**: Starting only from the registry, a reader or agent can identify candidate canonical skills by stable skill identity, lifecycle association, trigger context, expected inputs/outputs, related skills, or workflow membership.

**Acceptance Scenarios**:

1. **Given** a product is at a canonical lifecycle phase, **When** the registry is queried by that lifecycle context, **Then** it returns the skills explicitly associated with that canonical Product Model context.
2. **Given** a user intent matches a skill trigger, **When** a reader or agent inspects registry metadata, **Then** the skill can be identified without parsing the full skill body.
3. **Given** a candidate skill, **When** its registry entry is inspected, **Then** the reader can see enough metadata to decide whether to open or invoke that skill.

### User Story 2 - Understand a Skill Contract and Its Relationships (Priority: P1)

As a contributor or AI agent, I need each skill to expose consistent metadata for trigger, required and optional inputs, outputs, lifecycle placement, related skills, and workflows so composition does not depend on prose conventions.

**Why this priority**: Machine discovery is only useful when metadata means the same thing across every canonical skill.

**Independent Test**: Two different canonical skills can be inspected through the same metadata contract and their trigger, inputs, outputs, lifecycle relations, related-skill relations, and workflow usage can be compared without interpreting custom field shapes.

**Acceptance Scenarios**:

1. **Given** two skills have different prose bodies, **When** their manifests are inspected, **Then** the same metadata concepts use the same contract and semantics.
2. **Given** a skill requires specific context before use, **When** its manifest is inspected, **Then** required inputs are distinguishable from optional inputs.
3. **Given** a skill produces named semantic outputs, **When** its manifest is inspected, **Then** those outputs are explicitly discoverable without changing the underlying skill behavior.
4. **Given** a skill participates in a workflow or has a relationship with another skill, **When** its metadata is inspected, **Then** the referenced skill or workflow and the meaning of the relationship are explicit.

### User Story 3 - Keep Registry Metadata Trustworthy (Priority: P1)

As a maintainer, I need deterministic integrity rules so missing skills, duplicate identities, invalid Product Model references, and broken skill/workflow relationships cannot silently enter the catalog.

**Why this priority**: A stale or contradictory registry is worse than no registry because agents may route work using incorrect metadata.

**Independent Test**: Repository validation accepts a fully consistent skill catalog and rejects representative drift such as a duplicate skill ID, an unknown lifecycle ID, a missing related skill, or a workflow relation that cannot resolve.

**Acceptance Scenarios**:

1. **Given** every canonical skill has valid metadata and every reference resolves, **When** registry integrity is checked, **Then** validation passes.
2. **Given** a skill references a lifecycle identifier that is not present in the canonical Product Model, **When** integrity is checked, **Then** validation fails with the invalid reference identified.
3. **Given** a relation points to a missing skill or workflow, **When** integrity is checked, **Then** validation fails rather than silently dropping the relation.
4. **Given** a canonical skill exists under `skills/` but is absent from the registry, **When** coverage is checked, **Then** validation reports incomplete catalog coverage.

### User Story 4 - Preserve Global-First and Product/Tooling Boundaries (Priority: P2)

As an international contributor, I need canonical metadata to use stable English machine identifiers while remaining understandable to humans and excluding repository-development tooling from the distributable skill catalog.

**Why this priority**: The registry becomes a shared public contract. Mixing localized identifiers or `.agents/` development skills into the product catalog would create ambiguity for downstream consumers.

**Independent Test**: A contributor can inspect the registry and distinguish canonical distributable skills from repository-development skills, while all machine-facing IDs remain English and ASCII-safe.

**Acceptance Scenarios**:

1. **Given** a canonical distributable skill, **When** its metadata is inspected, **Then** machine identifiers use English, stable ASCII-safe values and human-readable descriptions can still be localized in derived views.
2. **Given** a repository-development skill under `.agents/`, **When** canonical registry coverage is checked, **Then** it is not treated as a distributable Product Pro Max skill.
3. **Given** a localized documentation surface, **When** it references a registered skill, **Then** the canonical skill ID remains unchanged.

### Edge Cases

- A skill directory exists under `skills/` but its manifest metadata is missing or incomplete.
- Two skills declare the same canonical skill ID.
- A manifest skill ID disagrees with the canonical skill directory or existing `SKILL.md` identity.
- A skill references a cycle, phase, or track not present in `model/product-model.json`.
- A phase reference is paired with a cycle that does not own that phase.
- A skill legitimately applies to more than one phase or cross-cutting track.
- A related-skill relation points back to the same skill without an explicitly valid self-relation meaning.
- Two related-skill records contradict each other or use an unknown relation meaning.
- A workflow references a skill that is not present in the canonical registry.
- Registry data and per-skill metadata disagree about the same canonical fact.
- A localized alias is mistaken for a canonical machine ID.
- A `.agents/` development skill has a name similar to a distributable skill under `skills/`.
- A new discovery field is proposed that would actually define compatibility, deprecation, quality evaluation, or search ranking semantics owned by a later foundation spec.

## Requirements

### Functional Requirements

- **FR-001**: The repository MUST define one canonical metadata contract for every distributable Product Pro Max skill under `skills/`.
- **FR-002**: Every canonical skill MUST have exactly one stable canonical skill ID, and that ID MUST agree with the skill's canonical repository identity rather than introducing a parallel naming system.
- **FR-003**: Canonical skill metadata MUST include enough identity and description information for a human or AI agent to understand the skill's responsibility without parsing its full body.
- **FR-004**: Canonical skill metadata MUST express lifecycle associations using only canonical cycle, phase, and track identifiers defined by `model/product-model.json`; any referenced phase/cycle combination MUST respect Product Model ownership.
- **FR-005**: A canonical skill MUST be able to declare more than one applicable lifecycle association when its bounded responsibility legitimately spans phases or cross-cutting tracks, without redefining lifecycle semantics.
- **FR-006**: Canonical skill metadata MUST express positive trigger conditions that indicate when the skill is relevant and negative or exclusion conditions when using the skill would be inappropriate or misleading.
- **FR-007**: Canonical skill metadata MUST distinguish required inputs from optional inputs and MUST identify the semantic purpose of each declared input.
- **FR-008**: Canonical skill metadata MUST declare the skill's expected semantic outputs so consumers can determine what the skill produces without inferring output fields from prose.
- **FR-009**: When a skill produces canonical gate or decision semantics, its metadata and declared outputs MUST remain compatible with the gate and decision vocabularies established by Spec 001.
- **FR-010**: Canonical skill metadata MUST support typed relationships to other canonical skills so a consumer can distinguish why another skill is related rather than receiving an unqualified list of names.
- **FR-011**: Every related-skill reference MUST resolve to an existing canonical skill ID, and relation semantics MUST be consistent across all skills.
- **FR-012**: Canonical metadata MUST expose workflow membership or workflow relationships for skills used by repository workflows, and every workflow reference MUST resolve to an existing canonical workflow.
- **FR-013**: Skill-to-workflow relationships MUST preserve workflow authority: metadata may expose composition relationships for discovery but MUST NOT duplicate or redefine workflow execution logic.
- **FR-014**: The repository MUST provide one aggregate machine-readable registry covering every canonical distributable skill exactly once and excluding repository-development skills under `.agents/`.
- **FR-015**: The registry MUST make the following discovery dimensions directly inspectable without opening every `SKILL.md`: canonical skill identity, description, lifecycle association, trigger/exclusion context, inputs, outputs, related skills, and workflow relationships.
- **FR-016**: The feature MUST define an authority rule between per-skill metadata and the aggregate registry so the same metadata fact does not have two independently editable canonical definitions.
- **FR-017**: Repository validation MUST detect incomplete registry coverage, duplicate skill IDs, malformed required metadata, invalid Product Model references, unresolved skill references, unresolved workflow references, and disagreement between canonical metadata and derived registry views.
- **FR-018**: Canonical machine identifiers introduced by this feature MUST use English, stable ASCII-safe identifiers; localized labels or explanations MUST NOT replace or fork canonical IDs.
- **FR-019**: Existing canonical skills MUST be able to adopt the metadata contract without changing their bounded behavioral responsibility solely to satisfy registry structure.
- **FR-020**: The metadata contract MUST remain focused on discovery and composition and MUST NOT define general versioning/compatibility/deprecation policy, standardized skill eval policy, release lifecycle, final documentation information architecture, catalog UI, or search-ranking behavior owned by later foundation specs.

### Key Entities

- **Skill Manifest**: Canonical metadata for one distributable skill, describing identity, responsibility, lifecycle association, trigger boundaries, inputs, outputs, and relationships without replacing the skill's behavioral instructions.
- **Skill Registry**: Aggregate machine-readable catalog that exposes canonical skills and their relationships for discovery, inspection, and composition.
- **Lifecycle Association**: Reference from a skill to canonical cycle, phase, or track semantics owned by the Product Model.
- **Trigger Descriptor**: Metadata describing conditions in which a skill should or should not be selected.
- **Input Descriptor**: Named semantic input expected by a skill, including whether it is required or optional.
- **Output Descriptor**: Named semantic result a skill is expected to produce.
- **Skill Relation**: Typed reference between two canonical skills that explains the relationship used for discovery or composition.
- **Workflow Relation**: Reference connecting a canonical skill to an existing workflow without transferring workflow orchestration authority into the skill manifest.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of canonical skill directories under `skills/` are represented exactly once in the aggregate registry.
- **SC-002**: 100% of registered lifecycle references resolve to canonical Product Model IDs, and every phase/cycle pair respects Product Model ownership.
- **SC-003**: 100% of related-skill references and workflow references resolve to existing canonical targets.
- **SC-004**: For every registered skill, a reader or agent can determine its identity, purpose/description, trigger boundary, required versus optional inputs, expected outputs, lifecycle associations, related skills, and workflow relationships from the metadata/registry contract without reading all skill bodies.
- **SC-005**: Introducing any representative duplicate skill ID, missing registry entry, invalid lifecycle reference, unresolved related skill, unresolved workflow, or canonical/derived metadata mismatch causes repository validation to fail.
- **SC-006**: Repository-development skills under `.agents/` contribute zero entries to the canonical distributable skill registry unless a later explicit product decision moves them into `skills/`.
- **SC-007**: Existing canonical skill behavior remains semantically unchanged by metadata migration; the feature adds discoverability and integrity rather than silently expanding skill responsibilities.
- **SC-008**: No general versioning, deprecation, standardized eval, release lifecycle, final docs/catalog UI, or search-ranking contract is introduced by Spec 002.

## Assumptions

- Spec 001 is implemented, verified, and converged; `model/product-model.json` is the canonical authority for lifecycle, gate, and decision semantics.
- The canonical product skill surface is `skills/<skill-name>/SKILL.md`; `.agents/` remains repository-development tooling.
- Existing skill `name` and `description` frontmatter provide useful seed identity/description data but are not yet a complete discovery contract.
- Existing skill sections such as Trigger, Inputs, and Output contract can inform migration, but the registry must not depend on free-form prose parsing as its only discovery mechanism.
- A skill may legitimately map to multiple lifecycle contexts, but metadata must keep the skill's responsibility bounded in accordance with the constitution.
- English is canonical for shared metadata fields, machine IDs, and discovery semantics; localized documentation may provide translated presentation around those stable values.
- The exact storage layout, schema format, generation mechanism, and validation implementation are planning decisions as long as the authority and observable behavior in this spec are preserved.

## Out of Scope

- General semantic versioning, compatibility guarantees, breaking-change policy, migrations, and deprecation rules owned by Spec 003.
- Standardized skill evaluation suites, scoring, quality benchmarks, and expanded validation policy owned by Spec 004.
- Repository ownership/review governance owned by Spec 005.
- Final documentation architecture, public catalog UI, visual browsing experience, localization architecture, and search ranking owned by Spec 006.
- Release, changelog, tag, migration, and removal flow owned by Spec 007.
- Changing the canonical Product Model established by Spec 001.
- Rewriting skill behavioral workflows solely for metadata normalization.

## Project Docs Impact

- `README.md`
- `README.vi.md`
- `SKILL-CONTRACT.md`
- `docs/ARCHITECTURE.md`
