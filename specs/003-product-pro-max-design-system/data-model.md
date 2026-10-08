# Design Model: Presentation Contract (not Product Domain Model)

**Source**: [spec.md](spec.md). All entries are planned presentation objects. Canonical lifecycle/gate/decision semantics belong to Spec 001.

| Concept | Identity | Owned fields | Invariants |
| --- | --- | --- | --- |
| Token Set | `design-system/tokens.json` + revision | token schema rev, supported themes, roles, palettes, spacing, type, borders/strokes | Only authority for token values; stable names; no domain enums |
| Semantic Visual Role | role ID | description, variant map, contrast category, optionally density | Stable role ID under theme switching; every required role resolves |
| Theme | `light`, `dark` | role values and palette aliases | Full coverage for required roles; Light/Dark never change semantics |
| Density | `compact`, `default`, `spacious` | spacing/type/geometry scale aliases | No hiding required information; no label shrinking below readability floor |
| Primitive Treatment | stable primitive name | applicable role mapping and structural affordance | Renders source-provided meaning; cannot invent domain state |
| Surface | `readme`, `diagram`, `docs`, `brand` | allowed output formats, default theme, accessibility/export constraints | Same roles, deliberate surface-specific layouts |
| Presentation Snapshot | artifact path + token revision | resolved theme/density, source artifact path, exporter revision | Source and visual fingerprints tracked separately |
| Visual QA Record | artifact path + reviewed revision | static, browser, screen size, keyboard, contrast, evidence | Never infer `passed` for unchecked dimension |

## Dependency direction

1. Product/skill/Spec Kit authoritative source → semantic content/relations.
2. Token Set + Theme + Density + Surface → presentation values.
3. Renderer consumes (1) and (2); cannot write back to (1).
4. Output contains source trace and token-revision metadata and can be checked independently.

## Important non-relations

- A token named `success` is a rendering affordance, not the canonical `pass` gate-result enum.
- A visual path to `impact` in the hero is decorative; it is not a canonical lifecycle/phase path.
- `planned` vs `implemented` metadata is sourced from Spec Kit modeling/Atlas, never inferred from color.
