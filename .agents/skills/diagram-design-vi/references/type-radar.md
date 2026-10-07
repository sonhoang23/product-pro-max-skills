# Radar / Spider

**Phù hợp nhất cho:** so sánh 3–5 entity trên 3–5 quantitative criterion cùng một normalized scale 0–N. Dùng cho capability matrix, product/backend evaluation, framework/team scorecard. Khi comparison table bắt đầu hết horizontal room, radar giúp shape của mỗi option đọc được ngay.

## Quy ước layout

- **N axis (3–5).** Chia đều trên regular polygon-N. Axis đầu ở top (`-90°`), đi clockwise. **Trên 5 → split hoặc dùng comparison table.**
- **Năm concentric grid ring** tại fraction `0.2 / 0.4 / 0.6 / 0.8 / 1.0` của radius. Vẽ thành closed polygon nối axis vertex ở fraction đó. Bốn inner ring dùng `rule` opacity 0.10; outer ring dùng `rule-solid` 0.20 để làm anchor mạnh hơn nhẹ.
- **Axis spoke** từ center tới mỗi outer vertex. Dùng `rule-solid` opacity 0.20. **Không arrowhead.**
- **Axis label:** một từ mỗi spoke — Jobs-minimal. Geist sans 11px weight 600. Đặt 16px ngoài outer ring theo axis vector. Top/bottom dùng `text-anchor="middle"`; phía phải dùng `start`; phía trái dùng `end`.
- **Scale tick**, ví dụ `2 4 6 8 10`, chỉ nằm trên **axis đầu tiên — top**. Gắn number lên mọi spoke làm chart rất nhanh bị clutter. Geist Mono 8px, `muted`, anchor end tại `cx − 6`.
- **Series polygon:** stroke 1.5px bằng series color, fill cùng color opacity `0.18` — `0.22` ở dark. Focal series stroke 1.8px, chỉ tăng nhẹ weight.
- **Vertex dot:** **chỉ focal series** có dot, `r=4` fill series color. Non-focal chỉ stroke + fill. Đây là load-bearing rule giữ chart đọc được khi có 4–5 series.
- **Drawing order:** dots-pattern bg → grid ring → axis spoke → axis label → scale tick → non-focal series — smallest area trước — → focal series → focal vertex dot → legend.
- **Legend:** horizontal strip dưới cùng theo global rule. Swatch là rect 16×8 — match polygon stroke+fill, không phải circle — rồi entity name. Khoảng 140px giữa entry. Có thể thêm italic tail phía phải giải thích rationale: `"One coral. Position is the signal — color reserved for the recommended option."`.

## Math

Với axis `i` — 0-indexed — trong tổng `N`, value `v` trên scale `S`, center `(cx, cy)`, outer radius `R`:

```
angle = -π/2 + 2π · i / N
x = cx + (v / S) · R · cos(angle)
y = cy + (v / S) · R · sin(angle)
```

Series values `[v0, v1, ..., v(N-1)]` trở thành `<polygon>` với `points="x0,y0 x1,y1 ..."`.

### Pre-computed reference — N=5, cx=500, cy=240, R=160, S=10, rounded integer

| Fraction `f` | i=0 (top) | i=1 | i=2 | i=3 | i=4 |
|---|---|---|---|---|---|
| 0.2 | 500,208 | 530,230 | 519,266 | 481,266 | 470,230 |
| 0.4 | 500,176 | 561,220 | 538,292 | 462,292 | 439,220 |
| 0.6 | 500,144 | 591,211 | 556,317 | 444,317 | 409,211 |
| 0.8 | 500,112 | 622,201 | 575,343 | 425,343 | 378,201 |
| 1.0 | 500,80  | 652,191 | 594,369 | 406,369 | 348,191 |

Với value bất kỳ `v` trên axis `i`, lấy unit offset từ row phía trên cho axis đó — ví dụ axis 1 có offset `(152, -49)` từ center — và scale theo `v/S`. **Xuất coordinate dạng integer — fractional pixel trong SVG render ổn, nhưng integer giữ source dễ scan.**

### Worked example — N=5

Series `[9, 8, 9, 9, 9]` trên scale 0–10 trở thành:

```svg
<polygon points="500,96 622,201 585,356 415,356 363,196"
         fill="rgba(235,108,54,0.18)" stroke="#eb6c36" stroke-width="1.8"/>
```

Mỗi vertex: `center + (v/10) · (outer_i − center)`, round tới pixel gần nhất.

## Series palette

Rule "1-focal" của skill vẫn giữ nguyên: `accent` dành cho focal series, còn editorial palette nhỏ — `series-1` tới `series-5`, định nghĩa trong [`style-guide.md`](style-guide.md) — dành cho non-focal series. Không dùng free-form color.

| Slot | Token | Light | Dark |
|---|---|---|---|
| Focal | `accent` | `#eb6c36` | `#f08a59` |
| 1 | `series-1` (sage) | `#7c8f6f` | `#9caf8f` |
| 2 | `series-2` (dusty-blue) | `#5e7a9b` | `#82a0c0` |
| 3 | `series-3` (mustard) | `#b8915a` | `#d3ad7a` |
| 4 | `series-4` (rust-brown) | `#9c6b50` | `#b88670` |
| 5 | `series-5` (slate) | `#6e6479` | `#8d8298` |

## Anti-pattern

- **Hơn 5 series** → mush. Split thành hai chart, ví dụ "best by latency" + "best by ops", hoặc chuyển sang comparison table.
- **Axis dùng native scale không nhất quán** — một cái 0–100, cái khác 0–1 — mà không normalize. **Luôn normalize về 0–N trước**; radar polygon so sánh *shape*, không phải absolute value.
- **Zero-baseline trick** — bắt inner ring từ v=5 để phóng đại difference. Grid bắt đầu ở 0; nếu difference nhỏ thì đó là cách đọc trung thực.
- **Dot trên mọi series.** Chỉ focal có dot. Thêm dot vào tất cả 4–5 series biến chart thành bead curtain.
- **Radar chỉ có 2 series** — comparison bar chart hoặc table 2 row rõ hơn.
- **Axis không quantitative.** Mọi axis phải đo được trên cùng normalized scale. "Speed" + "color" + "year" không thuộc radar.
- **Mono-font axis label.** Name dùng Geist sans theo global rule. Mono chỉ cho technical sublabel.
- **Rainbow palette.** Dù có token `series-*`, không cần dùng đủ 5; chỉ dùng đúng số non-focal entity.

## Ví dụ

- `assets/example-radar.html` — minimal light. 4 storage backend × 5 workload dimension, MinIO focal.
- `assets/example-radar-dark.html` — minimal dark, cùng data.
- `assets/example-radar-full.html` — full editorial: container framing + 4 card, một card mỗi backend, width khác nhau + footer.
