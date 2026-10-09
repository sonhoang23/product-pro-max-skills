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
