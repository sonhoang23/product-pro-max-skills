# Pyramid / Funnel

**Phù hợp nhất cho:** hierarchy of needs, prioritization rank, value pyramid, conversion funnel, stack mức độ quan trọng của content.

## Hai hướng — chọn một
- **Pyramid** (đỉnh hướng lên) — apex hẹp = quan trọng nhất / hiếm nhất / giá trị nhất. Base rộng nhất / nền tảng nhất.
- **Funnel** (đỉnh hướng xuống) — đầu hẹp = conversion (nhóm nhỏ nhất). Phía trên rộng nhất / audience.

Không trộn hai hướng trong cùng một diagram.

## Quy ước layout
- 4–6 layer. Mỗi layer là trapezoid tạo bằng SVG `<polygon>` có 4 point.
- Layer height nhất quán (56–72px).
- Width giảm tuyến tính từ base lên apex (pyramid) hoặc từ trên xuống dưới (funnel). Khi hiển thị funnel data thực, width phải trung thực (tỷ lệ với count/percentage).
- Mỗi layer có:
  - **Name label** căn giữa trong trapezoid — Geist 12–14px 600.
  - **Sublabel** dưới hoặc cạnh name — Geist Mono 9–10px.
  - **Side annotation** (phải hoặc trái) — tuỳ chọn. Với funnel: đặt drop-off percentage tại đây (`−40%`).
- Fill: subtle graded tint HOẶC toàn bộ paper-2 với hairline divider (sạch hơn). Chọn một.
- Stroke: hairline 1px giữa layer; outer silhouette 1px muted hoặc ink.
- **Coral chỉ trên MỘT layer**: apex của pyramid, conversion layer của funnel hoặc critical bottleneck.
- Tuỳ chọn arrow trục ở margin trái + label Geist Mono (`rarer ↑`, `drop-off ↓`).

## Anti-pattern
- 7+ layer (khó đọc — nén hoặc tách).
- Pyramid cho data không có hierarchy (dùng tree hoặc bar chart).
- Width không trung thực (giả khoảng cách bằng nhau khi mức giảm không bằng nhau).
- Coral trên base layer (làm yếu tín hiệu “apex = rare”).

## Ví dụ
- `assets/example-pyramid.html` — minimal light
- `assets/example-pyramid-dark.html` — minimal dark
- `assets/example-pyramid-full.html` — full editorial
