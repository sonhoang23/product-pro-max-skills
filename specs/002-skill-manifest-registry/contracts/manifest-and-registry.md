# Skill Manifest and Registry Contract

**Status:** Planned interface contract for Spec 002. Not implemented.

## Canonical file layout

Each distributable skill has the following files:

- `skills/<primary_cycle>/ppmax-<slug>/SKILL.md` — behavioral authority.
- `skills/<primary_cycle>/ppmax-<slug>/manifest.yaml` — metadata authority.

The `SKILL.md` frontmatter name must equal the manifest ID and directory name. Development tooling under `.agents/` is excluded.

## Manifest fields

| Field | Type | Constraint |
| --- | --- | --- |
| id | string | `ppmax-<slug>`; unique |
| namespace | string | `product-pro-max` |
| slug | string | stable ASCII kebab-case, no prefix |
| description | string | nonempty English responsibility summary |
| primary_cycle | string | Product Model canonical cycle |
| lifecycle | list | objects containing cycle and optional phase |
| tracks | list | canonical Product Model track IDs |
| triggers | object | positive include and negative exclude descriptions |
| inputs | list | name, description, required boolean |
| outputs | list | name, description and optional semantic_kind |
| related_skills | list | canonical skill ID and typed relation |
| workflows | list | existing workflow ID and discovery role |

The primary cycle must occur in lifecycle associations. Referenced phases must belong to their declared cycles. Input/output names and relations cannot be duplicated.

## Example canonical manifest

This is a contract fixture, **not** an existing registry member.

```yaml
id: ppmax-example-discovery
namespace: product-pro-max
slug: example-discovery
description: Investigates an uncertain product problem.
primary_cycle: opportunity
lifecycle:
  - cycle: opportunity
    phase: discovery
tracks:
  - research
triggers:
  include:
    - The user is exploring an unvalidated product problem.
  exclude:
    - The user asks to implement approved requirements.
inputs:
  - name: problem-context
    description: Context of the problem under investigation.
    required: true
outputs:
  - name: evidence-summary
    description: Findings and remaining uncertainties.
    semantic_kind: evidence
related_skills: []
workflows: []
```

## Relation vocabulary

- `prerequisite`: referenced skill should precede this skill when the relationship applies.
- `complements`: adjacent capability; no execution ordering implied.
- `produces-input-for`: this skill can supply semantic input to the referenced skill.

Unknown relation types, unresolved targets and self-links fail validation. Workflow references describe discovery relationships only; existing workflow definitions control execution order.

## Derived registry

Planned artifact: `registry/skills.json`. The top-level fields are `registry_version` (integer encoding marker 1) and `skills` (array sorted by ID). Each skill entry projects all manifest discovery fields plus its canonical directory path. Registry is generated from manifests, never edited as an independent source of authority. The encoding marker is not a skill compatibility or release policy.

## Generation and validation obligations

1. Enumerate all distributable skill paths and require both files.
2. Parse YAML safely; reject duplicate keys and malformed input.
3. Check canonical ID, namespace, folder, primary cycle, frontmatter name and field types.
4. Resolve lifecycle and relevant gate/decision semantics against Spec 001 Product Model.
5. Resolve typed skill relationships against discovered canonical IDs and workflow references against repository-defined workflows.
6. Reject duplicate IDs, missing manifests, invalid references, incomplete coverage and unexpected development skills.
7. Generate deterministic JSON only after successful validation; commit output via atomic replacement.
8. Read-only check must compare expected registry against existing registry without modifying files. A mismatch exits unsuccessfully and identifies the reason.

## Responsibility boundaries

Do not modify skill behavior to fit metadata normalization. Do not define versioning, deprecation, standardized evaluation, release, catalog UI or ranking policy in this contract; those belong to later foundation specs.
