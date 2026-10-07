# User Journey Map

**Phù hợp nhất cho:** một người làm gì xuyên suốt các stage của một experience và *cảm thấy* thế nào tại từng stage. Sentiment curve là load-bearing element — không có nó thì đây chỉ là process diagram với thêm row, vì vậy nếu không thể gọi tên sentiment cho từng stage, dùng **Process** hoặc **Timeline** thay thế.

## Quy ước layout

Vertical stack từ trên xuống, cho một persona:

- **Stage headers** — 5 column bằng nhau, rộng 200px, gutter 24px (tối đa 6 stage). Mỗi column: eyebrow Geist Mono 8px uppercase tracked (`STAGE 1` … `STAGE 5`) ở trên stage name Geist sans 12px weight 600, cả hai centered theo column.
- **Sentiment band — phần tạo khác biệt** — plot area cao 160px ngay dưới header. 3 horizontal reference hairline ở `rule` opacity 0.10 đánh dấu level `HIGH` / `NEUTRAL` / `LOW` — Geist Mono 8px `muted`, anchor `end` trong left margin 64px. **Không dùng emoji, không dùng `writing-mode` vertical text cho các label này.** Một smooth polyline `muted` 1.5px chạy qua một dot `r=5` mỗi stage, mỗi value snap vào một trong năm ordinal level (`HIGH`, `MED-HIGH`, `NEUTRAL`, `MED-LOW`, `LOW`) — chỉ ba level thực sự dùng mới cần labeled hairline. Dot của trough stage và incoming segment của nó dùng `accent`; mọi thứ khác trên curve dùng `muted`.
- **Content rows** — tối đa 3 labeled band dưới sentiment band, mỗi band có row label Geist Mono 8px uppercase nằm trong left margin — cùng column với sentiment level label, không rotate:
  - `ACTIONS` — user làm gì, Geist sans 12px, một short line mỗi stage.
  - `TOUCHPOINTS` — surface nơi action diễn ra, như email, app, docs…, Geist Mono 9px `muted`.
  - Optional third row cho metric hoặc owner, cùng treatment như touchpoint.
  Các row được phân cách bằng hairline span toàn plot width — từ left margin edge tới right edge của stage cuối.
- **Pain markers** — ở stage sentiment giảm, đặt tag box nhỏ dashed-stroke (`rx=2`, stroke `accent @ 0.50` dashed `3,3`, không fill hoặc accent tint rất nhẹ) dưới actions cell của stage đó, với label Geist Mono 8px gọi tên friction. Tối đa 2 mỗi diagram, và chỉ ở trough — tag mọi stage sẽ xoá signal.
- **Legend** — horizontal strip ở đáy theo global rule — hairline separator phía trên, entry cách nhau 160–180px — gồm ba key theo thứ tự: sentiment line, trough-stage highlight và pain-marker tag. Trough key không optional: dip chính là finding, nên reader cần biết highlight đó có nghĩa gì.

## Ghi chú connector

Sentiment polyline là **data curve**, không phải connector giữa node — §6 rule 1 về mandatory orthogonal elbow không áp dụng. Exemption **chỉ** cho sentiment curve; mọi connector khác trong journey map — thường không có — vẫn theo standard connector rule.

## Geometry

- Stage grid: left margin 64px, sau đó 5 column 200px với gutter 24px (`col_left = 64 + i·224`).
- Sentiment band cao 160px. Hairline tại top (`HIGH`), middle (`NEUTRAL`) và bottom (`LOW`), cách nhau 80px.
- Dot x = horizontal center của stage column. Dot y = hairline y của snapped level — hoặc interpolated position cho unlabeled level.
- Row height: đủ cho một line text cộng, riêng trong row `ACTIONS`, tối đa hai pain-marker box cao 16px stack lên nhau.

## Focal rule

Chính xác 2 accent element: trough dot + incoming curve segment của nó — tính là một — và pain marker của nó — tính là element còn lại. Không thứ gì khác trên map dùng `accent`.

## Complexity budget

Tối đa 6 stage · tối đa 3 content row · 5 sentiment level — ordinal, named, không numeric · tối đa 2 pain marker · tối đa 2 accent element.

## Anti-pattern

- **Không sentiment curve.** Nếu mọi stage đều cùng cảm giác hoặc bạn không thể đặt tên cảm xúc, bạn đang vẽ process — dùng **Process** hoặc **Timeline**.
- **Hơn 6 stage.** Split thành hai journey, ví dụ acquisition và retention, thay vì nhồi một funnel quá rộng vào một map.
- **Numeric sentiment axis** — score 0–100. Sentiment ở đây là ordinal — năm named level, không phải continuous metric chart.
- **Emoji làm sentiment marker.** Dùng named level và hairline; emoji không localize, không print tốt, không giữ được khi size nhỏ.
- **Nhiều persona trên cùng map.** Overlay hai sentiment curve xoá cả hai. Một map mỗi persona.
- **Pain marker trên mọi stage.** Nếu không còn stage un-marked thì không còn focal.
- **`writing-mode` vertical row label.** Chỉ horizontal, trong left margin — cùng rule như mọi type khác trong skill.
- **Dùng cho internal system flow không có con người.** Không person, không sentiment, không journey map — đó là architecture hoặc data-flow diagram.

## Ví dụ

- `assets/example-journey.html` — minimal light. *Trial to paid: the first week*, 5 stage, trough tại “Hit the limit”.
- `assets/example-journey-dark.html` — minimal dark, cùng data.
- `assets/example-journey-full.html` — full editorial: container framing + 3 summary card khác width + footer.
