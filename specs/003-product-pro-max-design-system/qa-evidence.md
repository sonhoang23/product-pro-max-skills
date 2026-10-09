# Spec 003 — Phase 3 scoped QA evidence

**Date:** 2026-10-09  
**Base source:** GitHub `main` at `14a3b5fc420dc6e918c65df618eff883e52cf2d2`.  
**Feature:** `003-product-pro-max-design-system` · Phase 3 T012–T017 only.  
**Truth:** planned semantic fixture plus implemented token exporter/test behavior. No changed Product Model/Skill Registry or living diagrams.

## Source / snapshot evidence

- Semantic fixture: `tests/fixtures/design-system/semantic-sample.json` · Git blob `29c1fcad064a3430ebf2e453ccce0abfd7d1833f` · SHA-256 `b9f2edeeb7693a97d6e608ef603d0bc97b41a9de059e63098d20931739f12dd6`.
- Tokens unchanged: `design-system/tokens.json` · blob `bf07abd8c0e93282c9bb15727fdbe711f4cd45f9` · revision `0.1.0`. Canonical `spec.md` blob remains `9cd5bac5b00e1d1759e33ba1f14be5cfc6dae4ac` (GitHub source inspection).
- Snapshot blobs:
  - `default-dark.css`: `0590a0c92f54ea61aa1a02a08238d9f30910588e` · visual fingerprint `2e8e64f6edc41a3c`.
  - `light.css`: `9d8aeb66a8eb0b14cc57431721f483857d59c1a3` · visual fingerprint `2e8e64f6edc41a3c`.
  - `light-accent-preview.css`: `a0f3e142cf900413c0d3d8c2b67807f68aef922a` · visual fingerprint `0524ca079864f0c0`.
- Changed Python sources match Git blobs exactly: `verify_design_system.py` `d029ced02c42c9d103d5a4102d951d7ab9a01413`; `export_design_tokens.py` `3d40cea467f6ae4e22b83e044f6357fe336c7b72`; `test_design_system_tokens.py` `c61f67ac8cf91408f33aef311a9b08f246e61d05`.

## Executed test evidence (isolated Python 3.13.5)

| Actual check | Result / boundary |
| --- | --- |
| `python -m unittest discover -s tests -p 'test_design_system_tokens.py' -v` | **PASS 19/19**, 3.989 seconds, after fixing an initial incorrect fixture keyword invocation |
| `python -m compileall -q scripts tests` | **PASS** |
| Three exporter commands with `--output ... --check` | **PASS 3/3**, no snapshot write |
| Negative state and label cases | **PASS**: unknown `pass`/other role rejected; empty/whitespace/null visible state label rejected |
| Official theme contrast | **PASS** for validator's designated text and meaningful non-text combinations on Light/Dark; deliberate dark `text-secondary=surface` rejected |
| Density/font | **PASS** for 3 density token configurations; >=14px label/caption/body floors and local generic fallbacks |
| Alternate accent | **PASS**: valid hex changes visual fingerprint, invalid CSS rejected, no canonical token or semantic fixture mutation |
| Gate/Decision independence | **PASS** fixture assertion: separate values and types, no fabricated `gate-result → decision-selected` relation |
| Full repository tests | **NOT_RUN**: network-unavailable GitHub clone, only relevant sources staged locally |

Measured minimum of sampled role-to-surface ratios: Light **6.16:1**, Dark **9.64:1**; not a complete browser/whole-component WCAG audit.

## Browser screenshot evidence (Chromium 144.0.7559.96)

A *temporary local-only stylesheet QA harness* generated cards directly from the unchanged semantic fixture and scoped exported CSS to specimen panels. It is **not** the canonical HTML/SVG diagram renderer (scheduled Phase 4), and no production/GitHub asset was tested.

All six screenshot captures report 5 visible nodes, no document horizontal overflow (`scrollWidth <= innerWidth`), and rendered CSS font chains `"Segoe UI", Arial, sans-serif`. Captures used `page.set_content` after `file://` navigation returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`; therefore local `file://` behavior is **NOT VERIFIED**.

