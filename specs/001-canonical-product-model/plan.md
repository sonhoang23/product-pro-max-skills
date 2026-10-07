# Implementation Plan: Canonical Product Model

**Branch**: `main` | **Date**: 2026-10-07 | **Spec**: [spec.md](./spec.md)

## Summary
Create one canonical machine-readable Product Model, align dependent project-state and skill-output contracts, add deterministic drift checks, and promote verified semantics into public documentation.

## Technical Context
**Language/Version**: Python 3.12; JSON, Markdown, YAML-like project templates  
**Primary Dependencies**: Python standard library only  
**Storage**: Repository files  
**Testing**: `scripts/validate_repo.py` plus installer dry-run  
**Target Platform**: GitHub repository and Agent Skills-compatible consumers  
**Project Type**: Documentation/contracts/tooling repository  
**Constraints**: No new runtime dependency; English canonical IDs; no Spec 002–007 implementation; existing 13 skills and 3 workflows remain valid  
**Scale/Scope**: 10 lifecycle cycles, canonical phases, tracks/loops, 3 gate outcomes, decisions, and project statuses

## Constitution Check
All applicable principles PASS. The design uses one durable contract, deterministic validation, no added dependency, bounded scope, and English machine identifiers.

## Runtime Risk Design
No `.agents/skills/runtime-verification/SKILL.md` repository-development companion exists at the required path. The distributable `skills/runtime-verification/` content is not treated as development authority. This feature adds no application runtime surface.

## Project Structure
```text
model/product-model.json
schemas/product-model.schema.json
schemas/project-state.schema.json
schemas/skill-output.schema.json
templates/project-state/project.yaml
scripts/validate_repo.py
PRODUCT-MODEL.md
README.md
README.vi.md
docs/ARCHITECTURE.md
QUALITY-GATES.md
SKILL-CONTRACT.md
```

## Design

### Canonical model
`model/product-model.json` is the identifier/relationship authority; `schemas/product-model.schema.json` validates shape.

### Dependent schemas
Skill output mirrors canonical gates/decisions. Project state mirrors cycles/phases/statuses and constrains cycle/phase pairs.

### Drift guard
The validator checks identifier format, uniqueness, phase ownership, expected gate set, dependent schema equality, project-state template fields/values, and existing workflow references.

### Documentation
`PRODUCT-MODEL.md` is the normative human explanation. README and architecture docs summarize and link instead of owning independent enums.

## Project Docs Promotion Plan
After core model, schemas, template, and validator pass validation:
- promote navigation/summary into `README.md` and `README.vi.md`;
- promote hierarchy/authority into `docs/ARCHITECTURE.md`;
- clarify gate vs decision in `QUALITY-GATES.md`;
- point `SKILL-CONTRACT.md` to canonical output semantics.

No project diagram is required; tables and machine-readable data are clearer for this ontology.
