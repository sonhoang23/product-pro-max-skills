# Product Model v1 Contract

## Canonical Authority
`model/product-model.json` owns canonical machine identifiers and relationships. `PRODUCT-MODEL.md` explains semantics but MUST NOT introduce identifiers absent from the machine model.

## Required Invariants
1. Cycle IDs are unique.
2. Phase IDs are globally unique.
3. Every phase belongs to exactly one cycle.
4. Track and loop IDs are unique within their namespaces.
5. Gate IDs are exactly `pass`, `warn`, and `fail`.
6. Decisions are independent from gate IDs.
7. Project statuses are independent from phases and decisions.
8. `schemas/skill-output.schema.json` gate and decision enums match the Product Model.
9. `schemas/project-state.schema.json` cycle, phase, and status enums match the Product Model.
10. Project state rejects invalid cycle/phase combinations.
11. `templates/project-state/project.yaml` uses canonical `cycle`, `phase`, and `status` fields.

## Identifier Convention
Machine IDs use lowercase English ASCII and kebab-case for multiple words. They remain untranslated in localized documentation.

## Gate and Decision Semantics
A gate answers: **How strong is the evidence/readiness?**  
A decision answers: **What should happen next?**

A gate result does not imply exactly one decision.

## Scope Boundary
This contract does not define skill metadata, registry structure, general compatibility guarantees, releases, or deprecation policy.
