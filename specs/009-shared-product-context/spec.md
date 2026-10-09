# Feature Specification: Shared Product Context

**Feature Branch**: `main` (specification record only; no implementation authorized)
**Created**: 2026-10-09
**Status**: Draft specification recorded; requirements self-reviewed; clarification, modeling, planning, implementation and runtime verification not started
**Input**: Approved product-design discussion: a shared, progressive context for all Product Pro Max skills, supporting research-first with no product idea, idea-first, many opportunities/products, evidence integrity, history, safe read/write and handoff.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Start with research, without a product idea (Priority: P1)

As a builder, I want to investigate a customer segment or market when I have no product name, concept, ICP, or proposed solution, so discovery can produce evidence and opportunities without inventing a product.

**Why this priority**: Requiring a product up front makes opportunity discovery biased and excludes research-first work.

**Independent Test**: Begin with only a research intent and optional market/segment; capture findings and later resume the same context with an independent skill.

**Acceptance Scenarios**:

1. **Given** no product idea, product name, or selected opportunity, **When** a research activity begins, **Then** the context can exist and persist meaningful work without placeholder claims becoming facts.
2. **Given** an initial unknown customer/problem, **When** research produces findings, **Then** the findings are retained with provenance and uncertainty, while product identity remains explicitly unknown.
3. **Given** research is inconclusive, **When** the activity ends, **Then** `research`, `defer`, or `stop` can be recorded without creating a product.

### User Story 2 — Start with an idea or an existing product (Priority: P1)

As a builder who already has an idea or functioning product, I want to enter at the relevant point and reuse the same context rules, without being forced to replay earlier cycles.

**Why this priority**: A shared system must serve research-first, idea-first, and existing-product users equally.

**Independent Test**: Start two independent contexts, one from an unvalidated idea and one from an existing product; preserve their initial evidence and lifecycle meaning.

**Acceptance Scenarios**:

1. **Given** an idea with no customer validation, **When** it is recorded, **Then** the idea is a hypothesis rather than established demand.
2. **Given** an operating product, **When** a context is initialized, **Then** existing product facts may be recorded with their sources and unverified claims remain flagged.
3. **Given** any entry point, **When** a skill is chosen, **Then** lifecycle phase is determined by the work being done rather than an enforced linear maturity sequence.

### User Story 3 — Explore many opportunities and products without contamination (Priority: P1)

As a builder, I want one body of market/customer research to inform several opportunities and potentially several products, while retaining clear boundaries between unrelated conclusions.

**Why this priority**: A single investigation may uncover several worthwhile problems; shared research must not force premature convergence.

**Independent Test**: Derive three opportunities from one set of research evidence, relate two products to the opportunities, and verify cross-context reuse without copying unrelated decisions.

**Acceptance Scenarios**:

1. **Given** one research collection, **When** several opportunities emerge, **Then** all opportunities may coexist with distinct identities, status, evidence links and hypotheses.
2. **Given** an opportunity, **When** more than one product direction is investigated, **Then** distinct product contexts may reference that opportunity without conflating scope or decisions.
3. **Given** shared workspace-level evidence, **When** an opportunity or product uses it, **Then** provenance and original scope remain visible.
4. **Given** a decision scoped to Product A, **When** Product B reads its context, **Then** Product A's decision is not silently applied to Product B.

### User Story 4 — Keep evidence, assumptions and decisions trustworthy (Priority: P1)

As a builder, I want each important claim and decision to be inspectable so an agent cannot turn an assumption into fact or quietly rewrite why a product direction changed.

**Why this priority**: Reuse without evidence integrity compounds mistakes across skills.

**Independent Test**: Store a hypothesis, conflicting research, a resulting strategy change and the superseded decision; reconstruct the reasoning and distinguish sources from inference.

**Acceptance Scenarios**:

1. **Given** a claim with only assumed support, **When** another skill reads it, **Then** the claim is still marked unverified.
2. **Given** contradictory evidence, **When** it is added, **Then** both supporting and conflicting records are preserved and the claim's confidence/readiness is reassessed rather than silently resolved.
3. **Given** an approved ICP or scope change, **When** it is recorded, **Then** the prior version, rationale, evidence references, decision authority and affected downstream outputs remain traceable.
4. **Given** an evidence item with unverifiable provenance, **When** it is assessed, **Then** missing information remains visible and cannot be counted as verified customer/runtime evidence.

