# Spec 003 — Integration Preflight Notes

**Observed**: GitHub `main`, starting at `7e45f673f97f907e1bbc807cec0e2517add63b17` (read-only connector inventory).  
**Nature**: Preflight for T003; **not a completed implementation task** and not a local checkout verification.

## Reconciliation observations

| Check | GitHub observation | Consequence |
| --- | --- | --- |
| Feature directory | `specs/003-product-pro-max-design-system/` exists with spec, plan, diagrams, checklists and tasks | Do not create duplicate feature folders |
| Active feature | `.specify/feature.json` points to `specs/003-product-pro-max-design-system` | Keep this pointer unchanged unless deliberately switching feature |
| Roadmap IDs | `specs/ROADMAP-foundation.md`: 001/002 complete, 003 Design System planned, former versioning 003→004, backlog through 008 | Old numbering conflict has been resolved |
| Diagram inventory | `docs/diagrams/diagram-index.json`: Spec 002 one planned diagram; Spec 003 two planned diagrams | Preserve scope, `truth`, `phase`, `source`, and relation graph |
| Project marker | Root `.diagram-design` not found on observed `main` | No project marker identified; machine-global profile availability remains unknown |
| Existing renderer skin | `.agents/skills/diagram-design-vi/references/style-guide.md` currently describes VibeToolPro skin | New repo-owned tokens must take precedence; do not rewrite developer-home profiles |
| Lazy Modeling | `spec` and `plan` gate remain `blocked` with missing repo-local validator/browser evidence | Do not run `speckit-implement-vi` or claim PASS yet |

## Deferred-local-QA record

- **User request:** Local modeling checks are temporarily deferred because no local machine is currently available.
- **Gate semantics:** `blocked` means formal validation incomplete. Deferral is scheduling metadata, **not** an accepted substitute for PASS, `no-diagram-needed`, or waiver of Lazy Modeling Gate.
- **Still required:** official diagram-design `self_check.py`, repo `verify-diagram-atlas.py` and `verify-diagram-layout.py`, browser navigation/zoom/accessibility review and freshness recheck after the latest spec/plan edits.
- **Evidence source now:** GitHub file contents and object SHAs only; no local runtime, no checked-out full-repository script execution.

## Next action on a machine

1. Pull latest `main`; compare SHA and reread `.specify/feature.json` / roadmap.
2. Inspect `migration-baseline.md` and reconcile any changes since the baseline snapshot.
3. Use the existing skill's documented CLI for self-check, run Atlas/layout checks and browser visual QA.
4. Refresh `.modeling-state.json` source hashes + QA evidence; only make the gate PASS if required checks actually pass.
5. Then start formal implementation Phase 1 and collect concrete evidence before checking T001–T003.
