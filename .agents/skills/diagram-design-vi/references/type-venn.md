# Venn / Set Overlap

**Phù hợp nhất cho:** giao nhau của concept/domain, thuộc tính dùng chung giữa category, “nơi A gặp B”, frame kiểu ikigai (desirable × feasible × viable).

## Quy ước layout
- **Ưu tiên 2 hoặc 3 circle.** Tránh 4+ (khó đọc — dùng matrix thay thế).
- Circle stroke: hairline 1px, màu theo từng set (ink, muted, soft).
- Circle fill: tint opacity rất thấp — `rgba(45,49,66,0.04)` cho ink set, `rgba(79,93,117,0.05)` cho muted. Tint tự cộng dồn ở vùng overlap.
- Radius: bằng nhau khi set có size tương đương; tỷ lệ khi size khác nhau có ý nghĩa. Không giả size bằng nhau chỉ vì thẩm mỹ.
- **Set label** đặt ngoài circle, KHÔNG BAO GIỜ cắt stroke. Geist 12–14px 600 cho set name, sublabel Geist Mono 9px tuỳ chọn.
- **Intersection label** đặt trong vùng overlap, Geist 12px 600, căn giữa. Với overlap nhỏ, dùng leader line tới label ở vùng trống.
- **Coral accent** chỉ cho MỘT focal intersection — “sweet spot”. Hoặc coral label stroke, hoặc coral fill tint giới hạn bằng clipPath (`rgba(235,108,54,0.10)`).
- Center và radius của circle phải chia hết cho 4.

## Anti-pattern
- Region không có label — người đọc không biết set nào là set nào.
- Circle không overlap dù overlap là điểm chính.
- Circle bằng nhau khi set rõ ràng khác nhau (không trung thực).
- Coral trên nhiều overlap region (mất focal signal).
- Label nằm trên circle stroke (khó đọc).
- 4+ circle khi 2–3 là đủ.

## Ví dụ
- `assets/example-venn.html` — minimal light
- `assets/example-venn-dark.html` — minimal dark
- `assets/example-venn-full.html` — full editorial
