# Line Chart

**Phù hợp nhất cho:** xu hướng liên tục theo thời gian hoặc một sequential index — signups theo tuần, revenue theo tháng, latency theo release. Dùng khi direction và rate of change giữa các point là thông điệp chính.

## Layout conventions

- **Plot area margins:** trái 80px, đáy 60px, trên 40px, phải 40px — trong `0 0 1000 500` viewBox.
- **Points:** 4–12 data point. Ít hơn → cân nhắc summary stat; nhiều hơn → aggregate thành period.
- **X-axis:** time/index label cách đều bên dưới plot. Dùng Geist Mono 8px, căn giữa tại `x` của từng point.
- **Y-axis gridlines:** 4–6 đường ngang theo interval đều nhau. Cùng faint treatment như bar chart.
- **Lines:** `<polyline>` với `fill="none"`. Focal series `stroke-width="1.8"`, series khác `"1.2"`.
- **Vertex dots:** chỉ focal series có dot (`r=4`, filled). Series khác chỉ có line.
- **Area fill (optional):** `<polygon>` đóng trở lại `y=420` — `x`-axis baseline — ở opacity 0.08. Chỉ dùng cho focal series khi area meaning thực sự quan trọng.
- **Multi-series:** tối đa 5 series. Focal = `accent`. Phần còn lại = `series-1`, `series-2`, `series-3`, `series-4` từ `style-guide.md`. Áp series palette theo thứ tự — không skip.
- **Legend:** horizontal strip ở đáy. Swatch = rect 16×8px với series fill/stroke. Một entry mỗi series.

### Polyline pattern

```svg
<!-- Focal series -->
<polyline points="x0,y0 x1,y1 x2,y2 ..."
          fill="none" stroke="#eb6c36" stroke-width="1.8" stroke-linejoin="round"/>
<!-- Dots at each point (focal only) -->
<circle cx="x0" cy="y0" r="4" fill="#eb6c36"/>

<!-- Non-focal series -->
<polyline points="x0,y0 x1,y1 ..."
          fill="none" stroke="#7c8f6f" stroke-width="1.2" stroke-linejoin="round"/>
```

## Anti-patterns

- Hơn 5 series — thành visual mush; giảm hoặc split.
- Line không bắt đầu từ shared zero baseline trừ khi được annotate rõ.
- Smoothed/spline curve khi underlying data là sampled — polyline mới trung thực.
- Dot trên mọi series khi có 4+ series — chỉ focal được dot.
- Y-axis không gồm zero khi absolute magnitude là phần quan trọng.
- Nối các discontinuous data segment mà không có visual gap.

## Variants

- **Slopegraph:** chính xác hai state, nhiều series, đọc như slope và rank change. Full spec bên dưới.
- **Ridgeline:** một distribution mỗi series, stacked với deliberate overlap trên một shared amplitude. Full spec bên dưới.
- **Bump chart:** rank movement qua 3–6 ordered snapshot, chỉ position. Full spec bên dưới.

---

### Slopegraph

**Phù hợp nhất cho:** thay đổi giữa chính xác **hai** state có thể so sánh qua nhiều series — hai năm, before/after, hai cohort, hai scenario. Cách đọc có ba lớp và không type nào khác cho cả ba cùng lúc: direction — đi lên hay xuống, steepness — nhanh đến đâu, và **crossings** — ai vượt ai. Slopegraph gốc của Tufte (*The Visual Display of Quantitative Information*, 1983) là một table mà các row được cho một góc nghiêng — mọi number vẫn được in, vì vậy ở đây cả hai endpoint vẫn giữ label.

Không dùng cho: ba state trở lên — đó là **line chart** ở trên hoặc bump chart; chỉ một series — viết thành câu; ranking tại một thời điểm không có change — dùng **bar chart**; hoặc hai biến đo bằng unit khác nhau — dùng **scatter plot**, vì một slope nối hai unit không cùng bản chất không có nghĩa.

#### Layout conventions

