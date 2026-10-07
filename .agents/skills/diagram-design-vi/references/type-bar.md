# Bar / Column Chart

**Phù hợp nhất cho:** so sánh các đại lượng rời rạc giữa category hoặc khoảng thời gian — sprint velocity, doanh thu theo tháng, mức độ sử dụng feature, cohort count. Dùng khi mỗi category có một giá trị số duy nhất và so sánh giữa các bar là thông điệp chính — hoặc, với biến thể dumbbell bên dưới, khi có đúng hai giá trị và **khoảng chênh giữa chúng** mới là thông điệp.

## Quy ước layout

- **Orientation:** bar dọc (column) là mặc định. Bar ngang phù hợp khi category label dài hoặc có hơn 8 category.
- **Plot area margins:** trái 80px cho y-axis label, dưới 60px cho x-axis label, trên 40px, phải 40px — nằm trong viewBox `0 0 1000 500`.
- **Giới hạn số bar:** 4–8 bar. Hơn 8 → group theo period hoặc tách thành hai chart.
- **Bar width:** ≥50% column pitch; khoảng trống không được lớn hơn bar. Điển hình: pitch=110px, bar=72px.
- **Y-axis gridline:** 4–6 horizontal line ở interval đều nhau. Stroke `rgba(45,49,66,0.08)` rất nhạt, 0.8px. X-axis baseline dùng `rgba(45,49,66,0.25)`, 1px.
- **Y-axis label:** Geist Mono 8px `muted`, căn phải tại x=72, tức 8px bên trái plot area.
- **X-axis label:** căn giữa dưới mỗi bar, Geist sans 11px weight 600 cho category name.
- **Value label:** Geist Mono 8px phía trên mỗi bar. Label của focal bar dùng `accent`; các bar khác dùng `muted`.
- **Focal bar:** tối đa 1 bar dùng accent fill/stroke. Tất cả bar còn lại dùng `muted @ 0.15` fill + `muted` stroke.
- **Y-axis line:** vertical `<line>` mảnh tại x=80 từ y=40 tới y=420.

### Bar element pattern

```svg
<!-- Opaque paper mask prevents bleed from background -->
<rect x="X" y="Y" width="W" height="H" fill="#f5f5f5"/>
<!-- Bar body -->
<rect x="X" y="Y" width="W" height="H" fill="rgba(79,93,117,0.15)" stroke="#4f5d75" stroke-width="1"/>
<!-- Value label above bar -->
<text x="X+W/2" y="Y-8" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace" text-anchor="middle">VALUE</text>
```

Với focal bar: thay fill bằng `rgba(235,108,54,0.12)`, stroke bằng `#eb6c36`, và label fill bằng `#eb6c36`.

## Anti-patterns

- Hơn 8 bar mà không group — không đọc được ở scale bình thường.
- Cắt ngắn y-axis, không bắt đầu từ 0 — làm méo so sánh magnitude.
- Accent hơn 1 bar — “cái gì cũng quan trọng” nghĩa là không có gì thực sự nổi bật.
- Bar 3D/extrusion — không shadow, không depth.
- Xoay category label quá 45°; hãy rút label hoặc chuyển sang chart ngang.

## Variants

- **Grouped bars:** hai bar mỗi category, đặt cạnh nhau. Dùng `accent` cho primary series và `series-1` cho secondary. Tối đa 2 group.
- **Stacked bars:** các segment xếp chồng thành total. Dùng `accent` cho focal segment; các phần còn lại dùng muted tint. Ghi total ở đầu mỗi stack.
- **Dumbbell:** mỗi category là một row, hai dot trên cùng một horizontal scale và được nối bằng hairline. Dùng cho so sánh hai trạng thái nơi *khoảng cách giữa hai đầu* là thông điệp — before/after, hai cohort, target vs actual. Chỉ hai series; dot thứ ba làm connector mất ý nghĩa và biến figure thành dot plot.

### Dumbbell layout

