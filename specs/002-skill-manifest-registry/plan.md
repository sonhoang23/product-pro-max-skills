# Implementation Plan: Skill Manifest Registry

**Branch:** main | **Date:** 2026-10-08 | **Spec:** [spec.md](spec.md)

## Summary
Define the canonical Skill Model and sibling YAML manifest contract; migrate distributable skills to `skills/<primary_cycle>/ppmax-<slug>/`, generate a deterministic registry from canonical manifests, and enforce integrity checks. Keep Spec 001 Product Model authoritative.

## Technical Context
- Language: Python 3; pin version during implementation.
- Dependencies: Python standard library plus explicit safe YAML parser, pinned for CI.
- Storage: repository YAML/JSON files; no database.
- Testing: deterministic generator/checker, failure fixtures and migration semantic-parity checks.
- Target: local and CI file-based tooling; global-first English ASCII identifiers.
- Scale: all canonical skills; `.agents/` excluded.

## Constitution Check
Pre-design and post-design: PASS at planned-design level. Constitution and spec remain authoritative; manifest metadata is canonical, registry derived, skill behavior stays in SKILL.md, and Product Model lifecycle/gate/decision vocabularies are unchanged. No implementation or runtime PASS implied.

## Project Structure
```text
SKILL-MODEL.md
SKILL-CONTRACT.md
model/product-model.json
skills/<primary_cycle>/ppmax-<slug>/{SKILL.md,manifest.yaml}
registry/skills.json
scripts/ (generator and validator; planned)
.agents/skills/skill-creator-vi/ (contract consumer)
specs/002-skill-manifest-registry/{plan.md,research.md,data-model.md,quickstart.md,contracts/}
```

## Phase 0 Research
See [research.md](research.md). Decisions: sibling canonical YAML, deterministic derived JSON, read-only drift check, strict lifecycle/relations validation, careful migration, no cross-spec feature creep.

## Phase 1 Design
[data-model.md](data-model.md) defines manifest entities/invariants; [contracts/manifest-and-registry.md](contracts/manifest-and-registry.md) defines interface examples and validation failures; [quickstart.md](quickstart.md) defines future end-to-end validation evidence.

## Runtime Risk Design
| Risk ID | Status | Requirement refs | Evidence/trigger | Prevention design | Verification strategy |
|---|---|---|---|---|---|
| SR-01 drift | APPLIES | FR-023–026 | Registry differs from manifests | Read-only byte comparison | Tamper registry fixture |
| SR-02 identity | APPLIES | FR-005–009 | Duplicate/mismatched ID or path | Full-tree inventory and strict identity rules | Failure fixture matrix |
| SR-03 references | APPLIES | FR-012, FR-017–022 | Unknown Product Model/skill/workflow ID | Cross-reference against authoritative inventories | Broken reference fixtures |
| SR-04 partial write | APPLIES | FR-024–026 | Invalid YAML or generator failure | Validate all before atomic derived write | Malformed manifest fixture |
| SR-05 migration drift | APPLIES | FR-030–031 | Changed behavior/broken links | Inventory map and semantic diff | Pre/post behavior review |
| SR-06 tooling leakage | APPLIES | FR-023, FR-028–029 | Dev skill in registry | Only scan canonical skills/ path | Exclusion fixture |
| SR-07 network runtime | NOT_APPLICABLE | N/A — technical boundary | No network interface in feature | Local file contract only | Static audit |

Technical risk IDs above are feature-local, not invented canonical runtime-verification IDs; that companion is absent in this repository.

## Project Docs Promotion Plan
After implementation with verification and fresh implementation modeling: evaluate README.md, README.vi.md, SKILL-MODEL.md, SKILL-CONTRACT.md, docs/ARCHITECTURE.md and appropriate project-level diagrams via Diagram Check. No docs/ or project-level diagram updates during plan.

## Scope guard
Only planning artifacts. No modeling(plan), tasks, implementation, compatibility/deprecation policy, eval scoring, catalog UI, release policy or ranking contract.
