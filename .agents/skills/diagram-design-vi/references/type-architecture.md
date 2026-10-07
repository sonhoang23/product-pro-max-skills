# Architecture

**Phù hợp nhất cho:** tổng quan hệ thống, data-flow diagram, integration map, infra topology.

## Quy ước layout
- Nhóm component theo tier hoặc trust boundary (frontend → backend → data; public → private).
- Primary flow chạy trái→phải hoặc trên→dưới. Chọn một hướng và giữ nhất quán.
- Vẽ arrow trước box để z-order đặt connection sau component.
- 1–2 coral focal node: integration point chính, data store chính hoặc decision node quan trọng.
- Dashed boundary rectangle đánh dấu region (VPC, security group, trust zone); label nằm trên mask màu paper phủ lên boundary line.

## Kiểu connector

**BẮT BUỘC dùng connector vuông góc bo góc (orthogonal)** cho mọi connection không nằm ngang/dọc — dùng `<line>` chéo giữa các node lệch trục là hard fail (xem SKILL.md §6). Elbow path hai lần bẻ với `r=8`:

```svg
<!-- right+down: from (x1,y1) to (x2,y2), mid = (x1+x2)/2 -->
<path d="M x1,y1 H mid-8 Q mid,y1 mid,y1+8 V y2-8 Q mid,y2 mid+8,y2 H x2"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

Đảo dấu dọc cho right+up. Chỉ dùng `<line>` thẳng khi endpoint cùng x hoặc y. Arrow label nằm trên vertical segment, căn giữa ngang tại `mid` và giữa hai corner theo chiều dọc.

**Chọn port — dùng top/bottom cho connector dọc.** Khi destination nằm cao/thấp rõ rệt so với source, đi ra từ top/bottom edge của source và đi vào top/bottom edge của destination. Dùng single-bend L-path (horizontal → corner → vertical vào node), không dùng side port trái/phải:

```svg
<!-- entering a node from its bottom (destination above source) -->
<path d="M x1,y_src H x2-8 Q x2,y_src x2,y_src-8 V y_dst"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

Dành left/right port cho connection chủ yếu chạy ngang. Đi vào node từ cạnh bên trên một path chủ yếu theo chiều dọc khiến arrow trông như xuyên vào mặt node thay vì tới từ trên/dưới.

**Dashed path — cùng rule routing.** Optional, return, async và passive flow dùng `stroke-dasharray="4,3"` và stroke nhẹ hơn (`stroke-width="1"`). Áp dụng **cùng orthogonal routing, port selection và bridge/hop rule** như solid path — dash pattern chỉ truyền đạt semantic weight, không phải routing grammar khác. Khi dashed path và solid path phải cắt nhau, bridge dashed path vì theo định nghĩa nó ít quan trọng hơn.

**Zone label margin.** Để ≥16px giữa đáy zone eyebrow label và đỉnh node đầu tiên bên trong. Zone rect phải đủ cao để chứa header gap này (zone `y` = node_top − 32; label mask `y` = zone_y + 4).

## Arrow cắt nhau — bridge / hop

Khi hai orthogonal arrow phải cắt nhau, thêm arc nhỏ (hop/bridge) trên arrow **ít quan trọng hơn** tại điểm cắt. Arrow quan trọng hơn vẽ liên tục.

```svg
<!-- Horizontal hop over a vertical crossing at x=cx, on a line at y -->
<path d="M x1,y H cx-8 a 8,8 0 0,1 16,0 H x2"
      fill="none" stroke="…" stroke-width="1.2" marker-end="url(#arrow)"/>
```

`a 8,8 0 0,1 16,0` là SVG arc: rx=ry=8, large-arc=0, sweep=1 (cong lên về mặt thị giác), tiến 16px sang phải — tạo bump bán nguyệt radius 8px phía trên điểm cắt. Với vertical hop qua horizontal, dùng `a 8,8 0 0,0 0,16` trên vertical path.

Chọn arrow để bridge theo semantic importance (passive, secondary, write-back) hoặc stroke nhẹ hơn (dashed, muted). Không bao giờ bridge cả hai.

## Nhóm zone

Nhóm 2+ node cùng tier hoặc trust boundary bằng zone rect — vẽ **trước** arrow và node (z-order: bg → zones → arrows → nodes):

```svg
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>
<rect x="{label_x}" y="{y+4}" width="{label_w}" height="12" rx="2" fill="{paper}"/>
<text x="{label_cx}" y="{y+13}" fill="rgba(45,49,66,0.40)" font-size="7"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.14em">LAYER</text>
```

Quy tắc:
- Để 12–16px phía trên node đầu tiên bên trong — eyebrow label nằm trong margin này.
- Zone fill: `rgba(45,49,66,0.02)` (2% ink wash). Mạnh hơn sẽ cạnh tranh với node fill.
- Tối đa 3 zone mỗi diagram. Nhiều hơn sẽ giống swimlane (hãy dùng type đó).
- Dark mode: đổi `rgba(45,49,66,…)` → `rgba(245,245,245,…)` giữ nguyên opacity; label mask fill = `paper` (dark).

## Anti-pattern
- Mọi box đều coral (“cái này cũng quan trọng”) — hierarchy sụp.
- Bidirectional arrow khi một hướng đã rõ từ context.
- Legend nổi trong vùng diagram.

## Ví dụ
- `assets/example-architecture.html` — minimal light
- `assets/example-architecture-dark.html` — minimal dark
- `assets/example-architecture-full.html` — full editorial
