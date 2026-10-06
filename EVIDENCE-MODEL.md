# Evidence Model

Evidence is a first-class product artifact.

## Evidence classes

| Class | Meaning |
| --- | --- |
| `provided` | Supplied by the user or project files |
| `observed` | Directly observed behavior or system state |
| `researched` | External research with provenance |
| `measured` | Produced by a test, metric or benchmark |
| `inferred` | Reasoned conclusion from other evidence |
| `assumed` | Unverified belief required to proceed |

## Rules

1. Assumptions are never presented as facts.
2. Inferences should point to the evidence they depend on.
3. External research records provenance.
4. Runtime/test claims record the command, environment or observable result when possible.
5. Contradictory evidence is retained.
6. Confidence is qualitative by default: `low`, `medium`, `high`.
7. A gate can fail because evidence is missing even when an idea appears plausible.

Machine-readable shape: `schemas/evidence.schema.json`.
