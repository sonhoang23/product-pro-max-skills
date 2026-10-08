# Feature Specification: Skill Manifest Registry

**Feature Branch**: `main`

**Created**: 2026-10-07

**Status**: Draft

**Spec modeling (planned truth)**: [Quan hệ khái niệm skill và metadata](spec-diagram/skill-metadata-relations.html) · [Feature diagram ledger](diagrams.html).

**Input**: Define the canonical Product Pro Max skill model, per-skill machine-readable manifest contract, physical organization, namespace, and derived registry so humans and AI agents can discover, inspect, relate, author, and compose skills consistently. Canonical distributable skills use the `ppmax-` namespace, are physically grouped by one primary lifecycle cycle, retain many-to-many lifecycle metadata, and remain compatible with the Product Model established by Spec 001.

## User Scenarios & Testing

### User Story 1 - Discover the Right Skill Without Reading the Whole Repository (Priority: P1)

As a builder or AI agent, I need one machine-readable catalog of canonical skills so I can identify relevant skills from product context without opening every `SKILL.md`.

**Why this priority**: Discovery is the primary value of the feature. A registry that cannot reliably answer “which skill fits this situation?” does not solve the foundation problem.

**Independent Test**: Starting only from the registry, a reader or agent can identify candidate canonical skills by stable skill identity, lifecycle association, trigger context, expected inputs/outputs, related skills, or workflow membership.

**Acceptance Scenarios**:

1. **Given** a product is at a canonical lifecycle phase, **When** the registry is queried by that lifecycle context, **Then** it returns the skills explicitly associated with that canonical Product Model context.
2. **Given** a user intent matches a skill trigger, **When** a reader or agent inspects registry metadata, **Then** the skill can be identified without parsing the full skill body.
3. **Given** a candidate skill, **When** its registry entry is inspected, **Then** the reader can see enough metadata to decide whether to open or invoke that skill.
4. **Given** skills from Product Pro Max are installed alongside skills from other sources, **When** their canonical IDs are inspected, **Then** Product Pro Max skills are immediately distinguishable by the `ppmax-` prefix.

### User Story 2 - Understand a Skill Contract and Its Relationships (Priority: P1)

As a contributor or AI agent, I need each skill to expose consistent metadata for identity, lifecycle association, trigger boundaries, required and optional inputs, outputs, related skills, and workflows so composition does not depend on prose conventions.

**Why this priority**: Machine discovery is only useful when metadata means the same thing across every canonical skill.

**Independent Test**: Two different canonical skills can be inspected through the same manifest contract and their identity, trigger, inputs, outputs, lifecycle relations, related-skill relations, and workflow usage can be compared without interpreting custom field shapes.

**Acceptance Scenarios**:

1. **Given** two skills have different prose bodies, **When** their manifests are inspected, **Then** the same metadata concepts use the same contract and semantics.
2. **Given** a skill requires specific context before use, **When** its manifest is inspected, **Then** required inputs are distinguishable from optional inputs.
3. **Given** a skill produces named semantic outputs, **When** its manifest is inspected, **Then** those outputs are explicitly discoverable without changing the underlying skill behavior.
4. **Given** a skill participates in a workflow or has a relationship with another skill, **When** its metadata is inspected, **Then** the referenced skill or workflow and the meaning of the relationship are explicit.
5. **Given** two skills are related, **When** their relation metadata is inspected, **Then** the relation uses a canonical relation type rather than an ad hoc label invented by one skill.

### User Story 3 - Keep Registry Metadata Trustworthy (Priority: P1)

As a maintainer, I need deterministic integrity rules and a single metadata authority so missing skills, duplicate identities, invalid Product Model references, broken relationships, and registry drift cannot silently enter the catalog.

**Why this priority**: A stale or contradictory registry is worse than no registry because agents may route work using incorrect metadata.

**Independent Test**: Repository validation accepts a fully consistent skill catalog and rejects representative drift such as a duplicate skill ID, an invalid lifecycle reference, a missing related skill, a path/primary-cycle mismatch, or a derived registry entry that disagrees with the canonical manifest.

**Acceptance Scenarios**:

1. **Given** every canonical skill has valid metadata and every reference resolves, **When** registry integrity is checked, **Then** validation passes.
2. **Given** a skill references a lifecycle identifier that is not present in the canonical Product Model, **When** integrity is checked, **Then** validation fails with the invalid reference identified.
3. **Given** a relation points to a missing skill or workflow, **When** integrity is checked, **Then** validation fails rather than silently dropping the relation.
4. **Given** a canonical skill exists under `skills/` but is absent from the derived registry, **When** coverage is checked, **Then** validation reports incomplete catalog coverage.
5. **Given** registry content disagrees with a canonical per-skill manifest, **When** validation runs, **Then** the registry is treated as stale or invalid rather than becoming a competing source of truth.

