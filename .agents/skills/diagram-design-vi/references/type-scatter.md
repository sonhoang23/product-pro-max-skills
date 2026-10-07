# Scatter Plot

**Phù hợp nhất cho:** tương quan và phân bố — hai biến liên tục được vẽ đối chiếu với nhau. Dùng khi mối quan hệ (hoặc không có mối quan hệ) giữa các biến là thông điệp chính, hoặc khi cần nhận diện cluster, outlier và các điểm có hiệu suất cao/thấp.

## Quy ước layout

- **Lề vùng plot:** trái 80px, dưới 60px, trên 40px, phải 40px — bên trong viewBox `0 0 1000 500`.
- **Số point:** 5–30 point. Ít hơn → mô tả quan hệ bằng prose; nhiều hơn → gom thành density contour.
- **Trục:** X tại y=420 (baseline), Y tại x=80. Cả hai dùng label gridline Geist Mono 8px. Mỗi trục có 4–6 gridline cách đều.
- **Shape point:** `<circle>` r=5 cho point thường, r=6 cho focal. Focal dùng fill `accent`. Các point khác dùng fill `muted @ 0.20` + stroke `muted`.
- **Label trên point (tuỳ chọn):** Geist Mono 8px đặt cạnh point. Dùng rect mask fill paper phía sau label. Chỉ label tối đa 2–3 point; không label tất cả.
- **Trend line (tuỳ chọn):** `<line>` từ dưới-trái lên trên-phải, stroke `rgba(45,49,66,0.25)` dashed `4,3`. Không bao giờ ép một perfect fit — chỉ thêm khi trend nhìn thấy rõ bằng mắt.
- **Quadrant divider (tuỳ chọn):** line dashed nhẹ tại median x và y để chia thành quadrant. Label mỗi quadrant bằng Geist Mono 8px, màu muted.

### Mẫu point

```svg
<!-- Non-focal point — paper mask + circle -->
<circle cx="X" cy="Y" r="5" fill="#f5f5f5"/>
<circle cx="X" cy="Y" r="5" fill="rgba(79,93,117,0.20)" stroke="#4f5d75" stroke-width="1"/>

<!-- Focal point -->
<circle cx="X" cy="Y" r="6" fill="#f5f5f5"/>
<circle cx="X" cy="Y" r="6" fill="rgba(235,108,54,0.15)" stroke="#eb6c36" stroke-width="1.2"/>
```

## Anti-pattern

- Hơn 30 point mà không clustering (jitter/mush) — khi chính đám đông là câu chuyện, chuyển sang **beeswarm variant** bên dưới; beeswarm pack point thay vì jitter.
- Ép trend line khi data thực sự phân tán — không trung thực.
- Label trên mọi point — chỉ label focal và 1–2 outlier đáng chú ý.
- Tự ý encode bubble size trong scatter thường. Nhận thức về size đủ kém để cần một contract riêng: khi giá trị thứ ba thực sự quan trọng, dùng **bubble variant** bên dưới, trong đó area được buộc vào value và được gate bởi `scripts/verify-bubble.py`; nếu không, một label trục thứ ba hoặc focal choice truyền đạt rẻ hơn.
- Trục không gồm zero khi absolute position quan trọng; hoặc trục lại gồm zero khi range rất hẹp và nằm xa zero.

### Bubble

**Phù hợp nhất cho:** ba quantity trên mỗi item — x, y và một magnitude — khi cách đọc *kết hợp* mới là câu chuyện: item nào vừa ở vị trí xấu vừa có footprint lớn. Shipped example vẽ service theo p95 latency và error rate, với area là request volume; điểm của figure chính là phép “nhân” mà scatter hai biến không thể làm — service chậm nhất gần như không đáng kể và service rủi ro nhất không phải service chậm nhất.

Không dùng cho: giá trị thứ ba thực chất là category (dùng focal accent hoặc facet); chỉ có hai biến (đó là parent scatter — size trên tất cả point chỉ là trang trí); hoặc magnitude trải qua nhiều order of magnitude (bubble nhỏ biến mất; hãy bin hoặc đưa magnitude lên một axis riêng).

#### Quy ước layout

