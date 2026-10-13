# Compatibility Test Fixture Conventions

**Status:** fixture design for Spec 004. Scenarios and examples are synthetic and **not** evidence of a published release or a supported historical baseline.

## Layout

- `positive/`: unchanged-contract and declared-tolerant-consumer cases with expected `compatible` only when evidence is complete.
- `negative/`: missing baseline, invalid digest/ref, version conflicts, strict-consumer breakage, path traversal and malformed manifests.
- `migration/`: disposable legacy, mixed-version, interrupted/repeated, missing-source and recovery simulations. Never use real user projects.
- Fixtures may be generated under a Python `tempfile.TemporaryDirectory()` rather than committed en masse; committed snapshots must have deterministic UTF-8 content.

## Source pinning

1. Use a real immutable source `commit_sha` (full 40 hexadecimal characters) plus an `authority_path` relative to a declared fixture/repository root.
2. Record a SHA-256 *file byte* `sha256` (64 lowercase hexadecimal characters). Recompute and compare before classifying a candidate.
3. A symbolic `ref` is only explanatory unless resolved to the recorded immutable commit. A different commit, missing blob, stale digest or dirty candidate is not a positive proof.
4. Reject `..` traversal, absolute paths, symlink escapes and duplicate baseline/component identities. Diagnostic paths use POSIX relative representation across Windows/Linux.
5. Keep base and candidate independent and read-only. Test output goes to a temporary directory; compare before/after input hashes.
6. Pin simulated `consumer_id`, `strict_reader`, `range`, `required_outputs` and explicit support scope. No known consumer does not imply universal compatibility.
7. JSON/YAML must be parsed with strict validation. Duplicate YAML mapping keys and unknown schema fields are negative fixtures, not silently accepted.
8. An absent/unsupported baseline, unknown reader tolerance or missing behavior evidence must produce a non-green `review`/`unassessed` result, not `allow`.

## Minimum independent cases

| Fixture family | Expected behavior |
|---|---|
| stable PATCH correction | Compatible only for assessed supported consumers, without invented runtime evidence |
| supported MINOR addition | Requires evidence every declared strict reader tolerates it |
| required output removed | Breaking; inadequate bump/undisposed migration blocks |
| closed enum or unknown manifest field | Breaking for a declared rejecting reader |
| semantic-only change | `review_required` without behavioral evidence |
| baseline missing/corrupt | `unassessed` or input error (distinct), never green |
| unknown dependency/cycle | Scoped diagnostic and non-green verdict |
| zero published skills | Empty registry is valid; no fabricated skill release |
| legacy/project migration | No history/provenance loss, safe dry-run and repeat behavior |
| environment/path normalization | Same canonical diagnostic paths on native Windows and Linux |

The official post-implementation acceptance matrix is in `specs/004-versioning-compatibility/quickstart.md`. As of setup, no fixture test has run.