### User Story 4 - Organize a Large Skill Library Without Losing Semantic Accuracy (Priority: P1)

As a maintainer or contributor, I need canonical skills grouped into stable lifecycle-based folders so a large repository remains navigable while the filesystem does not falsely imply that a skill belongs to only one phase or lifecycle context.

**Why this priority**: The repository is expected to grow beyond a small flat list. Physical organization must scale without replacing the richer lifecycle graph defined in metadata.

**Independent Test**: A contributor can locate a skill through its primary lifecycle cycle, while its manifest can still express additional cycles, phases, and tracks that apply to the skill.

**Acceptance Scenarios**:

1. **Given** a canonical skill, **When** its repository path is inspected, **Then** it is grouped under exactly one canonical primary cycle.
2. **Given** a skill applies to multiple phases, tracks, or lifecycle contexts, **When** its manifest is inspected, **Then** all valid associations can be represented even though the skill has one physical primary-cycle location.
3. **Given** a skill is physically stored under one cycle, **When** an agent determines semantic applicability, **Then** it uses manifest metadata rather than inferring full lifecycle membership from the path alone.
4. **Given** a skill's declared primary cycle differs from its physical grouping, **When** repository integrity is checked, **Then** validation reports the mismatch.

### User Story 5 - Author Product Pro Max Skills Through the Canonical Contract (Priority: P1)

As a repository contributor, I need the repository's skill-authoring tooling to consume the canonical Skill Model and manifest contract so newly created or updated skills follow the same identity, organization, metadata, and validation rules by default.

**Why this priority**: A contract that authors can easily bypass will drift as the skill library grows. Foundation rules must be part of the normal skill creation path.

**Independent Test**: Creating or updating a distributable Product Pro Max skill through `.agents/skills/skill-creator-vi` results in a skill that uses the canonical namespace, correct primary-cycle placement, valid manifest metadata, and consistent `SKILL.md` identity without making `skill-creator-vi` itself the semantic authority.

**Acceptance Scenarios**:

1. **Given** a contributor creates a new Product Pro Max distributable skill, **When** `skill-creator-vi` applies repository conventions, **Then** the resulting canonical skill ID uses `ppmax-<skill-slug>`.
2. **Given** lifecycle context is known, **When** the skill is created, **Then** one primary cycle is selected for physical organization and other valid lifecycle associations remain expressible in metadata.
3. **Given** canonical Skill Model rules change in the future, **When** authoring tooling is updated, **Then** the canonical model/contract remains the source of truth and `skill-creator-vi` remains a consumer rather than a competing definition.
4. **Given** `skill-creator-vi` itself lives under `.agents/skills/`, **When** registry coverage is evaluated, **Then** it remains repository-development tooling and is not added to the distributable skill registry.

### User Story 6 - Preserve Global-First and Product/Tooling Boundaries (Priority: P2)

As an international contributor, I need canonical metadata to use stable English machine identifiers while remaining understandable to humans and excluding repository-development tooling from the distributable skill catalog.

**Why this priority**: The registry becomes a shared public contract. Mixing localized identifiers or `.agents/` development skills into the product catalog would create ambiguity for downstream consumers.

**Independent Test**: A contributor can inspect the registry and distinguish canonical distributable skills from repository-development skills, while all machine-facing IDs remain English and ASCII-safe.

**Acceptance Scenarios**:

1. **Given** a canonical distributable skill, **When** its metadata is inspected, **Then** machine identifiers use English, stable ASCII-safe values and human-readable descriptions can still be localized in derived views.
2. **Given** a repository-development skill under `.agents/`, **When** canonical registry coverage is checked, **Then** it is not treated as a distributable Product Pro Max skill.
3. **Given** a localized documentation surface, **When** it references a registered skill, **Then** the canonical skill ID remains unchanged.

### Edge Cases

