# Spec 003 — Pre-migration Diagram Baseline (GitHub-only)

**Source scope**: Read-only inventory before the Signal Protocol migration pilot (T001/T035 precursor).  
**Starting commit**: `7e45f673f97f907e1bbc807cec0e2517add63b17`.  
**Status**: Baseline documentation prepared. No migration performed, no task checkbox ticked, no browser/Atlas validator PASS claimed.

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