- **Hai vertical axis rule**, `y` 40 → 420 trong `0 0 1000 500` viewBox, tại `x` 320 và `x` 680. Plot nằm trong `x` 40 → 956 với rotated value-axis caption ở `x=24`, giống parent chart; legend giữ house rhythm — rule ở `y=462`, `LEGEND` ở `478`, key swatch ở `492`, text baseline `496` — để người đọc bar/line/treemap tìm thấy nó đúng chỗ quen thuộc.
- **Giữ horizontal run hẹp hơn plot height.** Run 360px so với height 380px đặt slope dốc nhất của shipped example khoảng 35° và slope phẳng nhất khoảng 4° — đủ để “halved” và “barely moved” trông như hai claim khác nhau. Mở run rộng hơn làm mọi slope phẳng dần về horizontal và đánh mất chính comparison mà type tồn tại để thể hiện; phần width thừa dành cho label gutter vì chúng cần nó.
- **Label gutters:** bên trái, name right-aligned kết thúc tại `x=272`, value right-aligned kết thúc tại `x=304`; mirror bên phải từ `x=696` cho value và `x=728` cho name. Size gutter theo name dài nhất — name đụng axis là thứ duy nhất không thể sửa bằng cách dịch coordinate.
- **State captions** dùng Geist Mono 9px, centered dưới mỗi axis ở `y=440`, tracking `0.14em`.
- **Series count:** 4–10 — cố ý nhiều hơn parent chart cap 5. Cap của line chart tồn tại vì polyline 8 vertex sẽ rối ở mid-plot; slopegraph không có mid-plot, nên ceiling ở đây do endpoint label collision. Dưới 4, một câu hoặc pair of bars ngắn hơn.
- **Không gridline.** Mỗi endpoint đã in value riêng, nên gridline không mang thông tin nào figure chưa nói; hai axis rule *chính là* scale. Đây là departure thật so với parent line chart, nơi gridline là công cụ đọc.
- **Domain:** chọn round bounds chứa data và nêu chúng trong source line. Shipped example chạy 100–550ms trên `y` 420 → 40, tức 0.84px mỗi millisecond. Include-zero rule của parent chart không ràng buộc ở đây: slope không đổi khi origin di chuyển, miễn **cả hai axis cùng di chuyển**. Tight domain vẫn magnify mọi slope như nhau, nên phải state bounds để reader calibrate.
- **Legend key là line 24px + dot**, không phải rect 16×8 của parent section — đây cũng là thứ `example-line.html` thực tế ship; parent prose ở điểm này đã stale. Slopegraph key phải show stroke weight vì weight là cue của focal series.
- **Dot ở cả hai endpoint** — `r=3` non-focal, `r=4` focal. Đây cũng là departure: line chart chỉ cho focal dot vì mỗi series có tám vertex, dot ở tất cả sẽ rối; slopegraph chỉ có hai vertex nên cả hai đều là nơi đọc value.
- **4px grid** áp dụng cho designed constants như axis position, gutter edge, state-caption baseline. Endpoint `y` là data-scaled nên được miễn; snap chúng sẽ làm sai data. Hai inherited constant cũng off-grid và giữ nguyên: legend rule `y=462` cùng `LEGEND`/source baseline `478`, được mọi chart trong `assets/` dùng. Match house rhythm ở đây quan trọng hơn ép grid vì bar/line/scatter/treemap cũng dùng cùng baseline này.

#### Colour