- A skill directory exists under `skills/` but its canonical `manifest.yaml` is missing or incomplete.
- A distributable skill ID does not begin with `ppmax-`.
- Two skills declare the same canonical skill ID or the same unprefixed slug.
- A manifest skill ID disagrees with the skill directory name or `SKILL.md` name.
- A skill's `primary_cycle` disagrees with its physical cycle grouping.
- A skill references a cycle, phase, or track not present in `model/product-model.json`.
- A phase reference is paired with a cycle that does not own that phase.
- A skill legitimately applies to more than one cycle, phase, or cross-cutting track.
- A filesystem path is incorrectly treated as the complete semantic lifecycle assignment.
- A related-skill relation points back to the same skill without an explicitly valid self-relation meaning.
- Two related-skill records contradict each other or use a non-canonical relation type.
- A workflow references a skill that is not present in the canonical registry.
- Registry data and canonical per-skill manifest metadata disagree about the same fact.
- A contributor edits the derived registry directly without updating its canonical manifest source.
- A localized alias is mistaken for a canonical machine ID.
- A `.agents/` development skill has a name similar to a distributable skill under `skills/`.
- Existing flat, unprefixed skills must migrate to the new identity and physical grouping without changing their behavioral responsibility.
- A new metadata field is proposed that would actually define compatibility, deprecation, quality evaluation, release policy, or search-ranking semantics owned by a later foundation spec.

## Requirements

### Functional Requirements

- **FR-001**: The repository MUST define one canonical human-readable Skill Model that explains the shared semantics of Skill, Skill Manifest, skill identity, lifecycle association, primary cycle, trigger/exclusion boundary, input, output, skill relation, workflow relation, and registry.
- **FR-002**: The Skill Model MUST remain distinct from the Skill Contract: the Skill Model defines what shared skill concepts mean, while the Skill Contract defines what a valid skill must satisfy.
- **FR-003**: The repository MUST define one canonical machine-readable metadata contract for every distributable Product Pro Max skill under `skills/`.
- **FR-004**: Each canonical skill MUST keep behavioral instructions in `SKILL.md` and canonical machine metadata in a sibling `manifest.yaml`; neither artifact may silently redefine the other's responsibility.
- **FR-005**: Every distributable Product Pro Max skill MUST belong to the canonical `product-pro-max` namespace and MUST use a canonical skill ID of the form `ppmax-<skill-slug>`.
- **FR-006**: The unprefixed skill slug MUST be stable, English, ASCII-safe, and suitable for deriving the canonical `ppmax-` skill ID without creating a second independently named identity.
- **FR-007**: A canonical skill's directory name, manifest ID, and `SKILL.md` `name` MUST use the same canonical `ppmax-<skill-slug>` identity.
- **FR-008**: Every canonical skill MUST declare exactly one `primary_cycle` using a canonical cycle ID from `model/product-model.json`.
- **FR-009**: Canonical distributable skills MUST be physically grouped by `primary_cycle` using the repository shape `skills/<primary-cycle>/ppmax-<skill-slug>/`.
- **FR-010**: Physical placement MUST serve human navigation only and MUST NOT be treated as the complete semantic lifecycle authority for a skill.
- **FR-011**: Canonical skill metadata MUST support multiple lifecycle associations when a bounded skill legitimately spans additional cycles, phases, or tracks.
- **FR-012**: All lifecycle associations MUST use canonical cycle, phase, and track identifiers defined by `model/product-model.json`; any referenced phase/cycle combination MUST respect Product Model ownership.
- **FR-013**: Canonical skill metadata MUST include enough identity and description information for a human or AI agent to understand the skill's bounded responsibility without parsing its full body.
- **FR-014**: Canonical skill metadata MUST express positive trigger conditions that indicate when the skill is relevant and negative/exclusion conditions that indicate when the skill should not be selected.
- **FR-015**: Canonical skill metadata MUST distinguish required inputs from optional inputs and MUST describe inputs by semantic purpose rather than requiring implementation-specific transport or storage details.
- **FR-016**: Canonical skill metadata MUST declare expected semantic outputs so consumers can determine what the skill produces without inferring output fields from prose.
- **FR-017**: When a skill produces canonical gate or decision semantics, its declared outputs MUST remain compatible with the gate and decision vocabularies established by Spec 001.
- **FR-018**: The Skill Model MUST define a controlled canonical vocabulary for skill-to-skill relation types; individual skills MUST NOT invent incompatible relation labels ad hoc.
- **FR-019**: Canonical skill metadata MUST support typed relationships to other canonical skills so consumers can distinguish why another skill is related rather than receiving an unqualified list of names.
- **FR-020**: Every related-skill reference MUST resolve to an existing canonical skill ID and comply with the canonical relation vocabulary.
- **FR-021**: Canonical metadata MUST expose workflow membership or workflow relationships for skills used by repository workflows, and every workflow reference MUST resolve to an existing canonical workflow.
- **FR-022**: Skill-to-workflow relationships MUST preserve workflow authority: metadata may expose composition relationships for discovery but MUST NOT duplicate or redefine workflow execution logic.
- **FR-023**: The repository MUST provide one aggregate machine-readable registry covering every canonical distributable skill exactly once and excluding repository-development skills under `.agents/`.
- **FR-024**: Canonical per-skill `manifest.yaml` files MUST be the source of truth for skill metadata; the aggregate registry MUST be a derived discovery view and MUST NOT become a second independently editable semantic authority.
- **FR-025**: The registry MUST make the following discovery dimensions directly inspectable without opening every `SKILL.md`: canonical identity, namespace/slug, description, primary cycle, lifecycle associations, trigger/exclusion context, required/optional inputs, outputs, related skills, and workflow relationships.
- **FR-026**: Repository validation MUST detect incomplete registry coverage, missing manifests, invalid or duplicate `ppmax-` identities, malformed required metadata, path/primary-cycle mismatches, invalid Product Model references, unresolved skill references, non-canonical relation types, unresolved workflow references, and disagreement between canonical manifests and derived registry views.
- **FR-027**: Canonical machine identifiers introduced by this feature MUST use English and stable ASCII-safe identifiers; localized labels or explanations MUST NOT replace or fork canonical IDs.
- **FR-028**: Repository skill-authoring tooling, including `.agents/skills/skill-creator-vi`, MUST consume the canonical Skill Model and manifest contract when creating or updating Product Pro Max distributable skills and MUST NOT become a competing semantic authority.
- **FR-029**: `skill-creator-vi` MUST enforce or surface violations of canonical Product Pro Max identity, primary-cycle placement, required manifest metadata, lifecycle references, and skill/manifest identity consistency when it authors distributable skills in this repository.
- **FR-030**: Existing canonical skills MUST migrate from the current flat, unprefixed organization to the canonical `skills/<primary-cycle>/ppmax-<skill-slug>/` organization and metadata contract without changing their bounded behavioral responsibility solely for migration.
- **FR-031**: Existing skill behavior, trigger intent, evidence rules, output semantics, and workflow responsibility MUST remain semantically stable during metadata and naming migration unless a separate authoritative requirement explicitly changes them.
- **FR-032**: The metadata contract MUST remain focused on discovery, authoring consistency, and composition and MUST NOT define general versioning/compatibility/deprecation policy, standardized skill eval policy, release lifecycle, final documentation information architecture, catalog UI, or search-ranking behavior owned by later foundation specs.

