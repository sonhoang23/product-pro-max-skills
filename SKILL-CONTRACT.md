# Skill Contract

Every canonical distributable skill lives at `skills/<skill-name>/SKILL.md`.

## Required frontmatter

- `name`
- `description`

Metadata expansion is intentionally deferred to the dedicated skill manifest/registry foundation spec.

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