- **Một `accent`, còn lại là `ink` opacity ramp** — không dùng series palette. Trong line chart, hue là cách duy nhất để theo một series qua tám x-position nên `series-1`…`series-4` có lý do tồn tại. Ở đây mỗi series được name ở cả hai đầu, vì vậy hue sẽ là encoding thứ hai cho thứ label đã mang; nó tiêu focal rule mà không thêm meaning.
- **Ramp từ `0.80 → 0.62`**, ordered theo left-hand value. Hard floor là **`0.53`** — tại đó `ink` stroke vừa vượt 3:1 trên light paper; 0.53 đo 3.03:1, 0.52 đo 2.95:1. Mọi line ở đây là data, không phải decoration. Shipped ramp dừng 0.62 — 3.84:1 — thay vì sát floor, vì ramp mà lightest member chỉ vừa đọc được thì không còn room để thêm series.
- **Ramp không mua được identity giữa adjacent member.** 0.80 và 0.74 không phân biệt rõ ở 1.2px như shipped example cho thấy. Nó chỉ giúp trace một line qua crossing. Nó không bao giờ được là cách duy nhất phân biệt series; label mới làm việc đó.
- **Accent đánh dấu editorially focal series, không phải best hoặc biggest.** Trong shipped example, nó đánh dấu service duy nhất *tệ hơn*.
- **Focus được mang bởi stroke weight, không phải tone** — 2.4px focal so với 1.2px. Kiểm tra đúng token đang ship: `accent` đo **2.86:1 trên light paper** và 5.21:1 trên dark; trên light paper, focal line có contrast thấp hơn `ink` ramp mà nó phải nổi bật, vì vậy weight là cue duy nhất sống qua cả skin và greyscale.
- **Nói thẳng giới hạn còn lại.** 2.86:1 thấp hơn floor 3:1 của WCAG 1.4.11 cho graphical object; stroke dày hơn không nâng contrast ratio — chỉ giúp mark dễ tìm. Focal line vượt qua nhờ redundancy, không nhờ contrast: position và hai endpoint label (`ink` 11.8:1, `muted` 6.1:1) mang data, `accent` chỉ thêm *series nào focal*, điều mà legend nói bằng chữ và stroke weight lặp lại. Không meaning nào dựa vào accent đơn độc. Đây là property của skin accent trên light paper, không riêng variant này — focal bar, focal line, focal treemap cell đều inherit; sửa đúng nghĩa là đổi `accent` trong `style-guide.md`.
- **Label luôn `ink` cho name và `muted` cho value**, kể cả focal series. Accent text ở 9–11px không đạt AA trên light paper với 2.86:1. Focal value label màu accent là cách rất phổ biến làm slopegraph fail contrast dù nhìn có chủ đích.
- **Legend wording phải skin-neutral:** dùng "strongest tone", không dùng "darkest". Ramp là `ink`-at-opacity nên phần mạnh nhất là line tối nhất trên light paper nhưng lại sáng nhất trên dark. Legend nói “darker is higher” sẽ sai ở một trong hai skin dù render hoàn hảo.

#### Honest-data rule

**Cả hai axis phải dùng cùng scale và cùng unit.** Đây là toàn bộ claim của type: nếu scale khác nhau, angle của mọi line là fiction. `scripts/verify-slopegraph.py` enforce điều này.

- **Hai axis không bao giờ được khác nhau** — scale, origin hay transform. Shared *origin* quan trọng ngang shared scale: shift một axis làm mọi slope nghiêng cùng một lượng, rank giữa series vẫn đúng nhưng rate đều sai. Đây là lỗi khó thấy hơn, nên checker test slope và origin riêng.
- **Domain chặt hơn zero được phép; domain không disclosure thì không.** Cả hai axis cùng dùng 100–550 là legitimate vì moving origin để slope unchanged khi cả hai cùng move — đây là khác biệt giữa slopegraph và bar chart, nơi truncated baseline làm méo ratio. Tight window magnify mọi slope như nhau, nên source line phải nêu bounds. Log scale thì không: angle sẽ mất meaning.
- **Label cả hai endpoint bằng actual value.** Slope không magnitude chỉ là cảm giác.
- **Round một lần rồi vẽ từ rounded number**, để printed label, declared metadata và drawn `y` là ba cách nói cùng một number thay vì ba cơ hội bất đồng.
- **Nếu series thiếu một endpoint, drop nó và nói rõ.** Không interpolate để hoàn tất line.
- **Crowded endpoint label là data.** Hai series cách nhau vài phần mười khiến label chật *vì value gần nhau*. Dịch point để mở space biến problem legibility thành false statement — và lỗi này biến mất bằng mắt vì label giờ thoải mái cạnh vị trí sai. Đây là defect cụ thể mà gate phải bắt.
- **Hai series trùng cả hai endpoint thì không thể tách.** Merge thành một labeled line, hoặc drop một và ghi omission trong source line. Không nudge chúng ra — cùng lỗi ở trên với lý do nghe hợp lý hơn.
- **Straight line là connector, không phải trajectory.** Hai endpoint không nói gì về path giữa chúng: series có thể dip, spike hoặc cross ba lần. Vì vậy không đọc intermediate value từ slope và không annotate crossing bằng date. Shipped example có một service regress trong khi bốn service improve, nên line của nó cross ba line khác; không crossing nào được annotate.