- **Cùng plot frame với parent:** lề trái 80, dưới 60, trên 40, phải 40 trong `0 0 1000 500`; rule X tại `y=420`, rule Y tại `x=80`; gridline ở các vị trí của parent; legend theo house rhythm — rule `y=462`, `LEGEND` tại `478`, key tại `490`.
- **Số item:** 5–15. Dưới 5, phép kiểm tra scale leave-one-out không có đủ điểm tựa và table truyền đạt tốt hơn; trên 15, area bắt đầu chồng và cách đọc thoái hoá thành density cloud — đó là territory của contour parent, không phải type này.
- **Radius từ area:** `r = K·√value` với duy nhất một constant K cho toàn figure, chọn để bubble lớn nhất vẫn nằm trong plot (shipped example dùng `K = 1.4` trên requests-per-second, cho radius 10.8–42px). Nêu area scale trong source line.
- **Axis tick có binding:** mọi tick mang `data-tick` (axis) và `data-value` (number nó in). 4–6 tick mỗi axis ở interval đều nhau, Geist Mono 8px, placement giống parent.
- **Paper underlay cho mỗi bubble**, cùng radius, vẽ ngay phía dưới — translucent fill không được để gridline xuyên qua, vì fill phải đọc như một solid area duy nhất.
- **Thứ tự vẽ: lớn nhất trước.** Bubble nhỏ vẽ sớm sẽ bị giant vẽ sau chôn mất và area không còn đọc được. `verify-bubble.py` kiểm tra paint order trên mọi cặp overlap.
- **Label:** focal bubble cộng tối đa 2–3 outlier người đọc sẽ tìm, Geist Mono 8px small-caps trên paper mask; mỗi label bind với bubble bằng `data-name`. Không bao giờ label tất cả.
- **4px grid** áp dụng cho designed constants — axis rule, gridline, tick baseline, legend row. Bubble centre và radius được scale từ data nên được miễn; snap chúng sẽ làm sai data.

#### Màu

- **Một accent bubble, và một opacity ramp của `ink` cho mọi bubble còn lại** — không bao giờ một hue cho mỗi item. Bubble đã label được gọi tên ngay tại vị trí của nó, nên hue chỉ encode lại thứ label đã mang.
- **Accent đánh dấu item focal về mặt biên tập, không phải bubble lớn nhất hay item có một metric xấu nhất.** Shipped example đánh dấu service có *tổ hợp* rủi ro: gần peak volume trên error rate tệ nhất.
- **Ramp chạy faintest-on-largest** (fill 0.14 ở bubble lớn nhất tới 0.35 ở bubble nhỏ nhất trong shipped example). Đây là ink-mass compensation, không phải encoding: giant bubble cùng opacity với small bubble sẽ thống trị page chỉ vì area, nên opacity giảm khi area tăng để mọi bubble có visual weight tương đương. Tone **không** phải biến thứ tư — legend phải nói đầu nào của ramp tương ứng với đầu nào bằng ngôn ngữ trung tính với skin (`"faintest fill is the largest bubble"` đúng ở cả hai skin; `"darkest"` sẽ sai ở một skin).
- **Mọi bubble giữ stroke `muted`** (6.11:1 trên light paper, 7.07:1 trên dark) — fill ở opacity thấp hơn nhiều 3:1, nên stroke là thứ đáp ứng WCAG 1.4.11 cho edge của mark. Accent stroke của focal bubble đo 2.86:1 trên light paper; giống focal bar, line và slopegraph, data của nó được truyền đạt dư thừa — position, label và legend gọi tên bằng chữ — accent chỉ bổ sung *bubble nào là focal*.
- **Label giữ `ink` hoặc `muted`**, kể cả focal. Accent text ở 8px không đạt AA trên light paper.

#### Quy tắc trung thực với data

**Area encode giá trị thứ ba — tuyệt đối không phải radius.** Sizing theo radius bình phương claim: value lớn 6× sẽ trông như lượng mực 36×. `scripts/verify-bubble.py` gate điều này cùng với hai axis scale.

- **Một linear scale trên mỗi axis, mọi bubble dùng chung.** Dịch một bubble sang bên để tránh crowding sẽ đọc thành một number khác; crowded bubble chính là data, và cách sửa trung thực là hairline separation nhờ rule largest-first hoặc giảm item — không bao giờ dịch centre.
- **Axis gồm zero hoặc source line phải nêu bounds.** Position của bubble được đọc so với origin theo cách slopegraph không bị. Không dùng log scale nếu không nói rõ — và area cạnh log axis là cách đọc phần lớn audience dễ hiểu sai, nên tốt nhất tránh hẳn.
- **Item bị bỏ phải được đếm trong footnote.** Bubble chart lặng lẽ bỏ giant “bất tiện” cũng là lời nói dối như truncated axis.
- **Magnitude không dương không thể là bubble.** Area không có sign; bỏ item và nói rõ.
- **Round một lần, rồi draw từ số đã round**, để declared value và geometry được vẽ là hai cách nói cùng một number thay vì hai cơ hội lệch nhau.