- **Orientation:** chỉ horizontal. Row xếp từ trên xuống và value axis chạy trái → phải; dumbbell dọc buộc category label phải xoay.
- **Plot area:** left margin 200px cho row label — thay cho margin 80px bên trên — nên `x` chạy 200→960, `y` chạy 40→420 trong `0 0 1000 500`. Row label căn phải tại x=188, Geist 11px 600 `ink`.
- **Rows:** vẫn dùng cap 4–8 bar. Pitch và origin được cố định theo row count để block luôn nằm trong plot band — pitch 64px từ y=96 sẽ tràn y=420 khi có 7 row:

  | rows | pitch | first row `y` | last row `y` |
  | --- | --- | --- | --- |
  | 4 | 88 | 96 | 360 |
  | 5 | 64 | 96 | 352 |
  | 6 | 64 | 76 | 396 |
  | 7 | 52 | 72 | 384 |
  | 8 | 48 | 68 | 404 |

- **Gridlines:** vertical tại mỗi tick, `rgba(45,49,66,0.08)` 0.8px, span y 56→408. Ở domain floor, axis line thay gridline thay vì vẽ đè đôi: `rgba(45,49,66,0.25)` 1px, y 40→420.
- **Tick labels:** căn giữa dưới mỗi gridline tại y=440, Geist Mono 8px `muted`.
- **Axis title:** value axis dùng axis label của family — Geist Mono 7px `muted`, `letter-spacing="0.14em"`, căn giữa x=580, y=456, dưới tick label và không chạm legend rule. Horizontal axis dùng dạng không xoay như scatter x-axis, không dùng `rotate(-90 24 230)` của y-axis ở column chart. Category axis không cần title vì row label đã tự định danh.
- **Dots:** `r=6`, position theo value. Style theo *series*: reference end hollow, paper fill, `muted` stroke 1.5px; focal end solid `accent` với 1px `ink` stroke. Vì vậy cả hai mark đều có boundary >3:1 dù accent fill tự thân không đạt — xem phần dưới. Fill weight, không phải hue, mang pairing signal.
- **Accent đánh dấu series, không phải focal row.** Solid dot lặp lại trên mọi row — đây là chỗ duy nhất variant này khác quy tắc one-accent phía trên, vì hai đầu phải phân biệt được ở từng cặp. Không accent thêm row “thay đổi nhiều nhất”; sort order đã mang rank.
- **Connector:** `rgba(45,49,66,0.55)` 1px, khai báo trước hai dot để dot cap line. Đây không phải axis hairline: connector nói rằng *hai dot này thuộc cùng một row*, nên phải vượt 3:1; 0.55 cho 3.19:1, còn 0.25 của axis chỉ cho 1.60:1.
- **Endpoint position được round, không bao giờ snap.** `x = 200 + (v − floor) ÷ (ceil − floor) × 760`, trong đó `floor` và `ceil` theo axis rule bên dưới, rồi round nearest integer pixel — tối đa 0.5px, nhỏ hơn một rendered pixel. Data coordinate được miễn quy tắc grid 4px; snap sẽ làm sai dữ liệu.
- **Value label nằm ngoài cặp và đặt theo geometry, không theo series.** Nếu focal value thấp hơn reference thì dot đảo bên; derive `x_left = min(x_ref, x_focal)` và `x_right = max(x_ref, x_focal)`: left label right-anchor tại `x_left − 12`, right label left-anchor tại `x_right + 12`, cùng baseline `y + 4`, Geist Mono 8px `muted`, mỗi label vẫn mang value của series tương ứng. Nếu offset theo start/end cố định, cả hai label sẽ lọt *vào trong* cặp ở mọi row giảm.
- **Floor exception.** Value nằm đúng domain floor sẽ đặt label tại x=188, right-anchor trên baseline `y + 4` — trùng đúng anchor/baseline của category label. Khi `x_left − 12 < 200`, center label đó phía trên dot tại baseline `y − 10`.
- **Legend:** hai key trên legend row — hollow dot rồi solid dot, mỗi key kèm series name. Circular key center tại `cy=493`, trùng center của bar legend key rect 10px ở y=488, nên cả hai nằm trên text baseline 497. Row order đặt trong legend hoặc source line, căn phải trên cùng row.