#### Khai báo values

**Mọi visible string mang meaning đều được bind với attribute nói cùng điều đó.** Đây là toàn contract, vì mỗi unbound string là một chỗ figure có thể nói dối trong khi geometry check vẫn xanh.

```svg
<!-- State captions: data-axis names the axis, data-state binds the text -->
<text data-axis="from" data-state="BEFORE" x="320" y="440" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" letter-spacing="0.14em" text-anchor="middle">BEFORE</text>
<text data-axis="to" data-state="AFTER" x="680" y="440" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" letter-spacing="0.14em" text-anchor="middle">AFTER</text>

<!-- A series: the line declares its two values, and each of its four labels
     declares which series and which end it belongs to -->
<line data-series="Recommender" data-from="238" data-to="431"
      x1="320" y1="303.5" x2="680" y2="140.5" stroke="#eb6c36" stroke-width="2.4"/>
<circle cx="320" cy="303.5" r="4" fill="#eb6c36"/>
<circle cx="680" cy="140.5" r="4" fill="#eb6c36"/>
<text data-series="Recommender" data-end="from" data-role="name" x="272" y="307" fill="#2d3142" font-size="11" font-weight="600" font-family="'Geist', sans-serif" text-anchor="end">Recommender</text>
<text data-series="Recommender" data-end="from" x="304" y="307" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" text-anchor="end">238</text>
<text data-series="Recommender" data-end="to" x="696" y="144" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace">431</text>
<text data-series="Recommender" data-end="to" data-role="name" x="728" y="144" fill="#2d3142" font-size="11" font-weight="600" font-family="'Geist', sans-serif">Recommender</text>
```

Non-focal series: `stroke="rgba(45,49,66,0.68)"` tại `stroke-width="1.2"`, dot `r=3`, name `font-weight="500"`.

Mỗi binding bảo vệ một loại consistency:

| Binding | Nếu thiếu |
|---|---|
| `data-from` / `data-to` trên line | Checker phải đọc label; series mất label có thể biến mất khỏi verified set — đúng lỗ hổng từng để treemap cell ship lớn hơn 50%. |
| `data-end` trên value label | Printed number không thể cross-check với value nó tuyên bố. |
| `data-role="name"` trên name label | Hai series name có thể swap giữa row, đổi tên line, trong khi từng number vẫn đúng. |
| `data-axis` trên state caption | Caption có thể swap, đảo direction mọi slope. |
| `data-state` trên state caption | Chỉ swap hai visible string cũng đảo figure dù caption giữ vị trí. |

`scripts/verify-slopegraph.py` yêu cầu toàn bộ binding, cross-check mỗi visible string, và report label nào được vẽ gần endpoint của series khác hơn series mình — label ở wrong row tức là rename line.

**Không `transform` trên bất kỳ phần nào trong contract.** Checker đọc raw `x`/`y`; transform trên series line, bound label, ancestor `<g>` hoặc CSS rule làm rendered mark lệch khỏi number đã verify. `transform="translate(0 80)"` trên một line từng trượt endpoint 80px qua mọi green check. Transform bị reject thay vì resolve vì partial SVG transform implementation chỉ tạo ảo giác coverage. Bake offset vào coordinates. Rotated value-axis caption vẫn được phép vì không phải verified geometry hay bound label.

