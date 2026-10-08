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
- Phase 6–8 implementation modeling gates were refreshed with current source fingerprints and negative Diagram Checks after prior Windows evidence; T030/T034/T037 source documentation promotions are complete. Phase 9 final converge/Diagram Check T040 remains pending consolidated validation.

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

## Final source-preparation notes

The previous repository-wide validator still assumed flat skill paths and would reject canonical migration in the original `Validate` GitHub Actions workflow. `scripts/validate_repo.py` has now been updated to inspect `skills/*/ppmax-*/SKILL.md`, require sibling manifests and compare against canonical 13 IDs. The consolidated verifier explicitly runs this validator as well as the registry checker, all skill tests and installer dry-run. These changes have **not** received a post-change Python execution log and must be validated in the one-shot final run.

Phase 6–8 documentation/authoring/global-first implementation has been subject to a source-based negative Diagram Check; the final repo-wide Diagram Check remains a separate T040 evidence gate. No project-level diagram was created prematurely.

## Consolidated Windows release verification — 2026-10-08

User-provided PowerShell run after fast-forward `b03bea1 → 9679b10`:

- `python -m pip install -r requirements-registry.txt`: PyYAML==6.0.2 satisfied.
- `python scripts/verify_skill_registry_release.py`: exit was successful; final marker `RELEASE VERIFICATION PASS (read-only, no runtime skill invocation)`.
- Interpreter Python 3.13.3; PyYAML 6.0.2.
- 13 canonical skill entries, 3 workflow files; `registry/skills.json` SHA-256 `d1e25c6166be01627d05156162796ad54b82857feb4c535d0d26d67a4e229e29`.
- Repository validator PASS: 13 canonical skills, 3 workflows, 5 JSON schemas, 10 cycles, 34 phases.
- Derived-registry read-only `check`: `Registry check OK`.
- All **35 unittest cases PASS** in 0.196 seconds, including negative validation, duplicate YAML, missing manifests, malformed identity and read-only/no-write fixtures.
- Installer `--all --dry-run` resolved 13 distinct skill paths and reported `Selected 13 skill(s)`.
- This establishes **Windows source and read-only verification** for T039. The one-shot run does not print per-negative-case OS exit codes individually, and no actual installer write, agent-skill invocation, or workflow runtime was executed.

### CI and final modeling boundary

GitHub connector lookup of workflow runs for commit `9679b10` returned an empty result (the connector's lookup is limited to PR-triggered runs). Combined commit statuses also returned empty. **Ubuntu GitHub Actions success is not established**. T038 must remain unchecked until explicit workflow/job evidence is available.

Project-level Diagram Check: file-only manifest/registry and declarative lifecycle grouping add no project-level state machine, sequence or boundary beyond documented text and the existing Spec 002 planned metadata diagram. Reasoned **no new project diagram needed** for the verified source scope. Avoid duplicating the planned conceptual diagram. CI Ubuntu runtime remains separately unverified.

## Final local-only acceptance and installer write evidence

The user explicitly rejected GitHub Actions as an acceptance requirement. T038 is satisfied by the previously recorded Windows release verification (35/35 PASS, registry check PASS, 13-skill discovery) plus the latest PowerShell real installation:

`python scripts/install.py --target .tmp-skills --all` printed 13 distinct source→destination copies and `Selected 13 skill(s).` Subsequently `Remove-Item .tmp-skills -Recurse -Force` returned without an error. This supports installer success and cleanup but **does not provide independent file-byte parity** or actual agent workflow invocation. 

T041: FR-001–FR-032 and SR-01–SR-07 have been source-audited in the sections above and matched against the local verification results. No unverified Ubuntu CI PASS or actual AI skill invocation claimed. Spec 002 local file-contract acceptance is complete under this stated scope.
