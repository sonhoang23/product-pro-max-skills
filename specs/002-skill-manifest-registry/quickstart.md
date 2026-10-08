# Quickstart — Skill Registry (planned, not executed)

**Current state:** Phase 1 setup only. `scripts/generate_skill_registry.py`, `scripts/skill_registry_common.py` and `registry/skills.json` do not exist yet; commands below are **future interfaces**, not runnable claims.

## Environment

Use **Python 3.12**, matching `.github/workflows/validate.yml`. Once tooling exists, install the pinned parser:

```bash
python -m pip install -r requirements-registry.txt
```

Parser implementation in `scripts/skill_registry_common.py` must subclass `yaml.SafeLoader` to reject duplicate YAML mapping keys and unsafe tags.

## Future generator/checker interface

```bash
# Future T009–T011: validate the entire catalog first, then atomically replace derived JSON
python scripts/generate_skill_registry.py generate

# Future T011: read-only recomputation, byte-for-byte drift/coverage comparison, nonzero on mismatch
python scripts/generate_skill_registry.py check

# Future T012/T021/T022: negative fixtures + deterministic/regression checks
python -m unittest discover -s tests -p 'test_skill_registry*.py' -v
```

`generate` MUST validate every distributable manifest, identity, path, lifecycle and reference before atomic replacement of `registry/skills.json`; any error leaves the previous output unchanged. `check` MUST NOT write anything, including when the registry is missing, stale or malformed. Both modes MUST exclude `.agents/`.

## Validation evidence required after implementation

1. Inventory 13 distributable skill directories and 3 workflow definitions from `specs/002-skill-manifest-registry/migration-inventory.md`. After T024/T025, require matching `SKILL.md` and `manifest.yaml` identity.
2. Run `generate` twice and compare bytes/hashes; output must be deterministic.
3. Run `check` on valid data and verify exit 0 plus unchanged filesystem state.
4. Inject independent failures: missing manifest; malformed/duplicate-key YAML; bad/duplicate identity; wrong cycle/path; invalid phase ownership, track, gate/decision kind, skill/workflow relation; tampered registry. Require nonzero and actionable source diagnostics.
5. Verify `.agents/` exclusion and `skill-creator-vi` new/update contract compliance.
6. Compare migration source blob fingerprints and post-migration behavior/trigger/evidence/output/workflow responsibilities; record repaired links.
7. Record exact command, tool versions, SHA/commit, input inventory, output hashes, exit codes, logs and tests in `specs/002-skill-manifest-registry/verification.md` (T039).

**Evidence state:** All generator/checker, migration-parity and CI verification steps remain **NOT RUN** in Phase 1.
