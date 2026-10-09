# Product Pro Max repository adapter (Phase 4)

Only used within `sonhoang23/product-pro-max-skills` after the active repository root has been established. It is a **presentation-only adapter**, not a new ontology or a replacement for `diagram-design-vi`.

**Resolve priority:** `design-system/tokens.json` → validate role completeness / contrast → `scripts/resolve_repo_style.py` → render using existing geometry type rules. A `.diagram-design` marker, working `references/style-guide.md` and `~/.diagram-design` profile **must not override** the canonical local role values. Missing/invalid local tokens must produce an explicit nonzero failure without fallback.

| Existing primitive | Repo token role | Note |
| --- | --- | --- |
| `paper`, `paper-2` | `surface`, `surface-elevated` | Backgrounds |
| `ink`, `muted`, `soft` | `text-primary`, `text-secondary`, `label-muted` | Meaningful text uses accessible role |
| `rule`, `rule-solid` | `rule`, `border-strong` | Lines and bounds |
| `accent` | `accent-brand` | Decorative emphasis only; never state text |
| `link` | `link` | HTML navigation |
| `node-fill`, `node-stroke` | `node-fill`, `node-outline` | Core node |
| `edge`, `focus` | `edge`, `focus-ring` | Directed connector and visible focus |

The full machine mapping is maintained in `scripts/resolve_repo_style.py` and its values come **only** from validated `tokens.json`. Keep source IDs, labels, `planned/implemented`, accessible names and direction unchanged. Gate result and Decision remain distinct even when their visual colors look similar. No shared/global profile writes.