**Mỗi value label in một complete number.** Unit suffix như `208ms` được; thousands separator làm đổi value không được, và cũng không được có number thứ hai trong cùng label. Chỉ đọc numeric fragment đầu từng khiến label `512,000` khớp metadata `512`.

#### Anti-patterns — Slopegraph

- Different scale/unit/origin trên hai axis — lỗi nghiêm trọng nhất.
- Value axis có hai half không đồng ý, hoặc tight domain không state trong source line.
- Move endpoint để lấy chỗ cho label.
- Hơn 10 series hoặc ít hơn 4.
- Ba+ state column — đó là line/bump.
- Một hue mỗi series thay ink ramp + single accent.
- Value label màu accent hoặc text màu `soft` — 3.48:1 trên paper.
- Gridline hoặc value axis repeat number endpoint đã in.
- Annotate crossing bằng date hoặc đọc intermediate value từ slope.
- `transform` trên line/bound label/ancestor/CSS.
- Visible string không có binding.
- Curved connector — giữa hai point không có dữ liệu để curve qua.

---

### Ridgeline

**Phù hợp nhất cho:** một **distribution** mỗi series, stack theo fixed pitch với deliberate overlap, khi shape của mỗi distribution là story và các series trực tiếp comparable — request latency theo service, build duration theo pipeline, session length theo cohort. Line chart ở trên plot một value mỗi x; ridgeline plot cả distribution mỗi row, và cách đọc là silhouette: mass nằm ở đâu, chặt đến đâu, có second peak hay không. Một cặp p50/p99 không thể cho thấy bimodal service, và box plot flatten nó thành rectangle.

Không dùng cho: chỉ một distribution — đó là histogram; series khác unit hoặc x-range không thể share một x-scale; time series nơi mỗi row là một value mỗi moment; hoặc distribution giống nhau đến mức ridge là năm bản sao, trong trường hợp đó percentile table ngắn hơn.

#### Layout conventions

- **Một baseline mỗi ridge theo fixed pitch**, trong `0 0 1000 500`. Shipped example có năm baseline ở `y` 152/208/264/320/376, pitch 56px.
- **X-run giống slopegraph**, x 320 → 680, sampled ở 13 bin cách nhau 30px. Gutter đối xứng: name right-aligned kết thúc `x=304`, range bắt đầu `x=696`, cách plot 16px.
- **Name ở trái baseline, range ở phải**, mỗi cái trên row riêng của ridge — `y = baseline + 3.5`. Range là span của nonzero mass theo x-axis unit, number mà silhouette không thể cho.
- **Bin ticks** Geist Mono 9px tại `y=400`, centered trên bin position, tracking `0.14em`; x-axis caption `y=424`. Rotated amplitude caption ở `x=24` như parent chart.
- **Ridge count 3–12, bins 8–40.** Dưới 3 ridge không có family shape để compare; trên 12 stack quá cao. Dưới 8 bin outline chỉ là histogram đội curve; trên 40 bin hẹp hơn noise.
- **Straight segment giữa bin, đóng bằng `Z`.** Không spline: source line nói drawing unsmoothed, curve qua binned count sẽ đặt extrema giữa bin mà sample chưa đo. Draft cho phép Catmull-Rom với vertex đúng value; shipped grammar không dùng vì unsmoothed bin không cần footnote về curve invention.
- **Không gridline.** Baseline chính là rule, mỗi ridge in range của nó.

#### Colour — Ridgeline

Colour section của slopegraph giữ nguyên, thêm fill. Một accent cho focal ridge — stroke accent, fill accent `0.16` — các ridge khác dùng `ink` opacity ramp `0.80 → 0.62`, floor 0.53, ordered top-to-bottom. Focus do stroke weight 2.4px vs 1.2px, không tone. Label name luôn ink, range `muted`, kể cả focal.

