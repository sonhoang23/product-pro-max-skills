# Feature Specification: Product Pro Max Design System

**Feature Branch**: `main` (Spec Kit artifacts committed at `7e45f67`; implementation not started)  
**Created**: 2026-10-08  
**Status**: Reviewed draft — specification and planning artifacts committed; local modeling QA deferred, no implementation  
**Spec modeling**: [Semantic/presentation boundary](spec-diagram/presentation-boundary.html) · [Feature Diagram Ledger](diagrams.html) (planned truth only).

**Input**: Adopt approved **C — Signal Protocol** visual direction with **Signal Lime** as the prominent accent and a **Signal Path + Wordmark** brand mark, covering **Core + Brand Assets**. Design must remain flexible, self-contained where necessary, and presentation-only.

## User Scenarios & Testing

### User Story 1 — Change the visual skin without changing meaning (Priority: P1)

As a repository maintainer, I want one coherent set of configurable visual roles so I can update colors, theme, typography, or density without rewriting individual diagrams or changing their meaning.

**Why this priority**: Theme independence is the principal architectural requirement, not a cosmetic extra.

**Independent Test**: Change the approved accent and switch Light/Dark on the same example; verify all represented entities, relationships, statuses and source links remain identical, without editing the example's semantic content.

**Acceptance Scenarios**:

1. **Given** a diagram created with the default Signal Protocol theme, **When** the accent/theme changes, **Then** its semantic labels, edge directions, gate results, decisions, and references do not change.
2. **Given** a reusable visual primitive, **When** a maintainer adjusts visual roles centrally, **Then** a newly produced README/diagram/docs/brand preview uses the change without per-output hand editing.
3. **Given** a generated output must open without network access, **When** it is opened offline, **Then** presentation remains legible and functional without remote fonts, scripts, or CSS.

### User Story 2 — Read trustworthy and accessible technical diagrams (Priority: P1)

As a reader, I want diagrams and the Diagram Atlas to look consistent while explicitly distinguishing nodes, connectors, boundaries, evidence, gate results, and decisions, so I can understand the system without misreading visual emphasis as business authority.

**Why this priority**: Diagram readability and semantic integrity are more important than brand decoration.

**Independent Test**: Render the current Spec 002 semantic relationship as a pilot, compare semantic inventory and links before/after, inspect it in light mode on desktop and narrow viewports, and validate keyboard and accessible labeling.

**Acceptance Scenarios**:

1. **Given** a gate result `warn`, **When** it is displayed, **Then** it is labeled as a gate result and is not presented as a workflow decision or an automatic `revise` action.
2. **Given** two valid decisions may follow the same gate result, **When** either decision is rendered, **Then** visual treatments do not invent a one-to-one mapping from gate result to decision.
3. **Given** the Diagram Atlas contains a planned feature diagram, **When** users open it, **Then** `planned` vs `implemented` remains explicit and navigation/source backlinks remain available.
4. **Given** a narrow viewport or reduced motion preference, **When** the diagram is used, **Then** all essential information remains accessible, with neither animation nor color alone conveying meaning.

### User Story 3 — Produce coherent README and brand assets (Priority: P2)

As a contributor, I want recognizable Signal Protocol assets that render correctly on GitHub and remain reusable in docs and social graphics.

**Why this priority**: Public identity should match the diagram system without requiring a website or a frontend framework.

**Independent Test**: Compare the logo lockups and README hero in Light/Dark GitHub contexts, with alt text, usable SVG fallbacks, and correct rendering when external resources are unavailable.

**Acceptance Scenarios**:

1. **Given** the project's signature identity, **When** a README hero or brand cover is produced, **Then** it uses the Signal Path symbol and Product Pro Max Skills wordmark consistently.
2. **Given** GitHub displays a light or dark reader theme, **When** the README hero is rendered, **Then** the appropriate theme variant is visible without client-side script.
3. **Given** the brand accent is updated, **When** assets are regenerated, **Then** source identity/layout can be retained while the color system changes centrally.

### User Story 4 — Safely adopt the design system in existing assets (Priority: P2)

As a maintainer, I want a controlled migration of legacy diagrams and generator defaults so I can adopt the design system without breaking existing files or overstating QA.

**Why this priority**: Existing planned-truth diagrams, Atlas entries and repository-development skills already work and must not regress.

**Independent Test**: Migrate a copy of the Spec 002 pilot, compare node/edge/label/link inventories, run existing validators and visual QA; preserve the original if any required check fails.

**Acceptance Scenarios**:

1. **Given** a previously published standalone HTML diagram, **When** the migration is tested, **Then** the migrated copy retains its semantic statements, artifact authority labels, HTML opening behavior, and navigation relationships.
2. **Given** an invalid theme role or missing asset, **When** an output is generated, **Then** the process fails with an actionable error or uses an explicitly documented safe fallback; it never silently switches to an unrelated brand profile.
3. **Given** a migration has only passed static checks, **When** its readiness is reported, **Then** it is not labeled browser-verified.

