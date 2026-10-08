# Quickstart — Skill Registry

**Current state:** Canonical registry, all 13 migrated skills, unit fixtures and Ubuntu CI source have been committed. Windows regression at `b03bea1` passed 35/35 tests and registry check. The current release verification command must still run on the latest commit; no future CI result is presumed.

## Environment

Use **Python 3.12**, matching `.github/workflows/validate.yml`. Once tooling exists, install the pinned parser:

```bash
python -m pip install -r requirements-registry.txt
```

Parser implementation in `scripts/skill_registry_common.py` must subclass `yaml.SafeLoader` to reject duplicate YAML mapping keys and unsafe tags.

## Generator/checker interface

```bash
# T009–T011: validate the entire catalog first, then atomically replace derived JSON
python scripts/generate_skill_registry.py generate

# T011: read-only recomputation, byte-for-byte drift/coverage comparison, nonzero on mismatch
python scripts/generate_skill_registry.py check

# T012/T021/T022: negative fixtures + deterministic/regression checks
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

**Latest evidence:** Windows 35/35 skill tests PASS, read-only check PASS, installer dry-run 13/13 PASS at earlier commits; CI Ubuntu and full single-run verification still pending.

## One-command final read-only verification

```bash
python -m pip install -r requirements-registry.txt
python scripts/verify_skill_registry_release.py
```

The release verifier prints Python and PyYAML versions, registry SHA-256, exact 13-skill/3-workflow inventory, read-only registry check, test results and dry-run installer paths. It fails fast with nonzero status. It does not generate registry or execute skill workflows. Save the complete terminal output and the Git SHA in `verification.md` before closing T039.

