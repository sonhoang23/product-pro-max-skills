# Spec 003 — Local QA evidence and follow-up fix

**Date:** 2026-10-09  
**User environment:** Windows PowerShell, Python 3.13.3, PyYAML 6.0.2, Edge, local checkout of `main`.  
**Tested HEAD:** `1ab9a6c`; QA screenshots and log supplied in the conversation.  
**Status:** Partial local QA evidence; **NOT** a complete modeling gate PASS.

## Actual reported local results

| Check | Result | Evidence |
| --- | --- | --- |
| `self_check.py`, Spec 002 relation diagram | PASS | `OK specs/002-.../skill-metadata-relations.html` |
| `self_check.py`, Spec 003 presentation boundary | FAIL | `svg 1 title/desc IDs must be diagram-prefixed, never bare` |
| `self_check.py`, Spec 003 token resolution | FAIL | Same missing diagram-specific title/desc ID constraint |
| `scripts/verify-diagram-atlas.py` | PASS | 3 registered diagrams; links and sources checked |
| `scripts/verify-diagram-layout.py` | PASS | 3 static SVG diagrams; browser visual QA excluded |
| `scripts/verify_skill_registry_release.py` | PASS | 35/35 unit tests, 13 canonical skills, 3 workflows; 13 dry-run selections |
| Desktop browser screenshots | Viewed | Atlas and both Spec 003 diagrams visible at desktop width; no obvious overlapping nodes, missing SVG elements or clipping |
| Mobile 390px, 200% zoom, keyboard/tab/navigation, screen reader | NOT VERIFIED | No run-specific evidence received yet |

## Fix applied after log

- `spec-diagram/presentation-boundary.html`: rename SVG accessible title/desc IDs to `ppmax003-boundary-title` and `ppmax003-boundary-desc`, update `aria-labelledby`.
- `plan-diagram/token-resolution.html`: rename IDs to `ppmax003-token-resolution-title` and `ppmax003-token-resolution-desc`, update `aria-labelledby`.
- No changes to diagram node/edge structure, source-of-truth text, project Product Model, registry or Diagram Atlas relationships.
- This change is **not** a claim that `self_check.py` was successfully rerun on Windows after the fix.

## Remaining actions

1. `git pull --ff-only origin main`.
2. Rerun self-check on all 3 diagrams, `verify-diagram-atlas.py` and `verify-diagram-layout.py` on updated HEAD.
3. Confirm 390px width (scrollable diagram not clipped), 200% browser zoom, Tab focus and navigation links in the actual Edge browser.
4. Record the new exit codes and screenshot results. Gate may be reconsidered only with evidence and source freshness checks.

**Gate state:** `spec=blocked`, `plan=blocked` until required validation is complete. All implementation tasks remain unchecked.
