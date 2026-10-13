# Compatibility Scope (Spec 004)

**State:** foundation under implementation. No compatibility assessor or migration command is shipped by this document. This directory is not a release registry.

## Read-only assessment boundary

- Candidate sources: `model/product-model.json`, distributable `skills/**/{manifest.yaml,SKILL.md}`, existing/future `workflows/**/workflow.yaml`, `schemas/*.schema.json`, and declared `.product-pro-max/` project-state contracts.
- Baseline source: a deliberate ledger entry with immutable source ref/commit, owning path, exact digest, support scope and consumer dependency declarations. Missing or unsupported baseline is **unassessed**, not `compatible`.
- Existing `registry/skills.json.registry_version` and `skills-lock.json.version` are serialization markers, not skill/Model versions.
- The assessor must never mutate canonical sources, generated registry, lockfile, project-state or support ledger as a side effect of checking.
- The supported consumer boundary is explicit and finite. External/unknown consumers are reported as outside assessed scope, never silently treated as compatible.
- Structural verification, behavior verification, migrated-in-test, actual runtime verification and publication are separate evidence levels.
- An opt-in migration tool, if later implemented, must require explicit source/target versions, backup/receipt, recovery semantics and a separate action. Checking and `--dry-run` must not perform it.
- No network lookup, remote service, automatic package install, release publishing or implicit user-state migration is part of the offline assessor.

## Planned artifacts (not yet functional)

- `supported-baselines.json`: empty until real supported baseline declarations have traceable evidence.
- `schemas/supported-baselines.schema.json`: ledger format and strict provenance constraints.
- `scripts/compatibility_common.py`: safe parsing, version and consumer assessment primitives.
- `scripts/check_compatibility.py`: future report/exit-code command.
- Fixture expectations: `tests/fixtures/compatibility/README.md`; complete validation matrix: `specs/004-versioning-compatibility/quickstart.md`.

Publication and release-tag automation are owned by Spec 008. This directory does not alter the Product Model, Skill Model or workflow orchestration authority.
