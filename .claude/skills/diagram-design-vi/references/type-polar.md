# Polar Chart

**Phù hợp nhất cho:** một quantitative series qua 4–8 category có thứ tự clockwise mang ý nghĩa.

## Input contract

```yaml
title: "Request demand by UTC window"
unit: "% of daily peak"
scale:
  min: 0
  max: 100
categories:
  - { label: "00–03", value: 32 }
  - { label: "03–06", value: 18 }
  - { label: "06–09", value: 24 }
  - { label: "09–12", value: 58 }
  - { label: "12–15", value: 100, focal: true }
  - { label: "15–18", value: 82 }
  - { label: "18–21", value: 76 }
  - { label: "21–24", value: 45 }
start_angle: -90
clockwise: true
source_note: "Illustrative normalized workload profile"
```

Quy tắc validation:

1. `scale.min` phải chính xác bằng `0`; radial scale bị truncate là không hợp lệ.
2. `scale.max` phải finite và lớn hơn `0`.
3. Mọi value phải finite và thỏa `0 <= value <= scale.max`.
4. Category label phải unique sau khi trim và số category phải 4–8.
5. Tối đa một category được đặt focal.
6. Category giữ nguyên input order; sort theo value sẽ phá circular meaning.

Missing value nằm ngoài phạm vi version đầu. Agent phải dừng và hỏi nên bỏ category hay cung cấp value; không được ép missing data thành zero.

## Quantitative encoding

Với category `i` trong `N`, value `v`, center `(cx, cy)`, outer radius `R`:

```text
theta_i = start_angle + clockwise_sign * 2π * i / N
radius_i = R * v / scale.max
x_i = cx + radius_i * cos(theta_i)
y_i = cy + radius_i * sin(theta_i)
```

Angle dùng radian khi tính; `start_angle` được cung cấp bằng degree và mặc định `-90`, đặt category đầu tại vị trí 12 giờ. `clockwise_sign` là `+1` cho clockwise mặc định và `-1` nếu ngược lại.

Value ray là line segment từ `(cx, cy)` tới `(x_i, y_i)`. Visible length phải tỷ lệ chính xác với `v`. Endpoint circle có radius cố định và không encode quantity nào khác. Không được có filled sector phía sau hoặc bên dưới value ray vì area sẽ cạnh tranh với radius encoding đã khai báo.

Element mang `data-polar-chart` phải là root `<svg>` của chart. Descendant chỉ được phép là `<g>`, `<line>`, `<circle>`, `<rect>`, `<text>`, `<title>`, `<desc>`; nested SVG, path, polygon, external reference, image và mọi element khác đều bị reject. Duplicate attribute, markup không khớp, SVG reference có giá trị URL, transform, CSS load qua `@import`/`url()` và CSS ảnh hưởng geometry đều bị cấm. Chart element không mang `class` hoặc inline `style`; document style không được dùng selector có thể match chart, ngoại trừ canonical root `svg` layout rule. External stylesheet duy nhất được phép là Google Fonts. Mỗi line phải mang chính xác một trong `data-polar-spoke`, `data-polar-ray` hoặc `data-polar-rule` và dùng stroke width đã khai báo cho role đó; spoke/ray geometry được verify trong sai số `min(0.75 px, 5% of R)`. Năm grid circle mang `data-polar-ring`, dùng `fill="none"`, stroke 0.8px, cùng chart center và đúng một lần cho các interval radius 20% tới 100%. Mọi endpoint circle mang `data-polar-marker` và dùng radius 4px, hoặc 5px cho focal category, với stroke 1.2px. Full-canvas background tuỳ chọn là rectangle duy nhất và mang `data-polar-background`. Allowlist fail-closed này ngăn contributor lách radius-only encoding bằng shape fill không annotate hoặc annotate sai.

### Zero

Với `v = 0`, `radius_i = 0`. Không render value ray và endpoint marker. Giữ faint full-radius category spoke và render numeric label của category là `0`. Một scale label duy nhất ở center cũng đánh dấu shared zero baseline. Không thêm minimum hub, minimum ray length, displaced marker hoặc visible magnitude nào khác.

