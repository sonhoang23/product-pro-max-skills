# Signal Protocol visual primitive contract (Phase 2)

These are presentation instructions, not a product ontology. `model/product-model.json`, the Skill Registry and the feature's Spec Kit source determine all meaning. `speckit-system-modeling-vi` owns *what* to draw; `diagram-design-vi` owns *how* to draw it.

| Surface | Required visual roles | Primitive | Authority |
| --- | --- | --- | --- |
| README / brand | `surface`, `text-primary`, `accent-brand` | Symbol, wordmark, background | Brand display only |
| HTML diagram | `node-fill`, `node-outline`, `edge`, `edge-emphasis`, `boundary`, `label-muted`, `feedback-path` | Node, directed connector, boundary, feedback | Source-provided nodes/edges |
| Diagram / docs | `gate-result-emphasis`, `decision-emphasis`, `evidence-emphasis` | Distinct **labeled** node kinds; do not rely on color alone | Source's Gate result, Decision, evidence |
| Atlas / ledger | `surface`, `surface-elevated`, `link`, `text-primary`, `focus-ring` | Navigation and provenance | Existing diagram registry |
| All surfaces | `success`, `warning`, `danger`, `neutral` | Redundant status text + shape/icon + color | Source-provided status, never inferred |

## Semantic invariants

- A Gate result (`pass`, `warn`, `fail`) is **not** a workflow Decision (e.g. `continue`, `repeat`, `pivot`, `stop`). A Gate result NEVER implies a unique next Decision. Never turn `warn` into `revise` or infer a decision from a color.
- Every meaningful Gate / Decision / Evidence / status node MUST retain a visible type label and the exact source-provided value or identity. Color, line style or decorative icon are supplementary only.
- Preserve every source node ID, edge ID/direction, label, source path, navigation destination, scope, `planned`/`implemented` marker and accessible name. No role alias may inject semantic content.
- `accent-brand` is identity decoration, **not** an informational state role. On light backgrounds it must not be foreground text unless contrast is separately verified.
- Never replace modeling or renderers: these mappings are inputs to the existing `diagram-design-vi`, not a second semantics engine.
- All SVG diagrams require `<title>`, `<desc>`, `aria-labelledby` and a `viewBox`. All essential content must be readable without motion, color perception or network access.

## Presentation guarantees

Use repository-local `design-system/tokens.json`, with Light for diagrams/docs and Dark for README/brand by default. Fallback fonts are local/system only. Density changes spacing/stroke/type treatment, not element presence or semantic ordering. Long labels must wrap or allow scrolling; no hiding necessary nodes/edges. Source/Atlas links must retain actual targets. Concrete orthogonal connector/geometry guidance and piloted specimen belong to Phase 4 (T018–T026), not this foundation.
