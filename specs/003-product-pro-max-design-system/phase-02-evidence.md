# Spec 003 — Phase 2 implementation and verification evidence

**Date:** 2026-10-09. **Source base:** `5d467ceb5efe2a02892ae151ccd135ba12dd9493` (GitHub `main`).

## Scope and evidence classification

Phase 2 only, T004–T011: repo-owned Signal Protocol Light/Dark tokens, role/primitive contract, repo-local validator, deterministic offline CSS/SVG-CSS exporter, README instructions and independent verification status contract. All code and tests below were **executed in an isolated container staging directory** using Python 3.13.5; this is **not** a full Git checkout regression run. The five staged files were matched byte-for-byte to the Git blobs created for the eventual commit.

| File | Tested Git blob SHA |
| --- | --- |
| `design-system/tokens.json` | `bf07abd8c0e93282c9bb15727fdbe711f4cd45f9` |
| `design-system/components.md` | `67b1f22b949148d43e3ca7106f3b5d3ec72393de` |
| `scripts/verify_design_system.py` | `49ce647e11913d8816c560cd1f71628ca81f1ddb` |
| `scripts/export_design_tokens.py` | `40482b3dfe58cfb586d4b0b89b07b01204eaeb89` |
| `tests/test_design_system_tokens.py` | `3303214d8e7f1061cf492439f15fd151cb8c3aba` |

## Actual isolated runs

| Category | Command / observed output | Status |
| --- | --- | --- |
| Unit tests | `python -m unittest discover -s tests -p 'test_design_system_tokens.py' -v` → `Ran 11 tests in 2.371s / OK`; repeated → `11 tests in 2.394s / OK` | **PASS (isolated)** |
| Static syntax | `python -m compileall -q scripts tests` → exit 0 | **PASS (isolated)** |
| Token contract | `python scripts/verify_design_system.py --check-tokens` → `PASS: repo-local tokens validated...` | **PASS (isolated)** |
| All surfaces | `--surface readme/brand/diagram/docs` → 4 PASS; Dark defaults README/brand, Light diagram/docs | **PASS (isolated)** |
| Theme and density | Light/Dark × compact/default/spacious → 6 PASS | **PASS (isolated)** |
| Read-only determinism | `python scripts/export_design_tokens.py --check` → PASS; no file write | **PASS (isolated)** |
| SVG CSS output | `--theme dark --format svg-css` emitted `svg.ppmax-design-system` with revision `0.1.0` and fingerprint | **PASS (isolated)** |
| Export snapshot | `--surface docs --output /tmp/ppmax-design-phase2.css`, then same args with `--check` → EXPORTED and PASS | **PASS (isolated)** |
| Tampered derivative | Same `--check` after replacing output with `tamper` → nonzero, `FAIL: visual token snapshot drift`; no auto-repair | **PASS negative (isolated)** |
| Invalid theme | `--surface diagram --theme sepia` → `FAIL: theme 'sepia' unsupported` | **PASS negative (isolated)** |
| Malformed roles/profile | Unit tests rejected missing/unknown role, malformed CSS, font injection, small font, insufficient contrast, absent repo tokens with foreign HOME profile | **PASS negative (isolated)** |
| Contrast numeric spot check | minimum measured relevant roles vs surface: Light 6.16:1, Dark 9.64:1 (not an exhaustive UI contrast audit) | **PASS limited token sample** |

**Verified Python runtime:** 3.13.5. **Token revision:** `0.1.0`. The tests do not create a running browser/renderer, do not change user profiles, and do not alter Product Model or Skill Registry.

## Verification boundary

| Layer | Status | Reason |
| --- | --- | --- |
| `semantic_source` | **PASS — source review limited** | No semantic model or existing diagram edits in this patch; mapping contract explicitly preserves Gate/Decision |
| `static_check` | **PASS — isolated exact-blob sources** | Python unit/CLI/compile checks above; full-repo suites not run |
| `browser_visual` | **NOT_RUN** | No Phase 2 HTML/SVG diagram rendered; visual acceptance belongs to Phase 3/4 |
| `github_render` | **NOT_RUN** | GitHub SVG hero/README asset integration is future Phase 5 |
| `actual_publishing` | **NOT_RUN** | No release/deployment requested |
| `full_checkout_regression` | **NOT_RUN** | Container cannot resolve github.com for clone; no complete checkout or in-repo CI execution |
| `diagram_self_check/atlas/layout` | **NOT_RUN this phase** | No living diagram, Atlas, or registry entry was changed. Historical checks do not count as Phase 2 execution. |

**Runtime verification decision:** isolated Python implementation tests PASS only for the above token/export boundary. Browser, full repository integration, GitHub preview and production are explicitly unverified. Do not promote project-level implemented diagram or start pilot migration from this result.