### User Story 5 — Share context across independent skills and conversations (Priority: P1)

As a builder, I want a new skill or agent session to understand what is known and what to do next without relying on chat history or requiring me to repeat established details.

**Why this priority**: Durable handoff is the core reason for a shared context.

**Independent Test**: Finish a research task, end the session, and start a distinct skill; inspect whether it identifies the same scope, evidence, unresolved questions and relevant outputs.

**Acceptance Scenarios**:

1. **Given** an existing context, **When** a new skill starts, **Then** it can discover a concise entry point and locate detailed evidence, decisions and artifacts relevant to its task.
2. **Given** a skill completes work, **When** it hands off results, **Then** new findings, assumptions, risks, evidence references, decisions (if authorized) and suggested next actions are distinguishable.
3. **Given** no matching downstream skill, **When** work finishes, **Then** the context remains useful without a required orchestrator or fictional skill.
4. **Given** a skill recommends a next action, **When** no user/delegated authority permits execution, **Then** no next skill is automatically invoked.

### User Story 6 — Protect authority and concurrent changes (Priority: P1)

As a builder, I want skills to contribute evidence safely without silently modifying strategic decisions or overwriting work from another agent.

**Why this priority**: Shared write access can create destructive conflicts and unapproved strategy drift.

**Independent Test**: Have two agents propose incompatible ICP edits from the same starting revision; verify that both contributions remain reviewable and no unauthorized version wins silently.

**Acceptance Scenarios**:

1. **Given** an established product decision, **When** an unrelated skill proposes changing it, **Then** the change remains a proposal until the appropriate user or delegated authority accepts it.
2. **Given** stale context read by a skill, **When** a conflicting update arrives first, **Then** the later writer detects the changed basis and must reconcile or defer instead of silently overwriting it.
3. **Given** the writer cannot access an artifact or lacks update authority, **When** it attempts a handoff, **Then** the system identifies the limitation without claiming the update succeeded.

### User Story 7 — Revisit earlier discovery and stale knowledge (Priority: P2)

As a builder, I want to revisit old assumptions or restart research on an existing product while keeping accumulated decisions and highlighting information that may be outdated.

**Why this priority**: Learning does not follow a waterfall, and evidence loses relevance over time.

**Independent Test**: Reopen discovery for an existing product after new contradictory evidence and mark older research for review without deleting it.

**Acceptance Scenarios**:

1. **Given** an existing product in a later cycle, **When** new evidence invalidates its target-user assumption, **Then** the team can revisit discovery and backtrack without erasing later history.
2. **Given** time-sensitive research with an elapsed review condition, **When** a skill uses it, **Then** staleness is surfaced without automatically declaring the original record false.
3. **Given** an unresolved question, **When** a new activity begins, **Then** the next-action view surfaces that question with its context and provenance.

### User Story 8 — Keep workspaces and sensitive material separated (Priority: P2)

As a builder, I want customer information and work from unrelated contexts to stay separated unless explicit reuse is permitted.

**Why this priority**: Sharing context must not become accidental data disclosure.

**Independent Test**: Attempt to read a restricted interview or write a customer quote into a separate opportunity without permission; verify access boundaries and safe references.

**Acceptance Scenarios**:

1. **Given** a restricted artifact, **When** a skill without access requests it, **Then** access is denied and the skill does not fabricate or reconstruct its contents.
2. **Given** evidence contains sensitive customer data, **When** it is shared into another context, **Then** only authorized, appropriately minimized information is exposed.
3. **Given** a referenced source is missing, **When** the context is read, **Then** the missing reference is reported rather than silently substituted.

### Edge Cases