### Key Entities

- **Skill Model**: Canonical human-readable semantics for shared skill concepts and relationships. It defines what the metadata concepts mean without replacing individual skill instructions.
- **Skill**: A bounded distributable Product Pro Max capability with one canonical identity, explicit trigger boundary, inputs, outputs, and behavioral instructions.
- **Skill Namespace**: Stable product-family identity for canonical distributable skills. Product Pro Max uses `product-pro-max`, surfaced in skill IDs through the `ppmax-` prefix.
- **Skill Slug**: Stable unprefixed machine name representing the skill's responsibility.
- **Canonical Skill ID**: Globally safer Product Pro Max identity formed as `ppmax-<skill-slug>`.
- **Skill Manifest**: Canonical machine metadata for one distributable skill, stored alongside `SKILL.md` and describing identity, responsibility, lifecycle association, trigger boundaries, inputs, outputs, and relationships.
- **Primary Cycle**: Exactly one canonical Product Model cycle used to organize a skill physically for human navigation; it does not limit other valid lifecycle associations.
- **Lifecycle Association**: Semantic reference from a skill to canonical cycle, phase, or track concepts owned by the Product Model.
- **Trigger Descriptor**: Metadata describing conditions in which a skill should or should not be selected.
- **Input Descriptor**: Named semantic input expected by a skill, including whether it is required or optional.
- **Output Descriptor**: Named semantic result a skill is expected to produce.
- **Skill Relation**: Typed reference between two canonical skills using the shared relation vocabulary.
- **Workflow Relation**: Reference connecting a canonical skill to an existing workflow without transferring workflow orchestration authority into the skill manifest.
- **Skill Registry**: Derived aggregate machine-readable catalog built from canonical manifests for discovery, inspection, and composition. It is not an independent semantic authority.
- **Skill Authoring Tool**: Repository-development tooling such as `skill-creator-vi` that consumes canonical skill contracts to create or update compliant product skills.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of canonical distributable skill IDs use the `ppmax-` prefix and match their directory name, manifest ID, and `SKILL.md` name.
- **SC-002**: 100% of canonical skills declare exactly one valid primary cycle and are physically grouped under that cycle.
- **SC-003**: 100% of canonical skill directories contain both behavioral instructions and canonical machine metadata, with no duplicate canonical metadata authority.
- **SC-004**: 100% of canonical skill directories under `skills/` are represented exactly once in the derived aggregate registry.
- **SC-005**: 100% of registered lifecycle references resolve to canonical Product Model IDs, and every phase/cycle pair respects Product Model ownership.
- **SC-006**: 100% of related-skill references use canonical relation types and resolve to existing canonical skill IDs; 100% of workflow references resolve to existing canonical workflow targets.
- **SC-007**: For every registered skill, a reader or agent can determine its canonical identity, purpose/description, primary cycle, broader lifecycle associations, trigger/exclusion boundary, required versus optional inputs, expected outputs, related skills, and workflow relationships from the manifest/registry contract without reading all skill bodies.
- **SC-008**: Introducing any representative invalid prefix, duplicate ID, missing manifest, path/primary-cycle mismatch, missing registry entry, invalid lifecycle reference, non-canonical relation, unresolved related skill, unresolved workflow, or manifest/registry mismatch causes repository validation to fail.
- **SC-009**: Repository-development skills under `.agents/` contribute zero entries to the canonical distributable skill registry unless a later explicit product decision moves them into `skills/`.
- **SC-010**: A Product Pro Max skill authored through `skill-creator-vi` can satisfy the canonical namespace, identity, primary-cycle, manifest, and lifecycle requirements without defining a separate authoring-only metadata model.
- **SC-011**: All pre-Spec-002 canonical skills migrate to the new naming, physical grouping, and manifest model while preserving their existing bounded behavioral responsibility.
- **SC-012**: No general versioning, deprecation, standardized eval, release lifecycle, final docs/catalog UI, or search-ranking contract is introduced by Spec 002.

