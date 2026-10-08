# Skill Contract

Every canonical distributable skill lives at `skills/<primary_cycle>/ppmax-<slug>/SKILL.md`, with a sibling `manifest.yaml`. **Migration status:** Spec 002 is being implemented; the existing flat skill paths remain legacy until T024–T029 complete.

## Required frontmatter

- `name`
- `description`

## Machine metadata — sibling `manifest.yaml`

`SKILL.md` continues to own behavior. The manifest owns discovery metadata and cannot redefine behavior. `model/product-model.json` owns canonical cycle/phase/track/gate/decision values.

| Field | Constraint |
|---|---|
| `id` | required, unique `ppmax-<slug>`, lowercase ASCII kebab-case |
| `namespace` | exactly `product-pro-max` |
| `slug` | required, unique unprefixed lowercase ASCII kebab-case |
| `description` | required nonempty English summary |
| `primary_cycle` | exactly one valid Product Model cycle; path grouping matches |
| `lifecycle` | nonempty list of `{cycle, phase?}`; primary cycle included, phase belongs to cycle |
| `tracks` | list of unique Product Model track IDs |
| `triggers` | object with semantic `include` and `exclude` lists |
| `inputs` | list of unique `{name, description, required: boolean}` |
| `outputs` | list of unique `{name, description, semantic_kind?}` |
| `related_skills` | list of unique `{skill_id, type}`, target must exist |
| `workflows` | list of unique `{workflow_id, role}`, workflow ID must exist |

Unknown fields and wrong types must be rejected rather than silently ignored. Duplicate YAML keys and unsafe tags must fail safe parsing; errors must identify a path and reason. Canonical skill directory, manifest ID and `SKILL.md` frontmatter name must be identical. `semantic_kind` vocabulary for Spec 002 is `evidence`, `gate`, `decision`; gates and decisions stay distinct and canonical IDs (if referenced) come from Product Model.

Relation types are only `prerequisite`, `complements`, `produces-input-for` as defined in `SKILL-MODEL.md`. Self-links, unknown references, duplicates and contradictory relations fail. Workflow membership is discovery-only, not orchestration.

Only `skills/` is distributable. `.agents/` development skills are excluded. `registry/skills.json` is generated deterministically from all valid manifests, sorted by ID. `generate` validates everything before an atomic write; `check` compares byte-for-byte without writing. Missing manifests and incomplete coverage fail validation.

General compatibility/deprecation/version policy, evaluations, release policy, catalog UI and ranking are outside Spec 002.

## Required sections

1. Purpose
2. Trigger
3. Inputs
4. Workflow
5. Evidence rules
6. Output contract
7. Quality gate
8. Stop conditions
9. Anti-patterns
10. Example

## Behavioral requirements

A skill must:

- be independently useful;
- remain composable;
- prefer reversible decisions under uncertainty;
- avoid inventing evidence;
- expose unknowns;
- produce a next action or decision;
- use deterministic verification where practical;
- communicate in the user's requested language.

## Stable output semantics

Outputs should distinguish:

- evidence/facts;
- assumptions;
- inference;
- risks;
- decision;
- gate;
- next action.

Canonical gate and decision IDs come from `model/product-model.json` and are explained in `PRODUCT-MODEL.md`.

Gate and decision MUST remain separate fields when a structured output contains both. A gate is a readiness/evidence judgment; a decision is the next action selected from context.

The rendering may be Markdown, YAML, or JSON, but the semantic distinction stays stable.

## Contribution rule

Do not add a new skill when an existing skill can solve the same problem with a small extension.