- A workspace begins with only a question (no name, product, ICP, idea or defined problem).
- A user starts with a named product but no evidence of customer need, or starts with data but no clear market.
- One opportunity is connected to several possible products; one product draws on several related opportunities; one opportunity is intentionally rejected.
- Research results apply to a segment but not every related opportunity; a source becomes inaccessible or contradicts a newer source.
- A research note references a hypothesis with an outdated identity; a decision changes and dependent artifacts become candidates for review.
- An agent session ends before persisting changes; a handoff lacks required evidence references; a file is stale or malformed.
- Two skills concurrently update the same scoped conclusion; their changes overlap or differ without a natural merge.
- A user requests an irreversible deletion; maintain a safe treatment of history and privacy/retention obligations without silently removing decision evidence.
- A completed product returns to discovery; a study produces no product; a workflow stops even though a downstream skill exists.
- Canonical `gate`, `decision`, and `project status` are confused; an agent reports `pass` based only on a draft document.
- The same source is shared across workspaces with different permission scopes or sensitivity constraints.
- Existing `.product-pro-max/` project folders follow the current product-first template and require compatibility handling rather than forced replacement.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a durable, shared context for product-related work that remains usable across independent skills, agents and sessions without dependence on chat history.
- **FR-002**: A new context MUST be creatable from research intent alone; product name, product idea, defined ICP, problem statement and proposed solution MUST all be optional at creation.
- **FR-003**: The same context contract MUST support research-first, idea-first, problem-first, evidence-first and existing-product entry points.
- **FR-004**: The context MUST progressively accumulate knowledge; missing information MUST be represented as unknown/not established rather than fabricated or treated as validation failure by default.
- **FR-005**: The system MUST distinguish workspace-level shared knowledge, opportunity-specific context and product-specific context without requiring a mandatory stage progression between them.
- **FR-006**: A workspace MUST support zero or more opportunities and zero or more products; relationships MUST allow evidence or opportunities to inform more than one product without forcing a one-to-one mapping.
- **FR-007**: Information MUST have an identifiable authority and scope; reuse across scopes MUST preserve original provenance and MUST NOT propagate unrelated conclusions or permissions implicitly.
- **FR-008**: A discoverable, concise context entry point MUST summarize known purpose, current focus, validated findings, important uncertainties, open risks, latest authorized decisions and relevant references when those fields exist.
- **FR-009**: Detailed research, assumptions, evidence, decision records and deliverables MUST remain separately addressable through stable references; the summary MUST NOT be the only authoritative storage for all details.
- **FR-010**: Every reusable material claim MUST distinguish its evidence class, basis/source, captured/reviewed time when known, confidence and unknowns consistent with the existing Evidence Model.
- **FR-011**: Unsupported assumptions and AI inferences MUST NOT be promoted to observed, measured, researched or provided facts without qualifying evidence; inference MUST reference its inputs.
- **FR-012**: Contradictory and negative evidence MUST remain discoverable and linked to the claims or hypotheses it affects.
- **FR-013**: Important decisions MUST identify scope, action, decision authority, supporting and opposing evidence, assumptions, alternatives, rationale, date and conditions for review.
- **FR-014**: Superseding or revising a decision MUST retain the earlier decision and its reasoning, with links between versions and indications of affected downstream artifacts.
- **FR-015**: Each skill's context interaction MUST have a consistent read, validate, execute, record and handoff behavior with explicit input and output boundaries; independent usefulness of a skill MUST be preserved.
- **FR-016**: A skill MUST access only the relevant context scope necessary for its task; absence of optional information MUST NOT cause unrelated stages or artifact generation to become mandatory.
- **FR-017**: A skill MUST report which relevant context records it relied upon, which new records it contributed and which proposed changes were not accepted or persisted.
- **FR-018**: Evidence contributions and new artifacts MAY be recorded within the contributor's permitted scope, but changes to approved strategic assumptions or decisions MUST require the relevant user/delegated authority.
- **FR-019**: A context update MUST detect competing or stale edits to the same authoritative information and avoid silent overwrite, loss of history or false success claims.
- **FR-020**: A failed or unauthorized context update MUST preserve the prior accepted state and surface an actionable reason.
- **FR-021**: A skill MUST distinguish a proposed decision from an approved one and MUST NOT equate an evidence-quality gate result with an action decision.
- **FR-022**: Any declared cycle, phase, gate result, decision or project status MUST use valid canonical values and relationships from the existing Product Model; the feature MUST NOT create a second lifecycle ontology.
- **FR-023**: The context MUST support revisiting earlier lifecycle work, exploring parallel opportunities, backtracking, deferring, pivoting and stopping while retaining the underlying record.
- **FR-024**: A skill handoff MUST distinguish completed work, evidence, open assumptions, risks, unresolved questions, relevant outputs and recommended next actions, and it MUST NOT require the next skill to be present or automatically run it.
- **FR-025**: Time-sensitive claims MUST expose capture/review dates and explicit review conditions when known; out-of-date records MUST be flagged for reassessment rather than automatically deleted or relabeled false.
- **FR-026**: References that are absent, corrupted, inaccessible or scoped incorrectly MUST be reported; readers MUST NOT invent missing sources or silently substitute another record.
- **FR-027**: Context discovery, reuse and updates MUST respect access restrictions and minimize unnecessary exposure of sensitive customer or business material; copying sensitive content across scopes MUST require authorization.
- **FR-028**: The shared context contract MUST remain usable without a hosted database, vector search service, UI, agent orchestration platform or a published product skill.
- **FR-029**: The proposed context model MUST specify how existing project-state fields, templates, evidence records and product passport semantics remain readable or are migrated safely when implementation is later approved.
- **FR-030**: Repeated processing of unchanged context and equivalent inputs MUST not create conflicting identifiers, duplicate authoritative decisions or divergent claims without an explicitly documented reason.
- **FR-031**: The system MUST provide inspectable checks for malformed references, invalid canonical IDs, incompatible context scope, evidence/decision traceability, unauthorized mutation and missing handoff obligations.
- **FR-032**: Context quality and workflow progress MUST NOT be reported as verified solely because a passport, record or generated artifact exists.

