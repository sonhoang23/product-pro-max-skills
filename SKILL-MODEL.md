# Skill Model — Product Pro Max

**Status:** Canonical shared semantics for Spec 002. `model/product-model.json` remains the authority for cycles, phases, tracks, gates and decisions.

## Authority boundaries

- **Skill:** a bounded, distributable capability with a single stable canonical identity, trigger boundary, inputs, outputs and behavior.
- **SKILL.md:** behavioral authority (workflow steps, evidence safeguards, output instructions, quality gate and stopping conditions).
- **manifest.yaml:** machine-readable *metadata* authority (discovery, association and composition); it does not change or execute the behavior.
- **Skill Contract:** required format and compliance constraints for both artifacts. This model explains concepts; the contract validates them.
- **Registry:** derived, deterministic discovery projection of all valid manifests, never a separately edited semantic source.
- **Product Model:** authoritative lifecycle and evidence gate/decision vocabulary; a skill cannot invent canonical cycles, phases, tracks, gates or decisions.
- **Workflow:** `workflows/<workflow-id>/workflow.yaml` owns orchestration and transition order. A skill may reference workflow membership for discovery, but cannot redefine its steps or transitions.

## Identity and placement

The canonical namespace is `product-pro-max`. Each distributable skill uses `id: ppmax-<slug>`, with one unprefixed lowercase ASCII kebab-case `slug`. Folder, manifest ID and SKILL.md frontmatter `name` agree.

Exactly one `primary_cycle` determines physical placement at `skills/<primary_cycle>/ppmax-<slug>/`. The folder is a navigation aid, **not** the complete semantic lifecycle assignment. Manifest `lifecycle` may contain multiple valid `{cycle, phase?}` associations; the primary cycle must occur among them. `tracks` express cross-cutting applicability.

Repository-development tools under `.agents/` are not distributable skills, and never enter the derived registry.

## Selection boundary, inputs and outputs

- **Trigger inclusion:** positive circumstances in which a capability is relevant.
- **Trigger exclusion:** circumstances in which it must not be selected; excluded cases must not be lost when deriving registry metadata.
- **Inputs:** semantic named prerequisites, each with a description and required/optional boolean. These are not transport-specific parameters.
- **Outputs:** semantic named outcomes with descriptions and optional `semantic_kind`; an output kind can identify evidence, gate or decision but does not provide evidence itself.
- **Gate:** readiness/evidence assessment; **decision:** next action. They are distinct. Concrete IDs, where used, come from Product Model.

## Relationships

Each `related_skills` entry has a canonical `skill_id` and controlled `type`:

| Type | Meaning | Ordering |
|---|---|---|
| `prerequisite` | Referenced skill should precede this skill when the relationship applies | Directed |
| `complements` | Adjacent capability that adds value | No ordering |
| `produces-input-for` | This skill can provide semantic input to the referenced skill | Directed |

Self-reference, unresolved skill IDs, duplicate relations and contradictory relations are invalid. No per-skill ad hoc relation types.

A `workflows` relationship names an existing canonical workflow ID and a discovery-only role. Workflow definitions, not manifests, determine execution order.

## Change discipline

Changing labels, folder names or metadata for migration must preserve bounded responsibility, trigger intent, evidence requirements, outputs and workflow behavior. Versioning/deprecation, skill evaluation policy, releases, catalog UI and search ranking belong to later foundation specs.

## Comparable discovery contract (US2)

A consumer selects a skill using the manifest, never by guessing from folder location or parsing its instructions. `triggers.include` lists positive situations; `triggers.exclude` lists explicit negative selection boundaries. Both are lists of nonempty semantic descriptions, not executable predicates. Exclusions narrow selection even when inclusion matches; metadata never runs the skill.

Each `inputs` item has a stable semantic `name`, nonempty `description`, and literal boolean `required`; optional inputs use `required: false`, not an absent key. Each `outputs` item has a unique semantic `name`, `description`, and optional `semantic_kind` (`evidence`, `gate`, or `decision`). Output metadata describes expected meaning, not actual verified evidence.

`related_skills` references canonical IDs with typed relationships. `prerequisite` points from the current skill to one that should precede it; `produces-input-for` points toward a downstream consumer; `complements` imposes no order. These discovery hints are not execution commands. `workflows` declares membership as `{workflow_id, role}` with a nonempty human-readable discovery role, never the step order or transition rules. Duplicate semantic names or repeated references are invalid.
