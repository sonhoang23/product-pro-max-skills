# Skill Contract

Every canonical distributable skill lives at `skills/<primary_cycle>/ppmax-<slug>/SKILL.md`, with a sibling `manifest.yaml`. **Current status:** No distributable skills are published. The previous 13-skill migration was a historical Spec 002 baseline, now withdrawn for native-skill redesign. The contract remains authoritative for every future skill.

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
| `version` | optional while legacy manifests remain supported; when present, strict SemVer 2.0.0; owned by manifest, not SKILL.md or registry |
| `description` | required nonempty English summary |
| `primary_cycle` | exactly one valid Product Model cycle; path grouping matches |
| `lifecycle` | nonempty list of `{cycle, phase?}`; primary cycle included, phase belongs to cycle |
| `tracks` | list of unique Product Model track IDs |
| `triggers` | object with semantic `include` and `exclude` lists |
| `inputs` | list of unique `{name, description, required: boolean}` |
| `outputs` | list of unique `{name, description, semantic_kind?}` |
| `related_skills` | list of unique `{skill_id, type}`, target must exist |
| `workflows` | list of unique `{workflow_id, role}`, workflow ID must exist |

Unknown fields (other than the newly recognized optional `version`) and wrong types must be rejected rather than silently ignored. Duplicate YAML keys and unsafe tags must fail safe parsing; errors must identify a path and reason. Canonical skill directory, manifest ID and `SKILL.md` frontmatter name must be identical. `semantic_kind` vocabulary for Spec 002 is `evidence`, `gate`, `decision`; gates and decisions stay distinct and canonical IDs (if referenced) come from Product Model.

Relation types are only `prerequisite`, `complements`, `produces-input-for` as defined in `SKILL-MODEL.md`. Self-links, unknown references, duplicates and contradictory relations fail. Workflow membership is discovery-only, not orchestration.

Only `skills/` is distributable. `.agents/` development skills are excluded. `registry/skills.json` is generated deterministically from all valid manifests, sorted by ID. `generate` validates everything before an atomic write; `check` compares byte-for-byte without writing. Missing manifests and incomplete coverage fail validation.

Compatibility/deprecation policy is now scoped in Spec 004 [VERSIONING.md](VERSIONING.md); full compatibility assessor and release enforcement remain unimplemented. Evaluations, release automation, catalog UI and ranking are outside Spec 002.

## Consumer compatibility checks (Spec 004 — US2)

The implemented Python library in `scripts/compatibility_common.py` inspects
**declared** consumer dependencies and compares structural/semantic snapshots.
It is not yet an end-to-end release gate or proof of published support.
There are still no published distributable skills.

- A known consumer declares `consumer_id`, provider identity, source path,
  version range, required outputs/features, reader strictness and scope.
  Repo-local readers reveal code surfaces only, not accepted versions,
  release evidence or externally deployed consumers.
- A newly required input/field, removed required output, changed canonical
  Product Model ID/phase owner, rejected closed-enum member or changed
  expected file shape cannot be silently classified as compatible.
- Additive enum, optional field, output or metadata is **not** automatically
  MINOR-safe. Strict readers break; lenient readers require reader-specific
  acceptance evidence. Unknown tolerance remains `unassessed`.
- Trigger inclusion/exclusion, evidence safeguards, output meaning, quality
  gate/decision semantics and stopping conditions require semantic review and
  behavioral test evidence even when structural shape is unchanged.
- Inspect version ranges and supported-provider status per declared edge.
  Missing provider/version/range, incompatible or conflicting ranges and
  dependency cycles produce actionable non-green diagnostics. External readers
  absent from the inventory cannot be claimed universally compatible.
- Findings include stable component ID, source path, JSON pointer where
  relevant, affected consumers, classification and safe next action.
  `compatible`, `breaking`, `review_required`, `unassessed` are distinct;
  static checks do not imply runtime, migration or release proof.

Current verification: 15 synthetic US2 tests under Python 3.12
(GitHub Actions Validate #38388036169). Full CLI integration, project-state
migration, deprecation/release enforcement and native Windows parity are
future Spec 004 tasks. See `specs/004-versioning-compatibility/verification.md`.

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
