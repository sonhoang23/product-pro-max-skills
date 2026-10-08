# Spec 002 — Verification evidence

## Windows regression, 2026-10-08

- Source HEAD: `b03bea1e64a7688b5c5ecdf9e6a3eea8f50be597`
- Command: `python -m unittest discover -s tests -p "test_skill*.py" -v`
- User-provided terminal log: `Ran 35 tests in 0.169s` and `OK`; 35/35 PASS, including three T036 negative fixtures.
- Command: `python scripts/generate_skill_registry.py check`
- User-provided result: `Registry check OK` for committed `registry/skills.json`.
- Previously at `ef6de19`: installer `--all --dry-run` discovered 13 skills. This was discovery only, not a write/install run.

## Evidence still missing

- Python interpreter and PyYAML installed version for this exact run were not printed.
- Full `quickstart.md` validation matrix, byte hashes, exact negative-case process exit statuses and fresh filesystem fingerprints not recorded as a single end-to-end run.
- Ubuntu GitHub Actions job execution and exact logs unverified. Combined commit-status API for `b03bea1` returned no statuses; this does **not** establish CI PASS or FAIL.
- Phase implementation modeling gates are stale or in-progress; promotion tasks T030/T034/T037 and T040 remain pending.

Do not treat these missing checks as PASS or mark T038–T041 complete.

## Final source audit prepared (pending consolidated run)

- FR-001–004: `SKILL-MODEL.md`, `SKILL-CONTRACT.md`, `SKILL.md` and sibling manifests are the authoritative/behavioral split.
- FR-005–012: canonical ID/path/primary-cycle/lifecycle/track restrictions enforced by registry validation and fixtures.
- FR-013–022: metadata discovery fields, safe semantics and workflow/skill reference checks covered by manifest validation and registry projection.
- FR-023–027: generated 13-entry registry, byte-exact checker and ASCII/localization fixtures; development-tool exclusion tested.
- FR-028–029: `skill-creator-vi` authoring instructions and static contract fixture; actual end-to-end AI authoring has not been exercised.
- FR-030–031: 13 skill source migrations contain only frontmatter/H1 changes, static migration parity checked. Actual invoked behavioral parity remains untested.
- FR-032: source changes limited to metadata/registry/authoring/CI/verification; no new eval ranking, compatibility policy, or hosted UI.
- SR-01–04: negative fixtures for read-only drift, identity, references and atomic writes passed in earlier Windows run; rerun in consolidated release verification.
- SR-05: source static migration diff and manifest mapping reviewed; behavioral invocation not covered.
- SR-06: `.agents/` lookalike and localized identifier fixtures passed in earlier Windows run.
- SR-07: file-only implementation remains without new network runtime boundaries; CI runner needs network only for checkout and installing pinned PyYAML.

### Project-level Diagram Check — provisional source assessment

Existing spec diagram represents **planned** metadata/skill relationships. Implemented registry relationships are expressed in `SKILL-MODEL.md`, `SKILL-CONTRACT.md`, `docs/ARCHITECTURE.md`, and `registry/skills.json`. No additional project diagram introduces a clearer boundary or sequence for this small, deterministic file-only contract; **no-diagram-needed is the proposed outcome**, contingent on a fresh implementation modeling pass and final verification. Do not alter Diagram Atlas or duplicate planned semantics.

## Consolidated final run (not executed)

```powershell
python -m pip install -r requirements-registry.txt
python scripts/verify_skill_registry_release.py
```

Capture complete output, source HEAD, GitHub Actions Ubuntu run/check logs and negative-case process exit codes before marking T038–T041 complete. This section is a planned checklist, not a passing result.