### Key Entities

- **Workspace Context**: Long-lived shared knowledge space with purpose, membership/boundary, research evidence and links to zero or more opportunities/products; not necessarily a software product.
- **Opportunity Context**: Independently identifiable candidate problem/value opportunity with hypotheses, evidence, status and related workspace/product links.
- **Product Context**: Independently identifiable product or product candidate with its own scope, goals, strategy, constraints, lifecycle activity and references to relevant opportunities.
- **Context Entry Point**: Short, discoverable orientation view of a scoped context; references authoritative details rather than duplicating them.
- **Claim / Assumption**: A statement with evidence status and provenance; may be unverified, contradicted, inferred or superseded.
- **Evidence Record**: Traceable input or observation associated with claims and source/sensitivity scope; reuses existing evidence classifications.
- **Decision Record**: An explicit scoped decision, authority and rationale, with revision/review links.
- **Artifact**: Durable skill output linked to its owning context, dependencies and evidence; not proof of success on its own.
- **Context Revision / Change Proposal**: A candidate or accepted change with baseline identity, author/authority, status and affected records.
- **Handoff**: Bounded summary of a skill's inputs, outputs, unresolved matters and recommended next actions.
- **Relationship**: Explicit typed association allowing an evidence collection, opportunity or product to reference related contexts without transferring authority automatically.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In 100% of defined research-first acceptance cases, a new context can be created and resumed with no product idea, ICP, name or solution provided.
- **SC-002**: In a fixture with three opportunities and two product directions, all intended relationships are preserved and zero unrelated decisions are propagated between product scopes.
- **SC-003**: In a two-skill, two-session handoff scenario, the second skill identifies the previous output, its evidence basis, open assumptions and next relevant action without reconstructing the prior chat.
- **SC-004**: In every negative-evidence and inference fixture, unsupported claims remain explicitly unverified and both supporting and contradictory evidence references are retrievable.
- **SC-005**: In 100% of tested approved decision revisions, the prior decision, authority, rationale, evidence and affected-artifact links remain accessible.
- **SC-006**: In all tested stale-update and unauthorized-update cases, no accepted context data is silently overwritten; the conflict or denial is reported.
- **SC-007**: In all tested invalid cycle/phase, gate/decision and missing-reference cases, an actionable diagnostic identifies the scope and inconsistency without claiming successful verification.
- **SC-008**: In all tested missing-product, backtracking, deferred and stopped scenarios, no artificial product or mandatory linear lifecycle transition is created.
- **SC-009**: In all tested expired-review and restricted-evidence cases, stale/sensitive content is flagged or withheld according to its conditions, without inventing replacement evidence.
- **SC-010**: A maintainer can demonstrate an unchanged legacy project-state example remains readable or is safely migrated according to documented compatibility behavior; no silent data loss.
- **SC-011**: An end-to-end demonstration can execute the context contract without a database, hosted service, auto-orchestrator or installed product skill, and clearly separates static checks from runtime verification.

## Assumptions

