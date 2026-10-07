# Layer Stack

**Phù hợp nhất cho:** OSI model, CSS cascade, context hierarchy, tech stack, abstraction layer, memory hierarchy.

## Quy ước layout
- Các band ngang xếp dọc. Mỗi layer là rectangle full-width (cùng x, cùng width). Tổng 4–6 layer.
- Layer cao 56–72px, width thường 800–880px trong viewBox 1000px.
- Mỗi row chứa (trái→phải):
  1. **Index tag** ở xa bên trái (`L3`, `07`, `APPLICATION`) — eyebrow Geist Mono 8–9px.
  2. **Layer name** hơi lệch phải khỏi vùng center-left — Geist 14–16px 600.
  3. **Sublabel / note** ở xa bên phải — Geist Mono 9–10px muted.
- Border giữa layer: hairline 1px `rgba(45,49,66,0.12)`. Outer silhouette 1px ink hoặc muted.
- Fill: hoặc xen kẽ subtle shade (paper / paper-2), hoặc toàn bộ paper với hairline divider. Chọn một cách và giữ nhất quán.
- Direction indicator ở margin **TRÁI** (ngoài stack): arrow lên/xuống nhỏ + label Geist Mono (`abstraction ↑`, `packets ↓`).
- Coral trên **một** focal layer (stroke + tint fill nhẹ) — bottleneck, pay-rent layer hoặc layer đang được bàn tới.

## Anti-pattern
- Các layer không thực sự có hierarchy (dùng swimlane hoặc architecture).
- Nhảy số layer (thiếu L4 giữa L3 và L5 mà không giải thích).
- Mỗi layer một màu khác — hierarchy biến mất.
- Layer height không nhất quán mà không có lý do.

## Ví dụ
- `assets/example-layers.html` — minimal light
- `assets/example-layers-dark.html` — minimal dark
- `assets/example-layers-full.html` — full editorial
