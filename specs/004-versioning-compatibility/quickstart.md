# Quickstart — Planned Compatibility Validation

**Status:** validation design / expected outcomes only. None of the Spec 004 commands or fixtures below exist yet. This document does not claim executable test PASS.

## Preconditions

1. Work from a pinned clean checkout on `main`; record final commit/revision and modified paths.
2. Verify Spec 004 `spec = modeled` state remains fresh; the diagram's CI QA covers only the diagram.
3. Python 3.12 available. Existing `requirements-registry.txt` pins PyYAML 6.0.2; installation is a separate environment mutation, not an implicit step of read-only assessment.
4. Canonical `runtime-verification` v1.12.0 is synced at `.agents/skills/runtime-verification/` from upstream commit `fcd9a5b8db9c37673b9bb92d69bf6056af30ec3a`; recheck inventory freshness at Tasks time. This is a repo skill copy, not product test evidence.
5. No production project data; use disposable fixture directories with backups.

## Planned implementation entrypoints

```shell
# Once scripts and fixtures have been implemented:
python scripts/validate_repo.py
python -m unittest discover -s tests -p 'test_compatibility*.py' -v

python scripts/check_compatibility.py assess \
  --baseline-ledger compatibility/supported-baselines.json \
  --baseline-id fixture-supported-model \
  --candidate-root tests/fixtures/compatibility/positive/model-patch \
  --report-json .tmp-compatibility/report.json
```

The examples describe a proposed CLI; no execution can pass until the checker, baselines and fixtures are committed. Actual implementation must reconcile accepted CLI syntax with [contracts/compatibility-assessment.md](contracts/compatibility-assessment.md).

## Acceptance matrix (must create representative fixtures)

| Case | Requirement | Expected classification / verdict |
|---|---|---|
| 1. Pure README/visual edit | FR-002, FR-006 | No unrelated component increment; unchanged contracts |
| 2. Stable compatible bug correction | FR-004 | `compatible`, PATCH sufficient with evidence |
| 3. Optional feature with proven tolerant readers | FR-004, FR-012 | `compatible`, MINOR sufficient |
| 4. Required skill output renamed | FR-010, FR-013, FR-024 | `breaking`; insufficient bump blocks |
| 5. Model ID/phase relationship changed | FR-009 | Breaking or review; consumer path identified |
| 6. Added gate/decision member for closed reader | FR-009, FR-012 | Not automatically compatible; known strict reader breaks |
| 7. New required manifest field rejected by old reader | FR-012, FR-031 | Breaking; reader migration needed |
| 8. Same schema shape but changed skill evidence semantics | FR-010, FR-026 | `review_required`, non-green without proof |
| 9. Missing baseline ref/source digest | FR-007–008, FR-029 | `unassessed`, non-green |
| 10. Unsupported, unpublished or unknown dependency version | FR-013–014 | Diagnostic and non-green result |
| 11. Cyclic / conflicting skill-workflow version ranges | FR-011, FR-014 | Diagnostic with exact dependency path |
| 12. Zero published distributable skills | FR-001, FR-027 | Truthful `no published skills`; no fake skill release |
| 13. Pre-1.0 breaking change | FR-005 | Breaking + explicit 0.x increment and migration notice |
| 14. Known break with insufficient bump or missing migration | FR-017–020, FR-024 | Block even when other checks pass |
| 15. Deprecated skill/field with replacement | FR-021–023 | Notice, supported interval and migration duties visible |
| 16. Removal without consumer impact/migration disposition | FR-023 | Block or separately approved safety exception |
| 17. Legacy project readable unchanged | FR-017–019 | Original evidence/decision provenance preserved |
| 18. Data migration interrupted/partial/fails | FR-018–020 | Non-success receipt, preserved recovery path |
| 19. Migration repeated on same input | FR-020 | No duplicate records; `already_applied`/equivalent |
| 20. Missing migration source / reordered migration | FR-018–020 | Explicit error, no partial silent success |
| 21. Prior fixture prerequisite invalid | FR-025–028, VERIFY-008 | Fail fast at setup with root cause |
| 22. Report created from stale revision | FR-027, VERIFY-003 | Invalidate previous proof, rerun |
| 23. Windows versus Linux path separator | FR-025, ENV-003 | Equivalent component/consumer/path diagnostics |
| 24. Unexpected parser/test warning despite exit 0 | FR-026–027, VERIFY-004 | No clean verified-compatible claim |
| 25. Structural check vs runtime/release evidence | FR-027–029 | No runtime, migration-user or publication claim |
| 26. No known external reader inventory | FR-029 | Bounded support scope, unknown external consumers visible |

## Proof sequence after implementation

1. **Fixture inventory:** verify source/target digests, valid baseline ledger, stable component IDs and declared strict readers; assert fixture preconditions before invoking checker.
2. **Static validator:** run existing repository and affected registry/schema checks; capture command, exit, count, warnings.
3. **Compatibility checker:** run every positive and negative case; inspect JSON report and non-green codes `1/2/3`; ensure no write to canonical artifact.
4. **Migration simulation:** run dry-run and explicit apply in temporary copy; compare provenance/history and record-level digests; rerun; inject interruption and verify recovery.
5. **Consumer verification:** ensure known dependent readers/workflow examples and strict metadata parser behave per declared versions. Do not treat a passing schema check as behavioral skill proof.
6. **Final revision proof:** after any code, fixture or policy change, invalidate impacted PASS and rerun affected gates. Record HEAD, tree cleanliness, checker version, suite summary and evidence artifacts.
7. **Documentation promotion:** only after implementation and verification, update project-level docs and required diagrams; run Diagram Check for changed project diagrams. Never promote planned interface as already published.
8. **Converge:** compare spec/plan/tasks/implementation/evidence; do not mark release, runtime, user migration or feature complete from static outputs.

## Planned CI placement

- Add a dedicated compatibility-check/test step to existing Python 3.12 `.github/workflows/validate.yml` after scripts and fixtures land.
- CI must treat `review`/missing baseline and `block` as non-green; errors identify actionable paths/components/affected consumers.
- Keep `--check` read-only; generated diagnostics written only to explicit temporary report path.
- No release automation or actual user migrations in CI.

## Evidence record template (fill only when commands actually run)

| Field | Required value |
|---|---|
| Revision | Exact commit SHA and working-tree state |
| Command + target | Actual executable/arguments, suite and fixture set |
| Environment | Python version, platform, dependency versions |
| Exit / summary | Exit code, test count, warnings and failures |
| Baseline/candidate | Ref/hash, declared scope and checked consumers |
| Outcome | Compatible/breaking/review/unassessed; CI allow/block/review |
| Migration | Dry-run/apply stage, backup/receipt and recovery (when relevant) |
| Proof level | Static / behavior / migrated-in-test / runtime / published, without conflation |
| Artifact | Stored report/test log link and post-run source revision |

## Handoff to Tasks

Run `speckit-tasks-vi` after checking synced runtime-verification and `ensure-model(plan)`. Tasks must trace US1–US6 and FR-001–FR-032, plus ENV-003, VERIFY-003/004/008. Do not generate tasks or implement during this Plan-only request.
