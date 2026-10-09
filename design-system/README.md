# Product Pro Max Design System

**Status:** Phase 1–3 design-token foundation implemented. Phase 4 diagram specimen + repository style adapter under verification; brand assets remain Phase 5.

## Approved concept (reference only)

- **Concept:** Signal Protocol — a one-file HTML visual showcase for theme, accent, density and diagram treatments.
- **Canonical preserved source:** [approved-showcase.html](../specs/003-product-pro-max-design-system/references/approved-showcase.html).
- **Source identity:** Git blob `c556747321f1f31bd6927b8af264a000f32638a3`, present at base commit `d78320a3bcce531db43a6e47ce16ab284ada64b0` on `main`.
- **Reference revision:** `concept-v1` (documentation label bound to the blob above, **not** a released `tokens.json` version).
- **Use:** Review the appearance and interaction direction only. Its sample labels, mock workflow outcomes and CSS declarations are not canonical requirements, role IDs, gate results or decisions. This file is not a schema, token authority or implementation test.

## Source-of-truth hierarchy

1. [Constitution](../.specify/memory/constitution.md) and [Spec 003 requirements](../specs/003-product-pro-max-design-system/spec.md) govern constraints and intended behavior.
2. [Implementation plan](../specs/003-product-pro-max-design-system/plan.md), [data model](../specs/003-product-pro-max-design-system/data-model.md) and [tokens/surfaces contract](../specs/003-product-pro-max-design-system/contracts/tokens-and-surfaces.md) govern planned design and validation.
3. `design-system/tokens.json` is the **only canonical machine-readable presentation-token value source**. This README and the approved showcase must not independently define or override token values.
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


## Phase 3 — reproducible visual variants (T012–T017)

The [semantic sample](../tests/fixtures/design-system/semantic-sample.json) is an **illustrative test fixture**, not a second canonical ontology. It contains stable node/edge IDs, source provenance, visible Gate-result/Decision labels and explicit presentation-only visual state roles. The source `warn` result does not automatically choose `REPEAT`.

Three committed, deterministic **CSS snapshots** live in [tests/fixtures/design-system/snapshots/](../tests/fixtures/design-system/snapshots/):

```bash
python scripts/export_design_tokens.py --surface readme --theme dark --output tests/fixtures/design-system/snapshots/default-dark.css --check
python scripts/export_design_tokens.py --surface diagram --theme light --output tests/fixtures/design-system/snapshots/light.css --check
python scripts/export_design_tokens.py --surface diagram --theme light --accent-preview '#35E2DF' --output tests/fixtures/design-system/snapshots/light-accent-preview.css --check
python -m unittest discover -s tests -p 'test_design_system_tokens.py' -v
```

`--accent-preview` is **only a decorative export-time alternate**. It does not edit `tokens.json`, choose business states, overwrite a machine-global profile, or create an official brand. Invalid hex is rejected. Outputs embed the canonical token revision and a content fingerprint; identical semantic + token inputs yield byte-identical presentation, while modified presentation values change the visual fingerprint alone. A stale snapshot makes read-only `--check` fail instead of rewriting bytes. Snapshot refresh is an explicit non-`--check` operation.

The validator checks token role completeness, specified informative contrast pairs and local font fallbacks; samples cover all four visual states and three density values. **Browser QA is independently scoped**: see [Phase 3 QA evidence](../specs/003-product-pro-max-design-system/qa-evidence.md). Six preview screenshots prove only a temporary CSS/typography/status-card harness at 1366/390px; they do **not** prove final diagrams, 200% browser zoom, screen-reader interaction, SVG/GitHub rendering or production publishing.

## Phase 4 — repository adapter and diagram specimen

