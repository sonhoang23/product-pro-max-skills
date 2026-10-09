# Spec 003 — Pre-migration Diagram Baseline (GitHub-only)

**Source scope**: Read-only inventory before the Signal Protocol migration pilot (T001/T035 precursor).  
**Starting commit**: `7e45f673f97f907e1bbc807cec0e2517add63b17`.  
**Status**: T001 source inventory completed at `d78320a` on 2026-10-09; no migration performed and no new browser/Atlas validator PASS claimed. Earlier baseline at `7e45f67` retained below for historical comparison.

## Verified GitHub source files and blobs

| Surface | Path | Git blob SHA |
| --- | --- | --- |
| Spec 002 pilot HTML | `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html` | `6acb098a4e8513d50527bfb615a6561bf3520e16` |
| Repo Atlas HTML | `docs/diagrams/index.html` | `6561df73efce6248ece0eeb9e0a8f813e29ceec8` |
| Atlas registry JSON | `docs/diagrams/diagram-index.json` | `42c9004fd15aba8fbb493c626fbb965ee1f83f71` |
| Atlas checker | `scripts/verify-diagram-atlas.py` | `9018f5afd3bdd4d5b07632e95759def2b55efd11` |
| Layout checker | `scripts/verify-diagram-layout.py` | `198079774e6a66df40544ee29d2979fb86afa51f` |
| Diagram skill self-check | `.agents/skills/diagram-design-vi/scripts/self_check.py` | `d76ee3ae660b084cb0e6fd4ed9ba5c5daa2cf4fb` |

## Existing source semantics and navigation (must remain intact)

- Registry entry ID `feature-002-skill-metadata-relations`; `scope=feature`, `truth=planned`, `phase=spec`, `feature=002-skill-manifest-registry`, source `specs/002-skill-manifest-registry/spec.md`, parent `feature-002-ledger`.
- Existing visible node identities: Skill Model; Skill Contract; Một skill distributable; Skill Registry; Product Model · Spec 001; skill-creator-vi. Six SVG `rect.node/focus` shapes are visible in source and six SVG `path.edge` connectors are present.
- Center node references `SKILL.md + manifest.yaml`, `ppmax-<skill-slug>` and `skills/<primary-cycle>/…`; registry is a derived discovery view, not authority.
- The conceptual source describes relationships among model/contract/manifest/registry, and Product Model lifecycle IDs. Do not introduce a Gate result, a workflow Decision or an invented relation while reskinning this particular diagram.
- HTML navigation currently links back to `../../../docs/diagrams/index.html` and `../diagrams.html` (Feature Ledger / parent). Existing text indicates `planned truth`.
- Repo Atlas links Spec 002 and 003 feature ledgers separately. Spec 003's two additional `planned` entries must not be renamed or converted to `implemented` by visual migration.

## Unexecuted validation / rollback boundary

1. Before a pilot, re-fetch existing `main` blobs and diff against the SHAs above (a changed source invalidates this snapshot).
2. Create **a copy** of the Spec 002 HTML for visual comparison; never replace the original as the first step.
3. Compare complete original vs candidate text/labels, relations/edge direction, `planned` flag, source and navigation/registry links, preserving 100% unless the authoritative source is separately changed.
4. Run `python scripts/verify-diagram-atlas.py`, `python scripts/verify-diagram-layout.py` and the actual supported `self_check.py` CLI against a full checkout.
5. Perform desktop/390px/200%-zoom and accessibility review; record exact evidence. Roll back/reject the pilot on mismatch.

**Not done:** No implementation code, migrated file, official repo-local validation, approved pilot, or rollback execution. Do not claim T001/T035 complete from this inventory alone.

## Phase 1 execution record — T001 (2026-10-09)

**Observed source:** GitHub `main` commit `d78320a3bcce531db43a6e47ce16ab284ada64b0`; recursive Git tree returned `truncated=false`.
All entries below were fetched at that ref, not inferred from a screenshot or a local checkout.