- **Fill `ink` ở `0.12` cho non-focal ridge**, đủ thấp để hai overlap đọc như depth thay vì tone thứ ba. Đây là nơi type thật sự cần fill: outline một mình không nói bên nào của curve là mass.
- **Legend wording skin-neutral** — "strongest tone", không "darkest" vì ramp đổi lightness polarity giữa light/dark skin.
- **Accent đánh dấu ridge story tập trung vào**, không nhất thiết worst performer. Shipped example đánh dấu service có *shape* bất thường, không phải service chậm nhất.

#### Honest-data rule — Ridgeline

**Một amplitude cho mọi ridge, và nêu nó trong source line.** Đây là core claim: ridges stack để silhouette comparable; per-ridge normalization phá điều đó mà vẫn đẹp — một rare flat distribution dùng scale riêng có thể trông giống tight one. `scripts/verify-ridgeline.py` derive một amplitude và giữ mọi vertex của mọi ridge theo nó.

- **Baseline không được nói dối.** Mỗi ridge declare row nó rising from và row phải đúng fixed pitch với baseline rule chạy hết bin run. Nudge baseline lên để cho riêng ridge đó headroom là falsification giống private amplitude bằng arithmetic khác.
- **Mọi ridge share một x-scale.** Peak tại cùng x phải có cùng latency trên mọi row.
- **State overlap và giữ nó đúng là overlap.** Ridge được phép lấn vào row trên — đó là cách stack đọc như depth. Peak chạm row *hai bậc trên* bị occluded; fix bằng tăng pitch, không giảm amplitude riêng ridge.
- **Ridge bắt đầu và kết thúc trên chính baseline.** First/last bin = zero, outline đóng dọc baseline. Distribution bị clip mid-mass tạo cliff, và cliff sẽ đọc như data.
- **Không smoothing ngoài thứ footnote nói.** Shipped grammar không smooth. Nếu tương lai smooth, footnote phải name method, vertex vẫn đúng true value; spline invent second peak là không thể phân biệt bằng mắt với service có second peak thật.
- **Height là share, không volume.** Mỗi ridge normalized theo count của chính series trước shared amplitude; tallest ridge là concentrated nhất, không bận nhất. Source line phải nói rõ để reader không đọc traffic ngược.

#### Khai báo values — Ridgeline

Binding contract của slopegraph được áp cho area: outline khai báo bins và baseline, mọi visible string bind với thứ nó mô tả.

```svg
<line data-ridge="checkout-api" data-role="baseline" x1="320" y1="320" x2="680" y2="320" stroke="rgba(45,49,66,0.25)" stroke-width="1"/>
<path data-ridge="checkout-api" data-baseline="320" data-bins="0,1,6,17,21,14,8,6,7,9,7,4,0" d="M320,320 L350,317.6 L380,305.6 L410,279.2 L440,269.6 L470,286.4 L500,300.8 L530,305.6 L560,303.2 L590,298.4 L620,303.2 L650,310.4 L680,320 Z" fill="rgba(235,108,54,0.16)" stroke="#eb6c36" stroke-width="2.4" stroke-linejoin="round"/>
<text data-ridge="checkout-api" data-role="name" x="304" y="323.5" fill="#2d3142" font-size="11" font-weight="600" font-family="'Geist', sans-serif" text-anchor="end">checkout-api</text>
<text data-ridge="checkout-api" data-role="range" x="696" y="323.5" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace">40–440 ms</text>
<text data-tick="2" data-bin="240" x="500" y="400" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" letter-spacing="0.14em" text-anchor="middle">240</text>
```

`data-bins` là basis cho mọi geometry check, và là vocabulary riêng của Ridgeline: slopegraph bind `data-series` trên `<line>`, variant này bind `data-bins` trên `<path>`, hai gate không đọc attribute của nhau để không claim file của sibling. Future Line variant cũng nên có attribute riêng vì shared name khiến hai checker áp hai contract cùng lúc.

