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