| Variant | Viewport | Screenshot SHA-256 | Observed caption / density |
| --- | --- | --- | --- |
| Light | 1366×900 | `ff30ebb4ac00aeaf59c30c7ae5a8c282ba1592c9681f513143b666cbab0f49c8` | Light/default, 14px label |
| Light | 390×844 | `dec3181c92be201616211b293b25a6d8dd5b76ee5182d9f6e9c4541aec96cd5d` | Light/default, no overflow |
| Dark | 1366×900 | `d006ce3570f9a9439124f98d23eccda191f3468611af04df1d6316a964fc5a2a` | Dark/spacious, 15.4px label |
| Dark | 390×844 | `a039566a8ee6b45f18776098804f80c8a13c0fe2513a25d195703b82f1d71cee` | Dark/spacious, no overflow |
| Accent preview | 1366×900 | `b3fceb52e94ae6f6ba081bb6da595225e1db665e0d36b3c75a47c0b422fa9470` | Light/compact, preview accent |
| Accent preview | 390×844 | `56ebf6decaeac1d8fec6aeb3dc6019dcbea6d489a0f90f84ac6ccb7ae97c2a80` | Light/compact, no overflow |

**Visual review:** inspected Light at 390px, Dark at 1366px, accent preview at 390px. Labels, card borders, status caption differentiation and viewport fit were legible in those three captures. The other three captures were programmatically inspected for presence/overflow but not manually reviewed pixel-by-pixel. All six screenshots, machine metrics and reproduction harness were delivered separately as a conversation ZIP artifact; screenshots are **not Git-tracked** here.

## Separate verification dimensions

| Dimension | Status |
| --- | --- |
| `semantic_source` | **PASS, limited:** fixture byte hash unchanged through theme/accent; Spec canonical blob unchanged |
| `static_check` | **PASS, isolated:** 19 unit tests, byte-matched Git blobs, snapshot `--check`, compileall |
| `browser_visual` | **PARTIAL PASS:** 6 captures on temporary CSS harness, 3 manually visually reviewed; not the final diagram |
| `github_render` | **NOT_RUN:** brand README assets belong to Phase 5 |
| `actual_publishing` | **NOT_RUN** |
| Real browser zoom 200%, screen reader and file:// navigation | **NOT_RUN / BLOCKED**; future acceptance tasks |
| Full repository / Atlas / diagram self_check rerun | **NOT_RUN**; no registered diagrams or Atlas changed |

**Decision:** T012–T017 are complete within their Phase 3 **style-fixture and scoped screenshot** scope. Do not call this full diagram QA or a runtime/product verification PASS. Phase 4 T018–T026 remains untouched; formal diagram/browser/semantics parity checks are still required.

## Phase 4 incremental QA — 2026-10-09

**Base:** GitHub `main` commit `89a75e8116a26e137826948f5589764e38abf9fe`; scope T018–T025 delivered. **T026 remains open**; source implementation is not equivalent to full browser acceptance.

### Implementation/source inventory

- Repo-aware style resolver: `scripts/resolve_repo_style.py` · Git blob `96094b6c781c94d1b0a189037d6bd36c38785927`; mapping belongs to `.agents/skills/diagram-design-vi/references/product-pro-max-adapter.md`, with repo-only precedence documented in `SKILL.md`. No global home-profile write.
- Fixture-only HTML generator: `scripts/render_design_system_sample.py` · Git blob `b1e444fa479422f22479efd9d16d9a2fd83ee812`.
- Source-preserving tests: `tests/test_design_system_diagrams.py` · Git blob `38e6810147ec0f3278cc6d92b64ef38d7e20699f`.
- Generated fixture snapshots: `tests/fixtures/design-system/specimen-light.html` · blob `403ed14a5df963730f58bded77e94b2afc539da0`; `specimen-dark.html` · blob `cf7477d499d69ca06f7324653ff10b36c9b1e4c3`. Rendered from the unchanged source fixture and canonical tokens revision `0.1.0`; they are **not** living diagram registry entries.
- Atlas and Spec 002 Ledger received presentation-only inline token roles. Targeted GitHub source diff preserved all pre-existing HTML navigation `href` destinations; the canonical `docs/diagrams/diagram-index.json`, original Spec 002 diagram and product ontology were not modified.

