# Canonical catalog reset — 2026-10-09

## Decision

During foundation work, the 13 starter/demo distributable skills were withdrawn from the current catalog. This is a deliberate reset of product content, not a rollback of Spec 001–003 contracts.

Baseline commit: `34fc7d387f6bb3d0bfa143cae37fd69e82faf48a`. The former skill source and three executable workflow definitions remain recoverable in Git history. Historical Spec 002 migration and acceptance records refer to that past baseline and are not current runtime evidence.

## Current scope

- `skills/`: retain exactly the canonical Product Model cycle directories using `.gitkeep`; no distributable `ppmax-*` skill is currently published.
- `registry/skills.json`: deterministic derived empty catalog with `registry_version: 1` and `skills: []`.
- `workflows/`: retain three README design references; remove their executable `workflow.yaml` definitions until their skill dependencies are rebuilt.
- `.agents/`: development tools and skills remain untouched and outside the distributable catalog.
- `model/`, `schemas/`, `specs/`, `design-system/`, `templates/`: preserve foundation authority.
- Validator, generator, installer, and tests must accept zero current skills, while still rejecting invalid manifests, identities, stale registry output, and broken active workflow references.

## Re-entry gates

1. Analyze the canonical Product Model by cycle and phase; identify responsibilities and unmet capabilities before choosing skill count.
2. Design a bounded native skill with distinct trigger, inputs, artifacts, evidence, gate, and decision, referencing `SKILL-MODEL.md` and `SKILL-CONTRACT.md`.
3. Author the paired `skills/<primary-cycle>/ppmax-<slug>/{SKILL.md,manifest.yaml}`. Avoid invented evidence, overlapping responsibility, and premature cross-skill references.
4. Run `python scripts/generate_skill_registry.py generate`, `python scripts/validate_repo.py`, `python scripts/generate_skill_registry.py check`, and `python scripts/verify_skill_registry_release.py`; add focused evaluations. Declare runtime/browser evidence only when actually executed.
5. Activate a workflow only when every referenced skill is published and the end-to-end route is validated. Do not resurrect the three previous workflows automatically.

Do not advertise a demo skill or a conceptual workflow as a released capability.