**Vì sao hai dot khác nhau bằng fill chứ không bằng hue.** Pattern focal bar phía trên (12% tint + accent stroke) không chuyển tốt sang dot 6px: tint 12% trên disc radius 6 chỉ đóng góp khoảng 14 square pixel màu, nên mark nhìn gần như chỉ còn stroke và cặp sẽ phân biệt chủ yếu bằng hue. Solid accent dot đối lập hollow dot phân biệt bằng shape, sống sót khi grayscale và color-vision deficiency, còn hue trở thành redundant encoding.

**Non-text contrast: boundary mới là thứ mang contrast, không phải fill.** Accent trên paper đạt 2.86:1 toàn skin, thấp hơn mức 3:1 mà WCAG 1.4.11 yêu cầu cho graphical object cần thiết để hiểu nội dung — và shape redundancy không miễn yêu cầu này, vì reader vẫn phải nhìn thấy edge của mark và line nối cặp. Vì vậy không giao hai nhiệm vụ đó cho accent: solid endpoint có 1px `ink` stroke (11.82:1 so với paper, 4.13:1 so với fill của chính nó), còn connector dùng 55% ink ở light và 40% ở dark (3.19:1 và 3.24:1). Hollow end đã đạt qua `muted` stroke ở 6.11:1 light và 7.07:1 dark. `scripts/verify-dumbbell.py` assert cả bốn điều kiện, nên thay tint sau này không thể âm thầm kéo một mark xuống dưới ngưỡng. Khác biệt hollow/solid vẫn là redundant encoding cho grayscale và color-vision deficiency — không collapse hai dot về cùng fill.

**Minimum drawn gap — không bao giờ clamp.** Cả hai dot dùng `r="6"`; hollow dot paint tới 6.75 vì stroke 1.5px straddle path, nên mark chạm nhau ở center separation 12.75px và dưới khoảng 16px cặp sẽ đọc thành một blob — trên domain 0–100 trải 760px, data gap khoảng 2.1 unit. **Không** kéo hai dot xa nhau để “cho rõ”: dịch dot khỏi scaled position sẽ phá shared-scale rule. Giữ position thật và thu cả hai mark, ví dụ r=4 chạm ở 8.75px, hoặc in hai value và đánh dấu row là quá gần để phân giải.

### Dumbbell element pattern

```svg
<!-- One row. Connector first so the dots cap it; labels outside the pair. -->
<line x1="458" y1="96" x2="740" y2="96" stroke="rgba(45,49,66,0.55)" stroke-width="1"/>
<circle cx="458" cy="96" r="6" fill="#f5f5f5" stroke="#4f5d75" stroke-width="1.5"/>
<circle cx="740" cy="96" r="6" fill="#eb6c36" stroke="#2d3142" stroke-width="1"/>
<text x="446" y="100" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace" text-anchor="end">34</text>
<text x="752" y="100" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace">71</text>
<text x="188" y="100" fill="#2d3142" font-size="11" font-weight="600" font-family="'Geist', sans-serif" text-anchor="end">Platform</text>
```

Giá trị 34 và 71 trên domain 0–100 cho 458.4 và 739.6, round thành 458 và 740. Nếu row này giảm thay vì tăng, accent dot sẽ nằm bên trái; hai anchor vẫn gắn với left/right và mỗi label vẫn mang value của series tương ứng.

