# Explicit Project-State Migration — Spec 004 Phase 5

**Scope:** file-by-file, opt-in, offline migration of legacy-unversioned
`project.yaml` / `project.json` to a state declaring `contract_version: 1.0.0`.
This is not a published compatibility baseline, broad data migration, or
permission to rewrite historical decisions/evidence.

## Contract and sequencing

1. Work on a disposable copy first. Read schema
   `schemas/project-state.schema.json`; `contract_version` stays optional
   to keep legacy data readable.
2. Use `python scripts/migrate_project_contract.py --input PATH --output NEW_PATH`
   to inspect legacy classification. This default **dry-run** is read-only.
   `assess` is an equivalent read-only mode.
3. Inspect the output path, affected source file, version and digest. Apply is
   explicitly authorized for a **single** state file. No recursive directory
   operation is supported.
4. For a distinct destination, execute:

   ```shell
   python scripts/migrate_project_contract.py apply \
     --input ./legacy/project.yaml --output ./next/project.yaml \
     --backup ./next/project.original.bak --receipt ./next/project.receipt.json \
     --accept-legacy
   ```

   New directory parents must exist; input, output, backup and receipt paths
   must not overlap, except `--in-place` with a deliberately matching input
   and output path.
5. In-place apply additionally requires `--in-place` and backup/receipt paths
   distinct from the original file. Retain backups and receipts; they pin
   input/output SHA-256, migration ID, original null version, target version,
   idempotency key, checkpoint, status and recovery action.
6. Successful repeat validates receipt + backup + source/output digests then
   reports `already_applied` without writes. Any changed/unknown receipt,
   legacy version mismatch, deleted blob or unsupported version fails closed.

## Failure and restore

Atomic destination replacement uses a same-directory staged temporary file
and fsync. Backup is created before any output mutation. A failed apply after
backup writes `failed`; a failure after target replacement writes
`partially_applied`. If the process was forcibly terminated before a receipt
could be written, backup and target must be reviewed manually; no success
may be inferred from the target alone.

For an interrupted **in-place** migration with a failure receipt, calculate
the current input digest, inspect exact backup bytes and recover explicitly:

```shell
python scripts/migrate_project_contract.py restore \
  --input ./legacy/project.yaml --output ./legacy/project.yaml \
  --backup ./next/project.original.bak --receipt ./next/project.receipt.json \
  --expected-current-sha256 <64-hex-digest>
```

Restore refuses newer/unrecognized content and checks backup hash against the
receipt. Status becomes `recovered`; begin a new reviewed migration with new
backup/receipt paths. A failed copy-to-new-file operation may not have any
output to restore; preserve original, inspect receipt and clean up explicitly.

**Invariants:** only the new version field is added; no fabricated evidence,
no promotion of assumptions, no gate/decision conflation, no decision-history
rewrite and no changes to authoritative Product Model. Unknown or out-of-order
versions require a separate reviewed migration contract. Irreversible migration
exceptions are **not executable** by this CLI (no authorization workflow exists).

**Evidence:** `tests/test_compatibility_migrations.py` uses synthetic
temporary directories, repeat runs, malformed versions, checksum drift,
injected failures and explicit restore. Native Windows behavior remains
deferred to T049/T052. Never point tests at user project data.