#### Khai báo value

**Mọi quantity được vẽ phải bind vào attribute nêu chính value nó encode.** Data circle mang cả ba value; paper underlay chỉ là scenery và không mang data.

```svg
<!-- A bubble: position from two shared linear scales, area from the size.
     x = 80 + 1.76·ms, y = 420 - 95·pct, r = 1.4·√(req/s) -->
<circle cx="537.6" cy="154" r="38.6" fill="#f5f5f5"/>
<circle data-name="Payments" data-x="260" data-y="2.8" data-size="760"
        cx="537.6" cy="154" r="38.6"
        fill="rgba(235,108,54,0.15)" stroke="#eb6c36" stroke-width="1.2"/>

<!-- Its label, bound to the bubble it names -->
<text data-name="Payments" data-role="label" x="538" y="108" fill="#2d3142" font-size="8" font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">PAYMENTS</text>

<!-- An axis tick, bound to the number it prints -->
<text data-tick="x" data-value="300" x="608" y="440" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace" text-anchor="middle">300</text>
```

Mỗi binding đem lại gì, và mất gì nếu bỏ:

| Binding | Nếu thiếu |
|---|---|
| `data-x` / `data-y` trên circle | Không bắt được centre bị nudge — vị trí được vẽ sẽ là tuyên bố duy nhất về value. |
| `data-size` trên circle | Không còn gì pin area vào value; sizing theo radius vẫn trông hoàn toàn hợp lý. |
| `data-name` trên circle | Bubble không tên không thể label/cross-check và lặng lẽ rơi khỏi mọi comparison. |
| `data-name` trên label | Hai label có thể bị đổi cho nhau, đổi tên cả hai bubble trong khi từng number vẫn đúng riêng lẻ. |
| `data-tick` / `data-value` trên tick | Toàn bộ printed axis có thể bị relabel — bubble đều trung thực trên một scale mà axis nói dối. |

`scripts/verify-bubble.py` suy ra cả hai axis scale và area constant từ chính tập data (Theil–Sen, leave-one-out, để một bubble gian dối không thể kéo đường mà chính nó được đo theo), yêu cầu tối đa một accent bubble, kiểm tra paint order trên overlap và giữ mọi bound label/tick khớp mark nó mô tả. Cố ý **không** dùng `data-series`: attribute đó thuộc contract slopegraph; dùng nó ở đây sẽ đưa mọi bubble file vào scope của `verify-slopegraph.py`.

**Không có `transform` trên bất kỳ phần nào trong số này.** Checker đọc trực tiếp attribute `cx`/`cy`/`r` và `x`/`y`, nên transform trên bubble, bound label, ancestor `<g>` hoặc CSS rule sẽ di chuyển mark được render khỏi number đã verify. Bake offset vào coordinate. Rotated value-axis caption thì được — nó không phải geometry được verify hay bound label.

#### Anti-pattern

- Radius tỉ lệ với value — lỗi không thể chấp nhận của type này.
- Dịch bubble để tránh overlap hoặc vẽ small bubble dưới large bubble.
- Một hue mỗi item thay vì ink ramp + một accent; hoặc legend diễn giải ramp như data.
- Log axis mà source line không nêu, hoặc truncated axis không ghi bounds.
- Label mọi bubble — chỉ focal + 2–3 outlier.
- `transform` trên bubble, bound label, ancestor group hoặc CSS.
- Visible string không bind: label hoặc axis tick không có attribute nêu cùng value.
- Dùng size cho một value chẳng ai cần đọc — nếu area không thay đổi câu chuyện, đây chỉ là parent scatter mặc costume.

### Beeswarm

**Phù hợp nhất cho:** một full distribution trong đó mỗi unit xứng đáng có mark riêng — một dot mỗi item trên một shared value axis, được dodge theo phương vuông góc để không overlap. Dùng khi *shape* của crowd và các outlier là câu chuyện mà summary number sẽ che mất: shipped example vẽ 138 per-request latency sample cho một endpoint; điểm của figure là median khoẻ và p99 xấu cùng thuộc một dataset.

Không dùng cho: hai biến (đó là parent scatter); so sánh distribution qua nhiều group (facet hoặc dùng ridgeline); hơn khoảng 300 item (packing vượt band — bin thành histogram); hoặc chỉ vài value (dưới 20 không có distribution đáng để swarm, table nói ngắn hơn).