### Edge Cases

- Accent/background pairs that fail contrast; focus, selected, warning and error states with indistinguishable appearance.
- Some outputs require SVG files while standalone HTML embeds all necessary presentation resources; neither may depend on third-party font hosting.
- Long Vietnamese text, narrow screens (including 390px), user zoom 200%, print/export, and assistive-technology labels.
- A theme role is absent, malformed or renamed; existing output is viewed after the source token file changes.
- A generator is run from a different machine without the same home-directory profile or network access.
- Token changes affect a diagram snapshot's visual fingerprint but not its Spec Kit semantic source fingerprint.
- Gate results `pass/warn/fail` and decisions including `continue/research/revise/pivot/repeat/backtrack/defer/stop/escalate` must not be conflated.
- A README banner or poster uses a decorative route motif that could be mistaken for canonical product lifecycle order; decoration must never claim domain authority.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST establish one repository-owned authoritative source for presentation tokens with stable semantic role names.
- **FR-002**: The default visual identity MUST be **Signal Protocol** with a prominently visible **Signal Lime** brand accent, dark hero treatment, and light-first technical-diagram treatment. Brand accent MUST remain distinct from success/warning/danger status meanings, even if colors happen to match.
- **FR-003**: The visual identity MUST include a consistent **Signal Path symbol + Product Pro Max Skills wordmark**, with compact and full lockups appropriate to context.
- **FR-004**: The visual system MUST support Light and Dark themes, `compact`/`default`/`spacious` density and a deliberately scoped alternate-accent preview without changing content semantics or layout responsibilities. Density changes MUST NOT hide required labels, edges, legends, decision outcomes or source references.
- **FR-005**: Presentation customization MUST keep source semantics and presentation preferences independent; changes to theme, contrast or density MUST NOT mutate the Canonical Product Model, Skill Model, registry, or diagram source authority.
- **FR-006**: Token roles MUST cover color/surfaces/text, typography, spacing, borders/radius/strokes, focus/interaction affordances, and semantic status states.
- **FR-007**: Shared diagram primitives MUST include node, connector, boundary, gate result, decision, evidence, and feedback path, with labels and treatments that can be distinguished without reliance on color alone.
- **FR-008**: Diagram visuals MUST preserve the distinction between gate-result vocabulary and workflow decision vocabulary. Presentation MUST NOT invent relationships or transitions.
- **FR-009**: Standalone canonical HTML diagrams MUST retain functional layout, labels, and necessary styles without external network access.
- **FR-010**: The Atlas, Feature Ledger and individual diagrams MUST share visual roles without losing planned/implemented labels, source traceability, navigation or registry semantics.
- **FR-011**: README hero assets MUST render within GitHub's permitted Markdown/HTML/SVG behaviors and support light/dark reader preference without script dependency.
- **FR-012**: Documentation and exported brand assets MUST follow the same canonical visual roles while allowing surface-specific hierarchy and composition. Surface-specific treatments MUST use documented aliases/overrides of those roles, not independent or untracked token-value forks.
- **FR-013**: Typography MUST remain readable for English and Vietnamese without remote font prerequisites; a supported fallback stack MUST be provided. Essential browser-diagram labels MUST be at least 12 CSS px at default (100%) presentation scale, and changing density MUST NOT reduce them below that minimum; non-essential decorative labels may use smaller type only when they carry no unique information.
- **FR-014**: Relevant informative text MUST meet at least WCAG AA contrast (4.5:1 normal text, 3:1 large text), and meaningful non-text visual boundaries/icons MUST meet at least 3:1 where applicable.
- **FR-015**: Interactive outputs MUST support keyboard navigation, visible focus, programmatic names, sufficiently sized or spaced targets, and reduced-motion preferences; essential meaning MUST remain available without animation. Keyboard order, accessible name, focus visibility and motion fallback MUST be independently verifiable for every interactive control.
- **FR-016**: Narrow layouts MUST avoid losing content or relationships: responsive reflow and/or clearly accessible diagram scrolling/zooming MUST be provided where needed.
- **FR-017**: One theme switch MUST consistently affect all target surfaces that are generated from the same token revision, subject to documented output-specific constraints. Outputs carrying an older presentation revision MUST be detectable as visually stale without asserting that semantic source content has changed.
- **FR-018**: Existing diagram semantics, node/edge inventory, authority annotations and links MUST remain intact during visual-only migration unless the authoritative upstream artifact changes separately.
- **FR-019**: Migration MUST begin with the existing Spec 002 diagram and Atlas as a controlled pilot and preserve a revertible original until verification completes.
- **FR-020**: The system MUST expose an explicit precedence/fallback rule for theme, profile and token resolution; it MUST NOT silently inherit a developer's unrelated machine-global brand skin. Missing, malformed or incomplete repository tokens MUST cause an actionable failure and preserve existing outputs rather than silently falling back to that global skin.
- **FR-021**: The system MUST validate that required roles exist, supported color values are valid, contrast targets are met, and token resolution is deterministic for equivalent inputs.
- **FR-022**: Validation results MUST distinguish static validation, screenshot review, browser functional verification, and actual asset publishing; lack of evidence MUST NOT be reported as PASS.
- **FR-023**: Presentation design documentation MUST be discoverable by repo contributors and consumed consistently by `diagram-design-vi` while leaving `speckit-system-modeling-vi` responsible for **what** to visualize.
- **FR-024**: The design system MUST NOT introduce a React app, online asset service, database, independent diagram semantics engine, or second product ontology for its initial scope.
- **FR-025**: Existing generated diagrams MUST remain readable if no migration is performed; migration is opt-in by artifact until validated.
- **FR-026**: Approved showcase variations MUST be treated as a visual reference, not as executable semantic authority; mock example values MUST not redefine canonical gate/decision terms.
- **FR-027**: The implementation MUST maintain a clear version or revision identity for theme tokens in each derived output. An unchanged semantic source combined with changed token revision MUST flag only visual presentation staleness; a re-export from identical semantic and token inputs MUST yield the same presentation revision/identity.