`data-baseline` làm moved row detectable; thiếu nó, checker phải infer zero từ drawing — chính thứ đang bị falsify. Printed range được cross-check với first/last nonzero bin qua tick scale của figure. `scripts/verify-ridgeline.py` kiểm tra amplitude, pitch, baseline rule, shared bins, segment grammar, overlap ceiling, focus pairing và mọi label binding; `scripts/test-verify-ridgeline.py` chứng minh check ở cả polarity và pin scope treaty với sibling gates.

**Không `transform` trên outline, baseline rule, bound label, ancestor `<g>` hoặc CSS rule** vì checker đọc raw coordinates; bake offset vào coordinate. Rotated amplitude caption được vì không phải verified geometry/bound label.

#### Anti-patterns — Ridgeline

- Per-ridge normalization hoặc second amplitude bất kỳ.
- Baseline lệch pitch để lấy headroom.
- Ridge sampled trên x-range khác nhau hoặc x-scale không in.
- Smoothing tạo peak giữa bin, đặc biệt khi footnote nói unsmoothed.
- Ridge clip mid-mass và đóng như cliff.
- Pitch quá chặt làm peak hide sau peak — tăng pitch.
- Một hue mỗi ridge thay ink ramp + single accent.
- Legend nói "darker is faster" — sai ở một skin.
- <3 hoặc >12 ridge.
- Đọc traffic từ ridge height hoặc source line cho phép hiểu nhầm như vậy.

---

### Bump chart

**Phù hợp nhất cho:** rank movement qua **3–6 ordered snapshot** khi position, không phải magnitude, là story — package popularity theo quarter, team standings theo sprint, top queries theo month. Slopegraph cho hai moment và giữ magnitude; bump chart bỏ magnitude hoàn toàn để show nhiều moment của pure position. Đây là trade-off cốt lõi: vertical axis là rank, mỗi row cách một rank, flat line nghĩa là “không ai displaced nó”, không phải “không gì thay đổi”.

Không dùng cho: đúng hai snapshot — slopegraph; magnitude story — một series download tăng gấp đôi nhưng rank không đổi sẽ thành flat, nên nếu surprise này quan trọng phải dùng line chart; <4 series hoặc >8 series.

#### Layout conventions

- **Một vertical axis rule mỗi snapshot**, evenly pitched trong plot, dùng gutter slopegraph: name right-aligned kết thúc `x=272`, first rank `x=304`; mirror phải từ rank `x=696`, name `x=728`. Shipped example có bốn axis tại x 320/440/560/680 — cùng run 360px như slopegraph, chia thành ba segment.
- **Rank row fixed pitch.** Shipped grid `y = 88 + 56 × (rank − 1)`. Rank là ordinal nên — khác slopegraph với data-scaled `y` — **mọi vertex nằm chính xác trên 4px grid**. `scripts/verify-bump.py` enforce row placement không tolerance. Không có lý do trung thực để vertex nằm giữa rank row.
- **Straight segment giữa adjacent snapshot, dot tại mọi vertex** — `r=3` non-focal, `r=4` focal. Không spline: curve giữa quarterly snapshot vẽ trajectory chưa đo. Draft gọi chúng subway curves và cấm hẳn.
- **Label ở first và last appearance** — name + rank `#1`…`#6`, sigil để rank không bị đọc như magnitude — ở cả hai đầu, trên chính row series và nằm trong gutter outboard của endpoint nó mô tả. Cả coordinate row và column đều bắt buộc/check: row nói label thuộc series nào, column nói thuộc *end* nào. First-end label trượt dọc row vào plot vẫn in rank đúng nhưng đọc theo snapshot sai.
- **Snapshot captions** Geist Mono 9px centered dưới axis, bind `data-axis` / `data-state` giống slopegraph.
- **Series 4–8, snapshot 3–6.** Hai snapshot là slopegraph; >6 làm column nén tới mức rank change khó follow.
- **Không gridline.** Dot là readable position, axis rule là column.

