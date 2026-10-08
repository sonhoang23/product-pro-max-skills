# Design Quality Checklist: Product Pro Max Design System

**Purpose**: Reviewer-owned requirements-quality review of theme flexibility, accessibility, migration safety and asset compatibility  
**Created**: 2026-10-08  
**Feature**: [spec.md](../spec.md)  
**Review Ownership**: Items remain unchecked pending explicit reviewer quality evaluation. Checking them does not establish implementation or browser QA.

## Theme and token contract

- [ ] CHK001 Are required roles, variant coverage and precedence rules sufficiently specific to reject incomplete skins? [FR-001, FR-004, FR-020, FR-021]
- [ ] CHK002 Does the spec unambiguously distinguish Signal Lime brand accent from success/warning/error states? [FR-002, FR-007]
- [ ] CHK003 Are the rules for visual snapshots, revision stamping and visual-only invalidation measurable? [FR-017, FR-027]
- [ ] CHK004 Are allowed surface-specific deviations constrained rather than implicitly encouraging per-surface token forks? [FR-010–FR-012]
- [ ] CHK005 Are density behavior, typography minimums and long-language text outcomes covered? [FR-013, FR-016]

## Semantic integrity

- [ ] CHK006 Is gate-result vs decision distinction explicit even when display colors are identical? [FR-008]
- [ ] CHK007 Can a reviewer compare semantic labels, links, edges and source/truth status before/after migration? [FR-018]
- [ ] CHK008 Are decorative brand paths explicitly prohibited from implying canonical lifecycle relations? [FR-005, FR-026]
- [ ] CHK009 Is the modeling skill's WHAT authority distinguished from renderer HOW responsibility? [FR-023]

## Accessibility and environment

- [ ] CHK010 Are normal/large text and non-text contrast classes explicit for both baseline themes? [FR-014]
- [ ] CHK011 Are keyboard, focus, screen-reader labels and reduced-motion requirements testable independently? [FR-015]
- [ ] CHK012 Do viewport/zoom requirements permit scrollable technical diagrams without dropping text or arrows? [FR-016]
- [ ] CHK013 Do requirements define deterministic offline behavior when fonts/scripts/styles cannot be loaded? [FR-009, FR-013]
- [ ] CHK014 Does the GitHub README contract avoid assumptions about custom CSS or JavaScript execution? [FR-011]

## Migration and evidence

- [ ] CHK015 Are pilot, fallback and rollback boundaries explicit before broader migration? [FR-019, FR-025]
- [ ] CHK016 Does the spec define failures for missing, invalid and machine-global token/profile conditions? [FR-020, FR-021]
- [ ] CHK017 Are static, browser, GitHub and real publishing verification statuses independent? [FR-022]
- [ ] CHK018 Are out-of-scope platform/framework additions and Product Model rewrites excluded? [FR-024]

## Notes

- `[x]` is reviewer acceptance of **requirements quality only**, not working software or tests.
- `checklists/requirements.md` is a separate built-in specification-quality checklist.