#### Quy ước layout

- **Một value axis, horizontal, tại baseline của parent** (`y=420` trong `0 0 1000 500`, plot margin trái 80, phải 40), với 4–6 bound tick cách đều bằng Geist Mono 8px và **chỉ vertical gridline** — swarm axis không có scale để grid; một horizontal rule xuyên band sẽ khiến người đọc tưởng packing offset là value.
- **Số dot: 20–300**, một dot mỗi item, cùng một radius (shipped example dùng `r=4`). Cả hai đầu budget đều được `scripts/verify-beeswarm.py` enforce.
- **Greedy dodge quanh midline** (`y=230` trong shipped example): mỗi dot lấy free slot đầu tiên, xen kẽ trên/dưới theo fixed pitch `2r+2`. Dodge là packing, không phải data — bất kỳ arrangement collision-free nào cũng hợp lệ, algorithm không nằm trong contract.
- **Label: focal dot cộng các outlier người đọc sẽ tìm, tối đa 6.** Geist Mono 8px small-caps trên paper mask, mỗi label một tier, xen kẽ hai phía band; mỗi label nối với dot bằng leader hairline không bind và bind semantic bằng `data-name`.
- **4px grid** áp dụng cho designed constants — axis rule, gridline, tick baseline, legend row. Dot position được data-scale trên value axis và packing-scale trên swarm axis nên đều được miễn; snap chúng sẽ làm sai data.

#### Màu

- **Một ink fill cho mọi non-focal dot** (`ink` ở 0.55 trong shipped example) cộng stroke `muted` cho edge, và **tối đa một accent dot**. Density phải đọc qua *độ dày swarm*, không phải tone: opacity vừa encode value vừa dodge sẽ nói cùng một thứ hai lần theo hai cách sai khác nhau, nên `verify-beeswarm.py` yêu cầu non-focal fill phải giống hệt literal trên toàn swarm.
- **Accent đánh dấu item focal về mặt biên tập** — trong shipped example là request chậm nhất, cũng là item title đang nói tới — không bao giờ một hue cho mỗi group. Group là quyết định facet, không phải palette.
- **Focal dot giữ shared radius.** Cue của nó là accent fill/stroke, label và legend gọi tên bằng chữ; focal dot lớn hơn là encoding thứ hai và phá packing.

#### Quy tắc trung thực với data

**Value axis chính xác và shared; swarm axis không mang nghĩa — và phải nói rõ điều đó.** Legend hoặc source line nêu vertical spread chỉ là packing, nêu axis bounds và đếm mọi item bị bỏ. `scripts/verify-beeswarm.py` gate phần geometry.

- **Không dot nào bị drop, bin hoặc jitter khỏi true value.** Một dot = một item tại đúng value trên một linear scale duy nhất suy ra từ tập data (Theil–Sen, leave-one-out, để một dot gian dối không thể kéo scale nó được đo theo).
- **Overlap được giải bằng perpendicular dodge, không bao giờ bằng dịch dot dọc value axis.** Hai item cùng value chia sẻ position và dodge apart; crowding là data, rendering trung thực của crowd là thickness.
- **Không hai dot nào overprint.** Một dot vẽ đè lên dot khác biến density thành darkness, mắt người đọc sẽ hiểu như một value không ai khai báo.
- **Chỉ linear scale trong shipped grammar.** Log axis cần declaration riêng trước khi checker có thứ để enforce, nên hiện bị từ chối thay vì half-trusted; nếu spread buộc phải log, nói rõ trong source line và chấp nhận gate sẽ fail cho tới khi grammar có declaration.

#### Khai báo value

**Mọi dot bind vào value nó encode.** `data-value` trên `<circle>` là contract của beeswarm — cố ý không dùng `data-series` (slopegraph), `data-ranks` (bump) hay `data-size` (bubble), để checker sibling không claim beeswarm file và checker này không claim file của chúng. Detection theo element: `data-value` cũng xuất hiện trên `<text>` axis tick trong bubble contract, nên chỉ `<circle>` có binding này mới đưa file vào gate. Paper underlay dưới mỗi dot chỉ là scenery, không mang data.