- [Repository style resolver](../scripts/resolve_repo_style.py) maps existing `diagram-design-vi` paper/ink/accent/link primitive roles to validated local token roles, with **no fallback to home profiles**. The repo-specific instruction is documented at [adapter reference](../.agents/skills/diagram-design-vi/references/product-pro-max-adapter.md). Generic style-guide/profile files remain unchanged.
- [Specimen source](../tests/fixtures/design-system/semantic-sample.json), [light preview](../tests/fixtures/design-system/specimen-light.html) and [dark preview](../tests/fixtures/design-system/specimen-dark.html) are fixtures only, not living diagrams registered in Atlas. [Generator](../scripts/render_design_system_sample.py) preserves all source node/edge IDs and exact Gate vs Decision values; its geometry is fixed to this source sample, not a second general renderer.
- [Semantic/diagram tests](../tests/test_design_system_diagrams.py) enforce node/edge inventory, arrow direction, accessible title/desc, reduced-motion, source/truth labels, and tamper/no-write checks. See [QA evidence](../specs/003-product-pro-max-design-system/qa-evidence.md) for which browser checks were actually executed.
- Atlas and Spec 002 Feature Ledger have presentation-only token styling. Pilot migration of the *Spec 002 diagram itself* is reserved for Phase 6, after explicit approval. A derived style revision is not new implemented product architecture.

```bash
python scripts/resolve_repo_style.py --theme light
python scripts/render_design_system_sample.py --theme light --output tests/fixtures/design-system/specimen-light.html --check
python scripts/render_design_system_sample.py --theme dark --output tests/fixtures/design-system/specimen-dark.html --check
python -m unittest discover -s tests -p 'test_design_system_*.py' -v
```

## Phase 6 — reversible Spec 002 CSS migration

A strict CSS-only candidate is stored in [tests/fixtures/design-system/pilot/migrated-spec002.html](../tests/fixtures/design-system/pilot/migrated-spec002.html). Exact rollback markup lives alongside it as `original-spec002.html`. [Migration procedure](../specs/003-product-pro-max-design-system/migration-baseline.md) checks the original Git blob and rejects any source, graph, text or backlink mutation. Styling chooses Light/Dark using media queries, no JavaScript and no external CSS/fonts.

The candidate is a review fixture; links are relative to the original diagram directory and must be checked on the **promoted original path**. Promotion is conditional on independent source parity and browser/official validator results, not on CSS generation alone. The Diagram Atlas and Feature Ledger preserve existing parent/child/related, `scope`, `truth=planned` and registry filenames.

## Phase 7 verification record

See [integrated QA evidence](../specs/003-product-pro-max-design-system/qa-evidence.md) and [GitHub Actions Validate](https://github.com/sonhoang23/product-pro-max-skills/actions/runs/37873888264). Brand assets passed deterministic snapshot checks and actual GitHub Light/Dark README previews. Spec 002 is an accepted reversible CSS-only pilot; its graph registry and planned truth remain unchanged. The only known open verification layer is native browser UI zoom and full convergence (T026/T045/T055), which must not be confused with Chromium CDP compositor 200% scaling.

## Atlas and Feature Ledger skin synchronization

`scripts/export_navigation_styles.py` deterministically resolves Light/Dark styles for `docs/diagrams/index.html`, Spec 002 and Spec 003 Feature Ledgers. All role values come from `design-system/tokens.json`; token revision is recorded on each HTML root, while existing source/graph links, labels, and `planned` diagram truth stay unchanged. `--check` is read-only and detects token-value/style drift before publishing.

```bash
python scripts/export_navigation_styles.py --check
python scripts/export_navigation_styles.py          # explicit regeneration if canonical tokens change
```

The Atlas/ledgers are navigation surfaces, not semantic sources or product-status monitors. They may show `planned` for a spec-time diagram even when an implementation has since been committed and verified.

## Spec 003 closure

The repository-native Signal Protocol design system is implemented with 55/55 verified tasks, immutable canonical token authority, native Chromium 200% keyboard zoom evidence, GitHub Light/Dark README previews, and a reversible CSS-only pilot. The final modeling/converge gate is `no-diagram-needed` (no unresolved semantic gap requiring an additional diagram). Full evidence and QA limits: [Spec 003 acceptance record](../specs/003-product-pro-max-design-system/qa-evidence.md).

## Current README hero: process overview

The approved `assets/brand/hero-process.webp` is the GitHub README banner in **both** reader color schemes. It has its own dark background, is self-contained, requires no script or remote font, and presents six illustrative milestones: Discover, Define, Build, Verify, Launch, Improve. This graphic is an editorial overview rather than a second canonical lifecycle or new semantics: the complete official cycles remain in [model/product-model.json](../model/product-model.json). The earlier `hero-light.svg` and `hero-dark.svg` remain available as token-derived brand examples, but are no longer displayed as the README cover. See `tests/test_design_system_release.py` and the GitHub browser capture check for asset acceptance.
