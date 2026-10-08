# Nested Containment

**Phù hợp nhất cho:** hierarchy qua containment — scope boundary, cascade CLAUDE.md, trust zone, folder nesting, blast radius. Bên ngoài = rộng hơn, bên trong = cụ thể hơn.

## Quy ước layout
- 3–5 rounded rectangle (`rx=8`) lồng nhau với inset padding nhất quán (khuyến nghị 24–32px ngang, 32–36px dọc).
- Mỗi level có label ở góc trên-trái theo kiểu eyebrow Geist Mono (7–8px, letter-spacing 0.14em). Label nằm trên mask rect màu paper đè lên top border của ring.
- Stroke hierarchy: ring ngoài mờ (`rgba(..,0.30–0.45)`), tăng dần thành muted, rồi ink, rồi coral ở innermost focal.
- Fill tăng opacity từ ngoài vào trong: `rgba(..,0.015)` → `rgba(..,0.025)` → accent-tint ở lớp trong cùng.
- File-icon glyph tuỳ chọn (rect có góc gập) trong mỗi level để gợi ý scope content.
- Callout Instrument Serif italic (xem `references/primitive-annotation.md`) — tối đa 1–2.

## Anti-pattern
- Hơn 6 level (thông tin biến mất dần vào trong).
- Padding giữa các level không đều — nesting lệch trông như lỗi.
- Content trong ring không thuộc hierarchy — dùng sibling diagram.
- Coral ở nhiều level — hierarchy bị sụp.

## Ví dụ
- `assets/example-nested.html` — minimal light
- `assets/example-nested-dark.html` — minimal dark
- `assets/example-nested-full.html` — full editorial
