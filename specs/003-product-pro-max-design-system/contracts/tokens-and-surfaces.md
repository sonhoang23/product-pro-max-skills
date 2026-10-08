# Contract: Tokens, theme resolution and output surfaces

**Status**: Planned contract. No implementation implied.  
**Authorities**: `spec.md` requirements; Product Model and existing diagram/modeling source retain semantic authority.

## Canonical token artifact (illustrative minimal shape)

```json
{
  "schema_version": 1,
  "revision": "0.1.0",
  "brand": "signal-protocol",
  "themes": {
    "light": { "surface": "#F7F9F4", "text-primary": "#17201B", "accent-brand": "#A3FF47" },
    "dark": { "surface": "#0B100F", "text-primary": "#F2F6F3", "accent-brand": "#A3FF47" }
  },
  "density": ["compact", "default", "spacious"]
}
```

This snippet is deliberately **incomplete** and MUST NOT be copied as the finished schema: required named roles, density assignments, typography, state mapping, contrast classes, and fallbacks must be defined and validated before production use.

## Mandatory role classes

- **Base**: surface, surface-elevated, text-primary, text-secondary, rule, border-strong, accent-brand, focus-ring, link.
- **Diagram**: node-fill, node-outline, edge, edge-emphasis, boundary, label-muted, gate-result emphasis, decision emphasis, evidence emphasis, and feedback path.
- **States**: success, warning, danger, neutral (presentation only), with explicit icon/label/shape mappings.
- **Geometry**: font families/fallbacks and type scale, spacing scale, stroke thickness, corner radii, and density multipliers.

All semantic role IDs are stable machine identifiers, not English display labels and not lifecycle IDs. Signal Lime (`#A3FF47`) is a brand-accent default only; applying it to text requires per-combination contrast checks.

## Resolution order

1. `design-system/tokens.json` in the **active repo root** is required.
2. Validate role completeness/schema/values; no implicit fallback to global VibeToolPro `style-guide.md` or `~/.diagram-design` profiles.
3. Resolve explicit `surface`, then its documented default theme (`readme`/`brand`: dark, `diagram`/`docs`: light).
4. Resolve optional explicit theme, accent preview, and density (preview accent is not a new official brand).
5. Produce deterministic presentation snapshot and embed token revision in generated outputs.
6. If local tokens are missing or invalid, fail visibly and leave existing artifacts untouched; an explicitly user-selected documented safe built-in fallback may be considered only outside canonical repo builds.

## Rendering invariants

- **Semantic input**: node/edge labels, node type, directed relations, gate result, decision identity, source, scope/truth, project artifact links.
- **Presentation input**: token values, theme, density, viewport/surface.
- Changing only presentation input must not alter semantic input or reorder/erase edges, gate results or decisions.
- The chosen color for success/warn/danger may emphasize labels but must never infer a decision from a gate result.
- No external fonts, CSS or JS in standalone HTML; glyph fallback is local.
- SVG diagram has `viewBox`, `title`, `desc` and source metadata; HTML navigation links point to `.html` or anchors as existing Atlas contract requires.

## Export surfaces

| Surface | Format | Theme default | Constraints |
| --- | --- | --- | --- |
| README | committed SVG Light/Dark + Markdown/`picture` selection | Dark hero + Light alternative | GitHub-safe, alt text/fallback, no JavaScript |
| HTML diagram | self-contained HTML with inline SVG and resolved CSS | Light | scope/truth/source links, `file://` support, keyboard/accessibility |
| Diagram Atlas / Ledger | self-contained HTML navigation | Light | no semantically new diagram entries, existing registry truth |
| Documentation | Markdown + local SVG/HTML links as supported | Light | readable raw GitHub markdown, discoverable links |
| Brand asset | local SVG; optional PNG export derivative | Dark | Signal Path + Wordmark, title safe area, variants derived from same roles |

## Failure matrix

| Case | Required handling |
| --- | --- |
| Missing/unknown role | Reject with role and source path; don't write partial output |
| Unsupported theme or density | Reject with allowed values |
| Invalid CSS color / insufficient contrast | Reject relevant official variant until corrected |
| Network unavailable | Already generated HTML/SVG remains legible |
| Long locale text | Reflow/scroll safely; do not silently clip essential labels |
| Global profile differs | Repo-local approved tokens still prevail |
| Stale token revision | Report visual presentation stale, not semantic model stale |
| Browser visual unavailable | Record `browser_visual=unavailable`, never PASS |

## Migration compatibility

Pilot = `specs/002-skill-manifest-registry/spec-diagram/skill-metadata-relations.html` plus Atlas. Preserve `planned` provenance, source links and all semantic labels and relationships. Export rollback-safe copy first. Completion requires validator evidence and reviewed screenshots; no mass migration by default.
