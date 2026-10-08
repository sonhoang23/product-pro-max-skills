# Data Model — Skill Manifest Registry

Planned technical representation; source authority: Spec 002 and `model/product-model.json`.

## SkillManifest
- `id`: required `ppmax-<slug>`, ASCII lowercase kebab-case; globally unique in canonical skills.
- `namespace`: literal `product-pro-max`.
- `slug`: unprefixed stable ASCII name; derives the ID.
- `description`: required nonempty English summary.
- `primary_cycle`: exactly one existing Product Model cycle.
- `lifecycle`: nonempty list of `{cycle, phase?}`; referenced phase must belong to referenced cycle.
- `tracks`: list of valid Product Model track IDs.
- `triggers`: positive `include` and negative `exclude` semantic descriptions.
- `inputs`: list of `{name, description, required: boolean}`.
- `outputs`: list of `{name, description, semantic_kind?}`; gate and decision semantics must preserve Spec 001 distinction.
- `related_skills`: list of `{skill_id, type}` (controlled relation vocabulary).
- `workflows`: list of `{workflow_id, role}`, discovery-only; orchestration remains in authoritative workflow definition.

## Invariants
- Physical path `skills/<primary_cycle>/<id>/manifest.yaml` matches manifest ID, directory and sibling `SKILL.md` frontmatter name.
- `primary_cycle` is represented in lifecycle; other valid associations allowed.
- Duplicate IDs, slugs, relationships, keys or semantic inputs/outputs fail validation.
- All referenced cycles, phases, tracks, related skills and workflows must exist.
- Repository development skills under `.agents/` are excluded.

## Registry
`registry/skills.json` is the deterministic projection of all canonical manifests, sorted by ID, with `registry_version: 1` as an encoding marker (not a product compatibility policy). Include all FR-025 discovery fields and canonical file paths. No direct edits; check mode recomputes and compares byte-for-byte.

## Migration
Inventory old path, new canonical path, legacy name and behavioral fingerprint. Preserve responsibilities, triggers, evidence rules, outputs and workflow behavior; separately repair references. No automatic rewriting of behavior.
