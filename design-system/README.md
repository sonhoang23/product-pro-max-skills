# Product Pro Max Design System

**Status:** Phase 1 documentation and design-reference registration only (Spec 003).
No token contract, exporter, renderer integration or production brand asset has been implemented.

## Approved concept (reference only)

- **Concept:** Signal Protocol — a one-file HTML visual showcase for theme, accent, density and diagram treatments.
- **Canonical preserved source:** [approved-showcase.html](../specs/003-product-pro-max-design-system/references/approved-showcase.html).
- **Source identity:** Git blob `c556747321f1f31bd6927b8af264a000f32638a3`, present at base commit `d78320a3bcce531db43a6e47ce16ab284ada64b0` on `main`.
- **Reference revision:** `concept-v1` (documentation label bound to the blob above, **not** a released `tokens.json` version).
- **Use:** Review the appearance and interaction direction only. Its sample labels, mock workflow outcomes and CSS declarations are not canonical requirements, role IDs, gate results or decisions. This file is not a schema, token authority or implementation test.

## Source-of-truth hierarchy

1. [Constitution](../.specify/memory/constitution.md) and [Spec 003 requirements](../specs/003-product-pro-max-design-system/spec.md) govern constraints and intended behavior.
2. [Implementation plan](../specs/003-product-pro-max-design-system/plan.md), [data model](../specs/003-product-pro-max-design-system/data-model.md) and [tokens/surfaces contract](../specs/003-product-pro-max-design-system/contracts/tokens-and-surfaces.md) govern planned design and validation.
3. `design-system/tokens.json` will be the **only canonical machine-readable presentation-token value source** after Phase 2 creates it. This README and the approved showcase must not independently define or override token values.
4. Product Model/Skill Registry and Spec Kit artifacts continue to own product semantics. `speckit-system-modeling-vi` decides what a diagram represents; `diagram-design-vi` decides how the derived presentation looks.

## Repository-local token workflow (Phase 2)

The single **implemented token value authority** is [tokens.json](tokens.json). This guide describes behavior and intentionally contains no copied role values. [Visual primitive mapping](components.md) defines presentation treatments but cannot redefine product meanings.

- Project-first loading: `scripts/verify_design_system.py` reads `design-system/tokens.json` from its repository root (override root explicitly with `--root`). Invalid/missing roles stop work; the code does **not** consult `~/.diagram-design`, the machine environment, or VibeToolPro style profiles.
- A resolved token output is a **visual derivative**, not a semantic artifact. It never carries, invents or modifies Gate/Decision source content, edge direction, Atlas registry fields, model IDs or task requirements.
- `readme` and `brand` default to Dark; `diagram` and `docs` to Light. Explicit theme and density are validated; no silent fallback to unknown variants.
- The checked-in token file declares stable role IDs, theme values, local font fallbacks and geometry multipliers. `accent-brand` is for brand presentation, **not** state/gate/decision text. The validator enforces text contrast >= 4.5:1 and selected informative non-text contrast >= 3:1; use dark informational text on a light accent.
- Phase 2 exports inline CSS variables (or CSS scoped to `svg.ppmax-design-system`) and embeds a token revision plus deterministic short SHA-256 fingerprint. Exported CSS is not a full SVG/HTML renderer. Integration with `diagram-design-vi` and fully standalone specimens are scheduled for Phase 4.

### Reproduce checks

```bash
python scripts/verify_design_system.py --check-tokens
python scripts/verify_design_system.py --surface diagram --theme dark --density spacious
python -m unittest discover -s tests -p 'test_design_system_tokens.py' -v
python scripts/export_design_tokens.py --check
python scripts/export_design_tokens.py --surface diagram --theme light --format css --output /tmp/ppmax-diagram.css
python scripts/export_design_tokens.py --surface diagram --theme light --format css --output /tmp/ppmax-diagram.css --check
python scripts/export_design_tokens.py --surface diagram --theme dark --format svg-css --output /tmp/ppmax-svg.css
```

The `--check` mode **never creates, rewrites or repairs output files**. Without `--output`, it validates deterministic generation without writing. With `--output`, it compares existing bytes and returns nonzero on missing/stale data. A normal `--output` write is staged then atomically replaced. Font values are local/system only; exports never fetch remote assets.

### Verification status contract

Never treat a check in one layer as proof of another. For each artifact/claim, report these independent fields:

| Evidence field | Permitted value | Required provenance |
| --- | --- | --- |
| `semantic_source` | `PASS / FAIL / BLOCKED / NOT_RUN` | source file/commit/hash, invariant IDs, comparer/check |
| `static_check` | `PASS / FAIL / BLOCKED / NOT_RUN` | exact command, exit, runtime/tool version, checked artifact hash |
| `browser_visual` | `PASS / FAIL / BLOCKED / NOT_RUN / UNAVAILABLE` | browser/version, viewport/zoom/theme, screenshot location, keyboard/accessibility coverage |
| `github_render` | `PASS / FAIL / BLOCKED / NOT_RUN` | live GitHub page URL, theme, revision and screenshot/test record |
| `actual_publishing` | `PASS / FAIL / BLOCKED / NOT_RUN` | deployed URL, commit/revision and observed outcome |

A missing run or missing run-specific log remains `NOT_RUN`, never PASS. The isolated Phase 2 Python evidence is [here](../specs/003-product-pro-max-design-system/phase-02-evidence.md); it is **not** a full checkout suite, browser review, GitHub README rendering or production verification.

**Next phase (not started):** T012–T017 user story skin permutations, semantic sample and screenshot verification.