```svg
<!-- A dot: position on the shared value scale, x = 80 + 2·ms. The cy is
     packing only. -->
<circle data-value="90" cx="260" cy="250" r="4" fill="rgba(45,49,66,0.55)" stroke="#4f5d75" stroke-width="0.75"/>

<!-- The focal dot — named, accented, same radius as everyone -->
<circle data-value="431" data-name="req-4c1f" cx="942" cy="230" r="4" fill="rgba(235,108,54,0.55)" stroke="#eb6c36" stroke-width="1.2"/>

<!-- Its label, bound to the dot it names -->
<text data-name="req-4c1f" data-role="label" x="942" y="120" fill="#2d3142" font-size="8" font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">REQ-4C1F</text>

<!-- An axis tick, bound to the number it prints -->
<text data-tick="x" data-value="200" x="480" y="440" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace" text-anchor="middle">200</text>
```

Mỗi binding đem lại gì, và mất gì nếu bỏ:

| Binding | Nếu thiếu |
|---|---|
| `data-value` trên circle | Không bắt được dot bị nudge dọc value axis — vị trí được vẽ sẽ là tuyên bố duy nhất về value. |
| `data-name` trên focal/outlier circle | Outlier không tên không thể label/cross-check, và hai label bị swap sẽ lặng lẽ đổi tên hai dot. Name phải non-empty và unique cho đúng một dot: hai dot cùng name collapse thành một entry, nên một label sẽ “thoả” cả hai. |
| `data-name` trên label | Label trôi tự do — có thể gọi tên dot không tồn tại hoặc drift sang neighbour. |
| `data-tick` / `data-value` trên tick | Printed axis có thể bị relabel toàn bộ — mọi dot trung thực trên một scale mà axis nói dối. |

`scripts/verify-beeswarm.py` suy ra value scale từ chính các dot, yêu cầu dot cùng value phải cùng position, từ chối mọi pair overprint, giữ mọi dot cùng một radius và mọi non-focal dot cùng một fill, cap accent ở một dot và label ở sáu, yêu cầu mọi `data-name` non-empty + unique, và check mọi bound label/tick với mark nó mô tả; `scripts/test-verify-beeswarm.py` chứng minh mỗi check ở cả hai polarity và pin scope treaty với sibling gate theo cả hai hướng.

**Không gì được position mark ngoài chính attribute của nó.** Checker đọc raw `cx`/`cy`/`r` và `x`/`y`, nên mọi thứ áp dụng sau đó làm invalid check đã pass. Tất cả carrier đều bị từ chối — attribute `transform`, inline `style="…"` và rule trong `<style>` block — trên dot, bound label/tick hoặc ancestor `<g>`/`<svg>`. Mọi positioning property cũng bị từ chối, không chỉ `transform`: Level 2 individual properties `translate`/`rotate`/`scale`, SVG geometry properties `cx`/`cy`/`r`/`x`/`y` (CSS thắng presentation attribute), và CSS motion path. Bake offset vào coordinate. `line-height`, `color` và font declaration không bị ảnh hưởng vì không di chuyển gì.

#### Anti-pattern

- Dịch dot dọc value axis để mở chỗ — lỗi không thể chấp nhận của type này.
- Bin hoặc average trước khi plot (đó là histogram mặc costume), hoặc lặng lẽ bỏ inconvenient outlier.
- Dot size làm encoding thứ hai (đó là **bubble variant**), hoặc opacity encode value trong khi cũng dodge.
- Nhét meaning vào swarm axis: sort dodge theo biến thứ hai hoặc vẽ midline như thể nó là scale.
- Một hue mỗi group thay vì một ink + một accent.
- Label nhiều hơn focal dot và một handful outlier.
- Position dot, bound label, tick hoặc ancestor group bằng CSS — `transform`, `translate`, `rotate`, `scale`, geometry property (`cx`/`cy`/`r`/`x`/`y`) hoặc motion path — dù qua attribute, inline `style` hay rule trong `<style>` block.
- Hai dot dùng cùng `data-name`, hoặc name rỗng: một name nhận diện hai mark thì không nhận diện mark nào.
- Visible string không bind: label hoặc axis tick không có attribute nói cùng thing.

## Ví dụ

- `assets/example-scatter.html` — minimal light
- `assets/example-scatter-dark.html` — minimal dark
- `assets/example-scatter-full.html` — full editorial
- `assets/example-bubble.html` — bubble, minimal light
- `assets/example-bubble-dark.html` — bubble, minimal dark
- `assets/example-bubble-full.html` — bubble, full editorial
- `assets/example-beeswarm.html` — beeswarm, minimal light
- `assets/example-beeswarm-dark.html` — beeswarm, minimal dark
- `assets/example-beeswarm-full.html` — beeswarm, full editorial