### Key Entities

- **Design Token**: Named presentation role with value and supported theme variations; not a domain concept.
- **Theme/Brand Skin**: Named set of token values satisfying stable role contracts; Signal Protocol is the default.
- **Visual Primitive**: Presentation rendering rule for a shape/connection/label; input semantics are supplied by source artifacts.
- **Surface**: Output context (README, HTML diagram/Atlas, documentation, brand asset) with capability/format constraints.
- **Brand Asset**: Approved SVG/graphic derivative from symbol, wordmark, and presentation tokens.
- **Visual QA Evidence**: Scope, result, tool/viewpoint and freshness of layout/accessibility/behavior review; separate from semantic modeling evidence.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A single approved theme switch produces legible variants for all four named output surfaces without modifying their canonical content or source semantic fields.
- **SC-002**: The Spec 002 migration pilot retains **100%** of reviewed semantic labels, directed relationships, source/Atlas links, and planned/implemented annotations (except explicitly reviewed non-semantic presentation changes).
- **SC-003**: **100%** of sampled normal informational text and applicable significant icons/boundaries meet defined contrast thresholds across baseline Light and Dark themes.
- **SC-004**: Default and alternative variants remain usable at desktop and 390px viewport, at 200% browser zoom where applicable, with no inaccessible essential content.
- **SC-005**: A reviewer can distinguish gate results from decisions correctly in **all** specified samples without depending on color.
- **SC-006**: A contributor can produce and verify a standalone HTML diagram and GitHub-compatible README hero using documented repository-local resources with no network requirement.
- **SC-007**: All new visual outputs have traceable token revision and truthful QA state; no unsupported browser-verification claims are present.

## Assumptions

- Existing Spec 001/002 machine semantics and repository-development vs distributable-skill boundaries remain unchanged.
- Approved Signal Lime is the default brand accent; alternate colors are a demonstration of token-driven flexibility, not additional official brands.
- Dark is the primary presentation for hero/brand, Light for readability-heavy diagrams; both are supported wherever practical.
- The HTML showcase already approved is a **concept reference**, not a source schema or proof of production QA.
- The design system is repository-level development support; it is **not** a new distributable `ppmax-` skill.
- Repository content and canonical machine identifiers remain English/global-first; existing modeling policy may render labels in natural Vietnamese.
- Source/derived artifact relationships in Diagram Atlas remain as defined by existing modeling skill.

## Out of Scope

- Rewriting Product Model, Skill Manifest Registry, workflow behavior or canonical gate/decision vocabularies.
- Building a component framework, app shell, hosted documentation site, Figma sync, or design-token SaaS.
- Migrating every legacy diagram before the initial pilot is proven.
- Creating a new diagram renderer or replacing existing 39 `diagram-design-vi` diagram types.
- Treating visual preferences as a new Spec Kit authority layer or changing Lazy Modeling Gate semantics.

## Project Docs Impact

Planned promotion after verified implementation only: `docs/ARCHITECTURE.md` (presentation authority boundary), `docs/diagrams/index.html` and `docs/diagrams/diagram-index.json` (visual navigation without semantic change), README assets/links, `.agents/skills/diagram-design-vi/` integration instructions; no change to `model/product-model.json` or `registry/skills.json`.

**Roadmap compatibility**: Renumbering was committed in `specs/ROADMAP-foundation.md` at `7e45f67`: Design System uses 003; former versioning-compatibility uses 004; subsequent backlog moves to 005–008. No Product Model or Skill Registry IDs changed.
