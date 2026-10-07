# Feature Specification: Canonical Product Model

**Feature Branch**: `main`

**Created**: 2026-10-07

**Status**: Ready for implementation

**Input**: Establish one canonical product ontology before adding more skills so lifecycle, cycle, phase, track, loop, gate, decision, and project-state semantics cannot drift across documentation, schemas, templates, workflows, and future agent discovery.

## User Scenarios & Testing

### User Story 1 - Maintain One Product Ontology (Priority: P1)

As a maintainer, I need one canonical Product Model so shared lifecycle semantics are changed once and every derived contract can be checked against the same source.

**Why this priority**: Contract drift is the highest-cost foundation risk because every later registry, validator, workflow, and documentation layer depends on these terms.

**Independent Test**: A maintainer can inspect one canonical machine-readable model and determine the complete set and relationships of cycles, phases, tracks, loops, gates, decisions, and project statuses without reconciling conflicting prose or schemas.

**Acceptance Scenarios**:

1. **Given** several descriptions of lifecycle semantics, **When** a maintainer needs the authoritative definition, **Then** exactly one machine-readable Product Model identifies every canonical ID and relationship.
2. **Given** a phase belongs to a lifecycle cycle, **When** the model is inspected, **Then** that relationship is explicit.
3. **Given** gate outcomes and workflow decisions are different concepts, **When** the model is inspected, **Then** they are represented as separate vocabularies.

### User Story 2 - Detect Contract Drift (Priority: P1)

As a contributor or AI agent, I need repository validation to detect when schemas or project-state templates diverge from the canonical Product Model.

**Why this priority**: A canonical model has little value if dependent machine contracts can silently drift.

**Independent Test**: Repository validation succeeds when canonical and derived contracts agree and fails when a canonical gate, decision, cycle, phase, or project status is changed only in a dependent contract.

**Acceptance Scenarios**:

1. **Given** a dependent schema uses canonical gate and decision values, **When** those values match the Product Model, **Then** ontology validation passes.
2. **Given** a dependent schema contains a lifecycle phase not present in the Product Model, **When** validation runs, **Then** it reports drift.
3. **Given** a project-state phase is paired with the wrong cycle, **When** the state contract is evaluated, **Then** the relationship is invalid.

### User Story 3 - Understand the Model Without Internal Context (Priority: P2)

As a new international contributor or AI agent, I need a concise human-readable explanation so I can understand the hierarchy and cross-cutting concepts without repository history.

**Why this priority**: Global-first adoption requires the canonical model to stand on its own.

**Independent Test**: A reader can start from the public README, locate the canonical Product Model, understand hierarchy, tracks, loops, gates, and decisions, and identify where machine-readable IDs live.

**Acceptance Scenarios**:

1. **Given** a reader starts at the root README, **When** they look for lifecycle semantics, **Then** they can reach the canonical Product Model in one documentation hop.
2. **Given** a reader sees a gate result, **When** they read the model documentation, **Then** they can distinguish the gate result from the decision that follows.
3. **Given** localized documentation, **When** canonical identifiers are referenced, **Then** machine-facing IDs remain unchanged.

### Edge Cases

- A new phase is proposed without an owning cycle.
- Two phases use the same machine ID.
- A track or loop is accidentally modeled as a sequential phase.
- A gate value is added to one schema but not the canonical model.
- A decision such as `pivot` is incorrectly treated as project status.
- Documentation uses friendly labels that differ from canonical machine IDs.
- Existing pre-v1 project state uses legacy `stage` semantics.

## Requirements

### Functional Requirements

- **FR-001**: The repository MUST define exactly one canonical machine-readable Product Model for shared lifecycle semantics.
- **FR-002**: The Product Model MUST define lifecycle cycles and the ordered phases owned by each cycle.
- **FR-003**: The Product Model MUST define tracks as cross-cutting disciplines rather than sequential lifecycle states.
- **FR-004**: The Product Model MUST define loops as repeatable motions that may cross cycle or phase boundaries.
- **FR-005**: The Product Model MUST define gate results separately from workflow decisions.
- **FR-006**: The Product Model MUST define project statuses separately from phases and decisions.
- **FR-007**: Every canonical machine identifier MUST be unique, English, ASCII-safe, and kebab-case where multiple words are required.
- **FR-008**: Every phase MUST belong to exactly one lifecycle cycle in Product Model v1.
- **FR-009**: Human-readable Product Model documentation MUST explain hierarchy, cross-cutting concepts, gate/decision separation, and canonical identifier rules without prior repository context.
- **FR-010**: Project-state contracts MUST use canonical cycle and phase semantics and reject invalid cycle/phase combinations.
- **FR-011**: Skill output contracts MUST use canonical gate and decision vocabularies.
- **FR-012**: Repository validation MUST fail when canonical and dependent gate, decision, cycle, phase, or project-status contracts drift.
- **FR-013**: Existing workflows MUST remain valid under Product Model v1 gate semantics.
- **FR-014**: Public architecture and README documentation MUST point to the canonical Product Model rather than act as competing lifecycle authorities.
- **FR-015**: This feature MUST NOT define skill metadata, skill registry fields, general versioning policy, release automation, or the final global documentation information architecture.

### Key Entities

- **Product Model**: Canonical collection of lifecycle and decision semantics plus relationships.
- **Cycle**: Major lifecycle grouping organized around a product objective.
- **Phase**: Ordered product-work state owned by exactly one cycle.
- **Track**: Cross-cutting discipline that can operate across phases.
- **Loop**: Repeatable motion that turns evidence or operation into another iteration.
- **Gate Result**: Judgment about readiness or evidence sufficiency: pass, warn, or fail.
- **Decision**: Action selected after interpreting evidence and gate results.
- **Project Status**: Durable state describing whether the project is active, blocked, deferred, stopped, or completed.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All canonical cycles, phases, tracks, loops, gate results, decisions, and project statuses are represented exactly once in the machine-readable Product Model.
- **SC-002**: 100% of canonical phases resolve to exactly one owning cycle.
- **SC-003**: Repository validation reports zero ontology drift for the implemented state.
- **SC-004**: A mismatched canonical gate, decision, cycle, phase, or project-status value in a dependent contract causes validation to fail.
- **SC-005**: A reader starting from root README can reach the canonical Product Model in one documentation hop.
- **SC-006**: Existing canonical skills and workflows remain repository-valid after migration.
- **SC-007**: No Spec 002–007 implementation requirement is introduced by this feature.

## Assumptions

- The repository is pre-1.0, so this spec may normalize project-state shape before Spec 003 defines long-term compatibility guarantees.
- English is canonical for machine identifiers and shared product logic.
- User-facing labels may be localized without changing canonical IDs.
- Existing `pass|warn|fail` gate semantics remain valid.
- Existing decisions `continue|research|revise|pivot|defer|stop` remain valid and may be completed with already documented decisions such as repeat, backtrack, and escalate.
- Tables and structured data are clearer than a dense diagram for the complete ontology; no visual diagram is required unless later modeling finds a relationship that prose and tables cannot express clearly.

## Out of Scope

- Skill manifest fields, tags, registry, or search ranking.
- General compatibility and release-version policy.
- Standardized skill evaluation suites.
- Final docs-site information architecture, visual identity, or catalog UI.
- Release, changelog, deprecation, migration, and removal automation.

## Project Docs Impact

- `README.md`
- `README.vi.md`
- `docs/ARCHITECTURE.md`
- `QUALITY-GATES.md`
- `SKILL-CONTRACT.md`
- `schemas/project-state.schema.json`
- `schemas/skill-output.schema.json`
- `templates/project-state/project.yaml`