#### Colour — Bump

Giữ toàn bộ slopegraph colour rules: một accent cho editorial focal series; `ink` opacity ramp 0.80→0.62, floor 0.53 cho phần còn lại, ordered theo first-snapshot rank để legend có thể nói “strongest tone was highest-ranked” một cách skin-neutral; focus do stroke weight 2.4 vs 1.2 và dot size, không tone; label ink/`muted` kể cả focal. Accent đánh dấu series story tập trung vào, không phải winner — shipped example dùng cho package bị *tụt*.

#### Honest-data rule — Bump

**Nêu ranking key và tie-break trong source line.** Rank cố ý hide magnitude, nên footnote là nơi reader học "first" nghĩa gì và tại sao không hai series share row. `scripts/verify-bump.py` enforce geometry: mọi snapshot rank phải là permutation 1..N — duplicated rank là tie mà declared tie-break không thể tạo; skipped rank là empty row khiến reader tưởng có series không được vẽ.

- **Nếu ranking measure đổi definition giữa snapshot, chart invalid.** Rank dưới measure khác nhau không comparable.
- **Series enter late hoặc leave early phải start/stop.** Real gap là absence, không interpolate. Shipped grammar chưa có gap declaration, nên `verify-bump.py` hiện yêu cầu mọi series visit mọi snapshot — series có ít vertex hơn column là finding cho tới khi có explicit gap contract; nới rule mà không declaration sẽ cho truncated series giả thành deliberate exit.
- **Không smooth tie thành crossing.** Tie-break quyết order; drawing khác invent rank.
- **Không nudge vertex khỏi row** để né label — nó sẽ đọc như rank ở giữa hai rank, checker coi là lie.

#### Khai báo values — Bump

Binding contract của slopegraph được nâng lên một level: path khai báo ranks, mọi visible string bind tới thứ nó mô tả.

```svg
<path data-series="legacy-http" data-ranks="1,2,4,6" d="M320,88 L440,144 L560,256 L680,368" fill="none" stroke="#eb6c36" stroke-width="2.4"/>
<text data-series="legacy-http" data-end="first" data-role="name" x="272" y="91.5" fill="#2d3142" font-size="11" font-weight="600" font-family="'Geist', sans-serif" text-anchor="end">legacy-http</text>
<text data-series="legacy-http" data-end="first" data-role="rank" x="304" y="91.5" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" text-anchor="end">#1</text>
<text data-axis="0" data-state="Q1" x="320" y="416" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace" letter-spacing="0.14em" text-anchor="middle">Q1</text>
```

`data-ranks` là basis cho geometry check, nên series thiếu label vẫn ở verified set và missing label tự thành finding. `scripts/verify-bump.py` check grid, permutation, segments, dots, focus pairing, label binding, label placement ở cả hai axis và captions; `scripts/test-verify-bump.py` chứng minh từng check ở hai polarity. Gutter x được đọc từ figure — mọi label có cùng end+role phải agree trên một column — nên resize plot không cần đổi constant trong checker.

**Không `transform` trên path, bound label, ancestor `<g>` hoặc CSS geometry**, cùng lý do slopegraph/ridgeline: checker đọc raw coordinate.

## Examples

- `assets/example-line.html` — minimal light
- `assets/example-line-dark.html` — minimal dark
- `assets/example-line-full.html` — full editorial
- `assets/example-slopegraph.html` — slopegraph, minimal light
- `assets/example-slopegraph-dark.html` — slopegraph, minimal dark
- `assets/example-slopegraph-full.html` — slopegraph, full editorial
- `assets/example-ridgeline.html` — ridgeline, minimal light
- `assets/example-ridgeline-dark.html` — ridgeline, minimal dark
- `assets/example-ridgeline-full.html` — ridgeline, full editorial
- `assets/example-bump.html` — bump chart, minimal light
- `assets/example-bump-dark.html` — bump chart, minimal dark
- `assets/example-bump-full.html` — bump chart, full editorial
