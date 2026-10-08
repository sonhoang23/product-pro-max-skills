# Research: Product Pro Max Design System

**Date**: 2026-10-08 | **Scope**: repository design; no implementation/benchmark claims.

## Existing sources reviewed

- `model/product-model.json` + `docs/ARCHITECTURE.md`: canonical product semantics; `pass/warn/fail` are gate results, not workflow decisions.
- `.agents/skills/diagram-design-vi/SKILL.md` and `references/style-guide.md`: renderer and named token roles already exist; current custom skin describes **VibeToolPro**, not Product Pro Max.
- `.agents/skills/diagram-design-vi/references/profiles.md`: supports machine-local client profiles and an optional project marker; cannot be the *only* repo-wide canonical token authority because home profiles differ per author.
- `.agents/skills/speckit-vi-skills/speckit-system-modeling-vi/SKILL.md`: distinguishes WHAT/source of truth from HOW, contains Lazy Modeling Gate, scope/truth and Atlas contracts.
- Existing `docs/diagrams/index.html`, `docs/diagrams/diagram-index.json`, and `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html`: current single confirmed registered diagram and existing standalone HTML approach.
- Existing `scripts/verify-diagram-atlas.py` / `scripts/verify-diagram-layout.py`: static checks and visual QA evidence must remain distinguishable.
- Approved one-file interactive HTML showcase in conversation: reference for aesthetic, theme controls and component examples, not a canonical technical or domain schema.

## Decisions

### D-01 — Repository-local canonical JSON tokens

**Decision**: `design-system/tokens.json` owns values and stable role IDs. Documentation lists behavior, never forks the value table.  
**Reason**: Single tracked authority makes skin changes reviewable and reproducible.  
**Rejected**: copy values into README, style guide, HTML templates and global profiles independently.

### D-02 — Presentation alias + surface defaults

**Decision**: internal primitive roles (`surface`, `text-primary`, `focus`, `node-border`, `evidence-accent`, etc.) resolve to Light/Dark values; README hero defaults Dark and diagram defaults Light. A theme opt-in may override the default.  
**Rejected**: hardcoding Signal Lime in every primitive or using color names as semantic Gate/Decision IDs.

### D-03 — Static export instead of runtime fetch

**Decision**: HTML/SVG outputs embed their resolved styles and token revision; regeneration refreshes their visual snapshots.  
**Reason**: Offline, `file://`, GitHub and archival use.  
**Rejected**: fetching remote CSS/Google Fonts or a network token service.

### D-04 — Existing authoring skills, no new skills

**Decision**: `speckit-system-modeling-vi` remains authoritative for diagram scope/semantics; `diagram-design-vi` consumes repo tokens using a narrow repo-aware adapter/mapping. Do not replace its 39 type references or overwrite the user's global client profiles.  
**Rejected**: new diagram framework, another skill containing independent semantics, or a universal home profile requirement.

### D-05 — Explicit status shapes and labels

**Decision**: node silhouettes/labels distinguish evidence, gate results, decisions, boundaries and feedback loops; status color is secondary redundancy.  
**Reason**: Avoid misreading the visual system and meet non-color accessibility requirements.  
**Rejected**: green always equals `pass` always equals `continue`.

### D-06 — Pilot-first migration

**Decision**: use Spec 002 relationship diagram and Atlas as pilot; preserve source semantics and links; run static/visual QA; only then migrate other diagrams.  
**Rejected**: bulk search/replace of CSS across all repo diagrams.

### D-07 — GitHub native surfaces

**Decision**: SVG hero variants with Markdown/`picture`-compatible embedding and alt/fallback, no JavaScript on README.  
**Rejected**: HTML/CSS hero requiring GitHub to execute custom stylesheet/script.

### D-08 — Revision and compatibility

**Decision**: stable token role IDs plus a token revision in derived outputs; visually stale outputs need regeneration, not re-modeling of source meaning. Reserve role renames for a later compatibility policy; no new versioning feature here.  
**Rejected**: mixing rendering freshness with semantic source hash.

## Open technical verifications for implementation

- Confirm CSS/SVG GitHub rendering in actual light/dark themes before claiming browser/GitHub pass.
- Confirm English/Vietnamese font fallback metrics, responsive long-label handling, and print capture with chosen visual style.
- Determine which existing generator reference snippets contain hard-coded hex values and how minimal adapter changes can override them safely.
- Review any `main` changes before applying this staged design, especially Spec 003 number and Diagram Atlas inventory.
