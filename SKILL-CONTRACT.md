# Skill Contract

Every canonical skill lives at `skills/<skill-name>/SKILL.md`.

## Required frontmatter

- `name`
- `description`

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

The rendering may be Markdown, YAML or JSON, but the semantic fields stay stable.

## Contribution rule

Do not add a new skill when an existing skill can solve the same problem with a small extension.
