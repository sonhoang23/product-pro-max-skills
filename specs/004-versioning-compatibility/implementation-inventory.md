# Spec 004 — Source and Contract Inventory

**Observed at:** `b265649534480fab55c383678fc640f44bc683e7` on `main`, 2026-10-13. **Scope:** current repository artifacts. This is not a compatibility or publication verdict.

| Surface | Canonical owner | Observed current state | Planned version/compatibility treatment |
|---|---|---|---|
| Product Model | `model/product-model.json` | `model_version: "1.0.0"`; 10 lifecycle cycles, gates `pass/warn/fail` distinct from decisions | The model owns its own version and semantics; compare canonical IDs/relations and dependent readers before any compatible claim |
| Skill behavior | `skills/<cycle>/ppmax-<id>/SKILL.md` | No distributable skills published; development helpers live under `.agents/` | Skill behavior remains in SKILL.md, not registry or folder name |
| Skill metadata | Sibling `manifest.yaml` per distributable skill | Strict `scripts/skill_registry_common.py` currently rejects unknown metadata fields, and has no canonical `version` field | Expand reader and test legacy inputs *before* writing/mandating `manifest.version` |
| Workflow | `workflows/<name>/workflow.yaml` | `workflows/idea-to-first-users`, `idea-to-mvp`, `pre-launch-audit` are documentation-only; no executable `workflow.yaml` published | Existing `schemas/workflow.schema.json` defines `version`; do not invent workflows/releases |
| Machine schemas | `schemas/*.schema.json` + their strict readers | Five JSON Schema files: evidence, product-model, project-state, skill-output, workflow | Stable `$id` plus independently declared support-ledger contract version, only when actual baseline exists |
| Project state | `schemas/project-state.schema.json`, `templates/project-state/project.yaml` | Template has `project/cycle/phase/status/updated_at`, no `contract_version`. Schema permits additional properties and constrains phase/cycle ownership | Version future writes through explicit opt-in migration; preserve legacy unversioned reads |
| Durable evidence/decision | `schemas/evidence.schema.json`, `schemas/skill-output.schema.json`, `templates/project-state/evidence/`, `templates/project-state/decisions/` | Source artifacts carry history and evidence semantics | Preserve originals, provenance, assumptions and decisions across migrations |
| Generated registry | `registry/skills.json` | `{"registry_version":1,"skills":[]}` | `registry_version` is projection format, **not** skill/component version or evidence of a release |
| Installer lock | `skills-lock.json` | Integer `version: 1`; includes development tooling entry `diagram-design-vi` | Lock representation marker, **not** behavioral SemVer |
| Visual tokens/Docs | design tokens and presentation docs | Separate presentation authority | A cosmetic or doc-only change does not automatically imply a component bump |

## Current integration and constraints

- `scripts/validate_repo.py` checks repository structures, canonical cycle/phase/gate/decision consistency and project-state template.
- `scripts/skill_registry_common.py`, `scripts/generate_skill_registry.py` and `scripts/verify_skill_registry_release.py` own registry integrity; only `skills/` is distributable.
- `requirements-registry.txt` pins `PyYAML==6.0.2` and the canonical YAML parser uses duplicate-key detection.
- `.github/workflows/validate.yml` uses Python 3.12, runs repository checks plus diagram/browser tests. No Spec 004 checker or data-migration test exists yet.
- Spec 001 Product Model and Spec 002 Skill Model remain semantic authorities. Specs 005 (evals), 006 (governance), 008 (releases) and 009 (durable shared context) are separate.

## Evidence and unknowns

- This inventory is an **observed file-level review**, not proof of historical releases, all external readers or runtime compatibility.
- No supported historical baselines are declared here. Never derive one from HEAD, from the `model_version` value, the empty registry, a lock marker or example fixture.
- External clients and unpublished consumers are **unknown** until explicitly declared; `unassessed` is the truthful compatibility state without evidence.
- Planned `compatibility/supported-baselines.json` must be treated as an explicit policy ledger, not another Product Model/Skill Model authority.