- This is a **planned** foundation feature. No shared-context runtime protocol, required skill behavior or migration is implemented by drafting this spec.
- Canonical Product Model cycle/phase/track/loop/gate/decision/status IDs stay owned by `model/product-model.json`.
- The existing `EVIDENCE-MODEL.md`, `SKILL-CONTRACT.md`, `schemas/` and `templates/project-state/` are the compatibility baseline, not evidence that the future behavior already works.
- A compact human-readable entry point and inspectable machine-readable metadata are desirable; exact storage layout, filenames, schema fields and write mechanics belong to planning.
- Human approval is required for high-impact changes unless explicit delegated authority exists; permission infrastructure is not assumed to already exist.
- Research may yield zero, one or several opportunities; any opportunity may remain unpursued; product creation is optional.
- Context layers describe ownership/scope, not mandatory sequential maturity gates.
- Context provenance can be incomplete at entry, but incompleteness must remain visible and prevent unjustified confidence.
- Initial implementation should prioritize local, portable, reviewable artifacts; online synchronization, privacy enforcement integrations and migration mechanics require explicit design and verification later.
- Dependencies: Spec 001 (canonical lifecycle) and Spec 002 (skill identity/contract). Spec 004 compatibility rules may inform later rollout, but are not a prerequisite to record this specification.

## Recorded Product Decisions (Approved Design Direction)

The decisions below record the user-approved product direction; they are **requirements intent**, not evidence of implementation or acceptance.

| ID | Decision | Consequence |
| --- | --- | --- |
| D-001 | Shared context is cumulative knowledge, both input and output for skills. | No skill may assume context arrives complete. |
| D-002 | Research-first is a first-class entry point without a product idea. | Discovery must work with unknown name, ICP and product. |
| D-003 | Idea-first and existing-product entry points are equally valid. | No enforced front-to-back lifecycle. |
| D-004 | Workspace, Opportunity and Product are distinct context scopes, not mandatory stages. | One workspace may have many opportunities/products and explicit cross-links. |
| D-005 | The Product Model remains canonical for lifecycle vocabulary. | No alternate cycle/phase/status/gate/decision definitions. |
| D-006 | Evidence, assumptions, decisions and revisions are durable and traceable. | Preserve contradictions, historical reasoning and provenance. |
| D-007 | Product Passport is a concise entry point, not one giant mutable source of truth. | Keep detailed records separately, with stable references. |
| D-008 | Skills may contribute scoped artifacts/evidence, but may only propose unapproved strategic changes. | Authorized decision changes and conflict handling are explicit. |
| D-009 | Context handoff is cross-skill but does not itself orchestrate execution. | Workflows retain ordering authority; suggestions do not auto-run skills. |
| D-010 | Initial implementation should be proportional, local and portable. | No database, vector memory, UI or orchestration service requirement in v1. |
| D-011 | Freshness, scope protection and impact-aware revision are part of the contract. | Old data is flagged for review; sensitive content cannot spread by implication. |
| D-012 | Specification is recorded now; implementation can be deferred. | Do not claim a working context system or create product skills as part of this change. |

## Project Docs Impact

**Planned impact only — do not update implemented-truth docs before implementation and verification:**

- `docs/ARCHITECTURE.md` — extend authority diagram to distinguish workspace/opportunity/product context scope and read/write/handoff semantics.
- `PRODUCT-MODEL.md` — update explanatory text only if needed; machine Product Model authority must remain unchanged.
- `SKILL-CONTRACT.md` and `SKILL-MODEL.md` — introduce context-compatibility behavior without turning the registry into an orchestrator.
- `EVIDENCE-MODEL.md` / `QUALITY-GATES.md` — align traceability and readiness implications if contracts change.
- `templates/project-state/`, `schemas/project-state.schema.json`, `schemas/evidence.schema.json` — assess backward compatibility and progressive empty-context initialization.
- `README.md`, `README.vi.md` and onboarding examples — describe the new capability only after verification.
- `specs/ROADMAP-foundation.md` — record this proposal as planned truth now.

## Out of Scope

- Implementing schemas, validators, templates, skill code, workflows, agents, or migrations in the specification-only commit.
- Creating, adapting, installing or publishing the first product skill; the catalog remains empty.
- A second Product Model, mandatory three-stage pipeline, waterfall workflow or automatic lifecycle enforcement.
- Building a hosted service, database, semantic/vector store, dashboard, authorization provider or autonomous orchestration engine.
- Defining detailed filesystem layout, wire protocols, merge algorithms, encryption or platform-specific adapters at requirements stage.
- Rewriting current evidence or product history as if new customers had been interviewed or existing products verified.
- Claiming modeling, implementation, testing, real-world privacy guarantees or runtime PASS based on this spec.