**Dark theme.** Dot và label swap như kỳ vọng — hollow fill `#2d3142` với `#bfc0c0` stroke, solid `#f08a59` với `#f5f5f5` stroke, label `#bfc0c0`. **Hairline cũng phải invert:** gridline `rgba(245,245,245,0.08)`, axis `rgba(245,245,245,0.20)`, connector `rgba(245,245,245,0.40)` — connector tiếp tục nặng hơn axis vì cùng lý do 3:1. `rgba(45,49,66,…)` chính là dark paper color ở mọi alpha, nên nếu mang connector/gridline/axis từ light sang dark nguyên xi thì composite sẽ thành đúng 1.000:1 — gap encoding và scale cùng biến mất.

### Dumbbell honesty rules

- **Không bao giờ truncate value axis.** `floor` và `ceil` theo range của dữ liệu, không theo observed extreme — lấy `min` và `max` làm bounds *chính là truncation*. Gọi `lo` và `hi` là smallest/largest value, bốn case là đầy đủ: `lo >= 0` anchor `floor = 0` và round `ceil` lên quá `hi`; `hi <= 0` anchor `ceil = 0` và round `floor` xuống dưới `lo`; `lo < 0 < hi` bracket cả hai phía, và zero nằm trong plot — vẽ zero line ở scaled position bằng axis-line weight vì mọi gap được đọc tương quan với nó. Case thứ tư là case sign-based rule thường bỏ sót: **khi mọi value đều bằng zero**, `lo == hi == 0` làm `ceil - floor` bằng 0 và position formula chia cho zero, nên dùng finite fallback span (`floor = 0`, `ceil = 1` theo unit của data) và để mọi dot nằm trên floor — đó là sự thật. Data chỉ *chạm* zero đã thuộc hai case đầu, không cần case riêng. `scripts/verify-dumbbell.py` implement logic này và chứng minh coordinate hữu hạn cho cả bốn case. Plot width cố định nên domain hẹp hơn làm px-per-unit tăng và mọi gap trông rộng hơn: cùng 760px, gap 8 point là 61px trên axis 0–100 nhưng 152px trên axis 40–80. Ratio *giữa các row* vẫn giữ, nhưng mỗi gap phình ra so với frame — chính là cách reader đánh giá gap lớn hay nhỏ. Gap là toàn bộ claim của dumbbell, nên đây là cách phổ biến nhất để chart này nói dối.
- **Hai dot dùng cùng một scale và cùng một unit.** Label cả hai endpoint bằng value thật. Chỉ label focal end buộc reader phải tin geometry.
- **Connector là gap, không phải trajectory.** Nó encode khoảng cách giữa hai value và không nói gì về những gì xảy ra ở giữa — không intermediate point, không rate, không đảm bảo change monotonic. Không kể nó như một chuyển động theo thời gian.
- **Nêu rõ row order** trong legend hoặc source line: theo một endpoint, signed change, absolute change, hoặc thứ tự do subject cung cấp (chronological, geographic, ordinal). “By gap” là mơ hồ — phải nói signed hay absolute. Không được để order không nêu, vì nó đọc như arbitrary.
- **Row thiếu một endpoint phải được disclose, không impute và không silently drop.** Xóa incomplete category mà không nói sẽ thay population đang được so sánh. Hoặc vẽ known end và nêu missing value, hoặc bỏ row *và* ghi rõ row nào bị bỏ cùng lý do — lone dot nếu không giải thích sẽ không phân biệt được với hai dot trùng nhau, tức genuine zero gap.

Hai rule trong số này nằm ở formula chứ không ở drawing nên có thể kiểm tra executable: `scripts/verify-dumbbell.py` resolve domain qua mọi sign case và assert finite coordinate + mark contrast 3:1; `scripts/test-verify-dumbbell.py` exercise cả hai polarity — gồm all-zero, zero-touching data và các treatment dưới 3:1 đã bị thay thế. Checker đọc token trực tiếp từ file này, nên prose và threshold không thể drift. Nếu ship một dumbbell example, còn phải check drawn position so với value được in tại đó.

## Examples

- `assets/example-bar.html` — minimal light
- `assets/example-bar-dark.html` — minimal dark
- `assets/example-bar-full.html` — full editorial