## Assumptions

- Spec 001 is implemented, verified, and converged; `model/product-model.json` is the canonical authority for lifecycle, gate, and decision semantics.
- The public Product Pro Max namespace is `product-pro-max`; the concise canonical skill ID prefix is `ppmax-`.
- `SKILL.md` remains the canonical behavioral instruction artifact for a distributable skill.
- A sibling `manifest.yaml` is the canonical machine metadata artifact for that skill.
- The aggregate registry is derived from canonical per-skill manifests and is not manually maintained as a second source of truth.
- Physical organization uses one level of canonical lifecycle cycle grouping; deeper phase/track folder nesting is intentionally avoided because skill lifecycle applicability may be many-to-many.
- A skill may legitimately map to multiple lifecycle contexts, but exactly one `primary_cycle` is selected for physical navigation.
- Filesystem placement is navigation metadata, not the full semantic lifecycle authority.
- Existing skill `name`, `description`, Trigger, Inputs, and Output contract content provides migration input but does not replace the canonical machine manifest.
- `.agents/skills/skill-creator-vi` remains repository-development tooling; it will consume and enforce Product Pro Max skill contracts when authoring distributable skills but will not be registered as a product skill.
- English is canonical for shared metadata fields, machine IDs, relation semantics, and discovery contracts; localized documentation may provide translated presentation around those stable values.
- The exact registry serialization/generation mechanism and validator implementation remain planning decisions as long as the authority rules and observable behavior in this spec are preserved.

## Out of Scope

- General semantic versioning, compatibility guarantees, breaking-change policy, migrations beyond the one-time Spec 002 skill identity/layout migration, and deprecation rules owned by Spec 003.
- Standardized skill evaluation suites, scoring, quality benchmarks, and expanded validation policy owned by Spec 004.
- Repository ownership/review governance owned by Spec 005.
- Final documentation architecture, public catalog UI, visual browsing experience, localization architecture, and search ranking owned by Spec 006.
- Release, changelog, tag, migration, and removal flow owned by Spec 007.
- Changing the canonical Product Model established by Spec 001.
- Using filesystem hierarchy as a replacement for lifecycle metadata.
- Making `skill-creator-vi` or any other repository-development skill a second source of canonical Product Pro Max skill semantics.
- Rewriting existing skill behavioral workflows solely for metadata, prefix, or physical-layout normalization.

## Project Docs Impact

- `SKILL-MODEL.md`
- `SKILL-CONTRACT.md`
- `README.md`
- `README.vi.md`
- `docs/ARCHITECTURE.md`