### Executed checks — isolated Python 3.13.5

`python -m unittest discover -s tests -p 'test_design_system_*.py' -q` → **26/26 PASS** after one correction of an overlapping edge label. Includes semantic node/edge parity (5/5 nodes, 2/2 source edges), no Gate-to-Decision invented relation, malformed input/unknown role rejection, typed state/status text, HTML title/desc and focus, no-write snapshot drift, external HOME profile attack fixture, theme/density determinism.

`python -m compileall -q scripts tests` → **PASS**. `python -O scripts/render_design_system_sample.py --check` → **PASS** (fixture assertions replaced with fail-closed TokenError checks). Local working source Git SHA matched all three code blobs above, and both fixture HTML blobs matched emitted output.

### Chromium browser visual evidence

Headless Chromium in an isolated container, `page.set_content` for each generated HTML snapshot, `prefers-reduced-motion:reduce`. Six screenshots captured and archived in the conversation artifact `ppmax-spec003-phase4-browser-qa.zip`; **screenshots not committed**. Actual file navigation, full checkout and GitHub README render were not executed.

| Variant | Viewport / zoom | Browser observations | Screenshot SHA-256 |
| --- | --- | --- | --- |
| Light | 1366×900 / 100% | 5 nodes, 2 directed edges; document width 1366; no horizontal overflow | `5db1e7731c66fa3e1cf8d8e251bd10a1a6862c0d1d2f8c0f9530bcb818cb53dd` |
| Light | 390×844 / 100% | document width 390; internal panel width 355, content 1120; ArrowRight scroll +37px | `58290c14d00791ef4fecfa7fc600c2e570fc4d5e2c3951f04decfe2b85fadcb9` |
| Dark | 1366×900 / 100% | 5 nodes, 2 directed edges; no document horizontal overflow | `3c2b33a5ba9c2c05d28ca7ecd9daae6ddfee9358330a188d2beaf21c2d4c316b` |
| Dark | 390×844 / 100% | document width 390; panel scroll +36px on ArrowRight | `a5c23af358d7192749a6f147d23dc046af8d593beb4c3db28ca384667738da62` |
| Light | 1366×900 / CSS zoom 200% simulation | document still width 1366; internal panel scrollable | `8838b726dae57516d2be34427ac861cb1398a5e85b47d4dba1f625f938d85b70` |
| Dark | 1366×900 / CSS zoom 200% simulation | document still width 1366; internal panel scrollable | `5b7a5c637ec0262e466431475cd72fc20876c0d1a64d72aebc45d36efec6ef51` |

**Visual review:** Light desktop/mobile screenshots inspected; initial connector labels were partly masked by node fill. Moved them to the free canvas gutter above nodes; refreshed all six screenshots and reran tests. No visible collision in the corrected desktop image. Mobile content remains available by scrolling the focusable technical panel.

### Independent verification statuses

| Dimension | Status | Boundary |
| --- | --- | --- |
| `semantic_source` | PASS (fixture-only) | 5 nodes and 2 input edges unchanged; no new relation or source/truth state |
| `static_check` | PASS (isolated) | 26 Python unit tests + compileall; exact source/snapshot blobs |
| `browser_visual` | PARTIAL | Light/Dark, desktop and 390px, keyboard ArrowRight, CSS 200% simulation; **not native browser zoom** |
| `browser_file_navigation` | NOT_VERIFIED | HTML loaded via `set_content`; link destinations checked as source, not activated |
| `atlas_layout_self_check` | NOT_RERUN | Connector lacks executable full repository checkout; no claim of formal PASS |
| `github_render` | NOT_RUN | Phase 5 README assets not yet built |
| `actual_publishing` | NOT_RUN | No publishing requested |

**Acceptance decision:** T018–T025 checked for their bounded source/fixture/presentation preparation deliverables. **T026 remains unchecked and Phase 4 must not be marked fully complete** until native browser zoom and relevant full navigation/validator coverage are supported by run-specific evidence. Do not start Phase 5 under Lazy Modeling Gate.