## Quy ước layout

Version 1 hỗ trợ:

- một quantitative series;
- 4–8 category cách đều với clockwise order có ý nghĩa;
- shared linear scale với `min = 0` và `max > 0`;
- năm circular grid ring tại 20%, 40%, 60%, 80%, 100%;
- một focal category tuỳ chọn dùng accent token;
- ví dụ minimal light, minimal dark và full-editorial;
- category label horizontal, upright, bên ngoài outer ring;
- một numeric value label mỗi category.

Version 1 loại trừ:

- DISC, personality, competency và role-profile wheel có sector định tính;
- arbitrary point placement trong sector;
- filled quantitative wedge, gradient band hoặc donut hub;
- multiple series, negative value, logarithmic scale, unequal sector angle và hơn tám category;
- animation hoặc interaction.

Dùng Radar cho nhiều entity được chấm trên cùng criterion; Line cho hơn tám ordered time bucket; Bar khi circular order không mang thêm ý nghĩa.

## Geometry

Cả ba example dùng `viewBox="0 0 1000 520"`, center `(500, 230)`, `R = 160`.

- Grid ring: `r = 32, 64, 96, 128, 160`.
- Category spoke: center tới `R`, stroke rule 0.8px, không arrowhead.
- Non-focal value ray: stroke muted 2px; endpoint marker radius 4.
- Focal value ray: stroke accent 2.4px; endpoint marker radius 5.
- Ring label: `0.2 × max` tới `1.0 × max` chỉ trên first axis, Geist Mono 8px; example hiển thị `20, 40, 60, 80, 100`.
- Category label: tại `R + 28`, Geist Sans 11px semibold, horizontal và upright.
- Numeric label: tại `R + 44`, Geist Mono 8px; unit nằm ở chart subtitle thay vì lặp tám lần.
- Label anchor: `middle` trong 15 degree quanh vertical, `start` ở nửa phải, `end` ở nửa trái.
- Drawing order: background → rings → spokes → scale labels → non-focal rays → focal ray → endpoint markers → category labels → numeric labels → legend/source note.

Minimal example dùng full canvas 1000×520. Full-editorial example đặt cùng chart vào editorial frame hiện có và thêm summary card mà không đổi chart geometry.

## Visual treatment

- Tối đa một accent category. Mọi value ray khác dùng muted token.
- Circular ring và spoke là structural grid mark, không phải category color.
- Endpoint marker là lollipop head kích thước cố định, không phải bubble.
- Category label giữ horizontal; tangent rotation bị loại vì giảm scanability và thuộc qualitative wheel direction đã reject.
- Chart phải vẫn hiểu được trong grayscale: position và numeric label mang data; accent chỉ hướng chú ý.
- Accessible description của SVG nêu peak category, scale và clockwise category order mà không kể geometry.

## Complexity budget

- 4–8 category.
- Chính xác một quantitative series.
- Tối đa một focal category.
- Năm grid ring và một numeric value label mỗi category.
- Chỉ static output; split hoặc đổi type thay vì thêm interaction hay encoding thứ hai.

## Khi không nên dùng

- Multiple series → dùng Radar.
- Non-cyclic category → dùng Bar.
- Hơn tám ordered time bucket → dùng Line.
- Qualitative profile, arbitrary sector placement, negative value hoặc logarithmic scale → chọn representation phi-polar trung thực.

## Anti-pattern

- Donut hub hoặc inner baseline khác zero.
- Filled wedge, sector hoặc gradient band khiến area có vẻ encode magnitude.
- Category label tangent/rotated.
- Multiple series trên cùng polar chart.
- Truncated scale có minimum khác zero.
- Sort category theo value thay vì giữ circular order có ý nghĩa.
- Coi missing value là zero.

## Ví dụ

- `assets/example-polar.html` — minimal light.
- `assets/example-polar-dark.html` — minimal dark với cùng dataset và geometry.
- `assets/example-polar-full.html` — full editorial với ba summary card không bằng nhau và chart geometry không đổi.