| Artifact | Observed blob SHA | Baseline result |
| --- | --- | --- |
| `docs/diagrams/diagram-index.json` | `42c9004fd15aba8fbb493c626fbb965ee1f83f71` | 3 registered feature diagrams; all `truth=planned` |
| `docs/diagrams/index.html` | `6561df73efce6248ece0eeb9e0a8f813e29ceec8` | Atlas links Spec 002 and 003 ledgers |
| `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html` | `6acb098a4e8513d50527bfb615a6561bf3520e16` | Original pilot source retained, unchanged |
| `scripts/verify-diagram-atlas.py` | `9018f5afd3bdd4d5b07632e95759def2b55efd11` | Static registry/navigation/scope validator source |
| `scripts/verify-diagram-layout.py` | `198079774e6a66df40544ee29d2979fb86afa51f` | Static SVG/layout validator source |
| `.agents/skills/diagram-design-vi/scripts/self_check.py` | `d76ee3ae660b084cb0e6fd4ed9ba5c5daa2cf4fb` | Diagram HTML/SVG self-check validator source |

**Registry verification (source-level):** 3 unique planned diagram entries; each referenced `path` and `source` exists in the untruncated tree. Existing Spec 002 entry is `feature-002-skill-metadata-relations`, `scope=feature`, `phase=spec`, `truth=planned`. Spec 003 entries remain in their existing `spec` and `plan` phases. No Atlas/ledger/source/diagram file was modified.

**Preservation rule:** The existing Spec 002 diagram blob above is the exact pre-migration restore baseline. This document is not evidence of a migrated copy or of any parity/rollback test. Those are Phase 6 tasks T035–T043.

**Verification level:** GitHub tree/blob inspection **PASS** for inventory, ID uniqueness and file presence. Actual execution of `self_check.py`, Atlas/layout Python, desktop/mobile/zoom/browser QA **NOT RUN in this session**. Earlier user-reported Windows validator evidence for modeling at `341f952` is recorded separately in `modeling-acceptance.md`; do not relabel it as a 2026-10-09 rerun of Phase 1.

**Scope guard:** No changes to Product Model, Skill Registry, existing diagrams, Atlas semantics or migration pilot.

## Phase 6 — isolated source migration plan and rollback (2026-10-09)

**Baseline restore authority:** Git blob `6acb098a4e8513d50527bfb615a6561bf3520e16` for `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html`. The same exact source is preserved as `tests/fixtures/design-system/pilot/original-spec002.html`. `spec.md` is never modified.

**Candidate:** `tests/fixtures/design-system/pilot/migrated-spec002.html`. The candidate changes **only the original `<style>` block**. After removing the CSS blocks, every other byte of original HTML equals candidate HTML. No node, connector, text, source path, planned marker, arrow geometry, navigation link or Atlas entry is rewritten.

**Preflight boundary:** Before promoting, compare candidate vs source with `scripts/migrate_design_system_pilot.py check` and `tests/test_design_system_diagrams.py` migration parity checks, then run full original self-check/layout/Atlas and desktop/mobile/zoom browser visual acceptance. If any required dimension fails, refuse promotion or restore immediately.

**Explicit reversible actions (safe guards included):**

```bash
python scripts/migrate_design_system_pilot.py preview   # generates copy only, leaves live diagram unchanged
python scripts/migrate_design_system_pilot.py promote   # changes live diagram ONLY if current content is expected baseline/candidate
python scripts/migrate_design_system_pilot.py check     # read-only deterministic preview + promoted original check
python scripts/migrate_design_system_pilot.py restore   # restores verified baseline, refuses unexpected concurrent edits
```

Do not change `docs/diagrams/diagram-index.json` or Ledger graph semantics to "implemented". A visual migration does not change feature truth (`planned`). Other diagrams remain untouched without explicit follow-up scope. On mismatch: run `restore`, compare source Git blob to pinned baseline, rerun Atlas/layout/self-check and report the actual failure, never stamp false acceptance.

**Source-stage note:** A candidate/rollback implementation may exist before visual or native-zoom acceptance. This document does not assert acceptance of migration, full browser usability or any unrun CLI.

## Approved pilot record

- Source SHA restored from immutable fixture: `6acb098a4e8513d50527bfb615a6561bf3520e16`.
- Promoted CSS-only original Git blob: `7f191bcf586c479783b925dd432c916a34a86174` (commit `d5493bcea3fd8786961793cfa500dad35670f40e`).
- GitHub CI on promoted diagram: 33/33 tests, Atlas/layout/self_check, desktop/mobile Light/Dark browser and actual `file://` link-click navigation **PASS**. Browser zoom compositor 200% only; native UI 200% pending.
- `python scripts/migrate_design_system_pilot.py check` verifies active promoted original and preview with no writes; `restore` writes pinned source only if original is an expected candidate/baseline.
- No Atlas JSON truth, source model, Skill Registry or unrelated diagram was migrated. Further migrations require separately approved scope.
