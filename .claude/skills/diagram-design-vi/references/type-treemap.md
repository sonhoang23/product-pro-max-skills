# Treemap

**Phù hợp nhất cho:** part-of-whole nơi *relative size là câu chuyện* — disk/bundle usage, budget/spend breakdown, market share, population, time allocation. Dùng khi một total được chia thành part và câu hỏi là “cái gì chiếm ưu thế, và bao nhiêu?”.

Không dùng cho ranked list cần exact value hơn proportion (dùng **bar chart**), containment/scope không có quantity (dùng **nested**), hoặc hierarchy cần trace parent-child (dùng **tree**).

## Quy ước layout

- **Plot area:** `x` 40 → 956, `y` 40 → 420 trong `0 0 1000 500` viewBox — cùng vertical rhythm với bar/line/scatter; legend rule tại `y=462`, `LEGEND` tại `478`, key tại `488`.
- **Squarified layout** (Bruls et al., 2000): sort descending, đặt từng row theo *shorter side* của remaining rectangle. Aspect ratio gần 1 để area dễ so bằng mắt. Không layout theo stripe đơn giản.
- **Cell count:** 4–8. Trên 8, tail thành sliver khó label — group tail thành cell `Other` rõ ràng và nêu contents trong source line.
- **4px grid:** edge snap grid, gutter 4px. Snapping/gutter làm đổi area nên phải check bằng **relative error** `(drawn − true) ÷ true`, không percentage point. Giữ mỗi cell trong vài phần trăm true share; shipped example worst-case 2.7%. Ghi encoding trong source line (`AREA = POPULATION`). `scripts/verify-treemap.py` gate điều này.
- **Fill:** rank-ordered `ink` opacity ramp (ví dụ `0.16 → 0.04`) để non-focal order sống được khi grayscale/color-blind. Chỉ một accent cell — focal về editorial, không mặc định là largest. Focal cell nằm ngoài ramp nên trong grayscale không còn thể hiện rank bằng tone; nhận diện bằng accent stroke và không để tone mang meaning mà area chưa mang. `ink` là role, không phải color: near-black trên light paper, near-white trên dark; opacity giống nhau ở cả hai skin, chỉ lightness đảo.
- **Stroke:** hairline 1px `ink @ 0.30`; focal cell stroke `accent` 1.5px.
- **Label nằm trong cell**, top-left inset 16px: name Geist 12–14px 600, value Geist Mono 9px dòng sau. Ba tier theo cell size:
  - large — name + value + share (`4.78B · 59% of world`)
  - medium — name + value
  - small — abbreviation mono 3 ký tự nếu trung thực
  - sliver — **không text.** Nếu cell ít nhất 12×12px, dùng filled `ink` disc `r=5` ở center có `i` màu paper, và spell out name/share trong legend. Dưới 12px ở bất kỳ axis nào, bỏ in-cell mark và identify qua legend position; fixed-size disc không được vượt cell boundary. `scripts/verify-treemap.py` check containment. Không rotate label để ép vừa.
  - Không shrink cell để fit label. Cell size là data; label là commentary.
- **Contrast:** check token thực tế ship. Value line 9px là `muted`, không `ink`; `muted` yêu cầu cell nhẹ hơn: ramp tối đa **0.16 light, 0.14 dark** trước khi xuống dưới 4.5:1. Mid-tone solid accent hay 50% `ink` fail với cả light/dark text; dùng tint-plus-stroke. Source line cũng dùng `muted`: `soft` chỉ 3.48:1 trên paper.
- **Legend:** house block, nêu focal cell, direction của `ink` ramp và cell có info mark. **Tên direction bằng contrast với paper — `stronger contrast is larger` — không bằng lightness.** `darker is larger` sai ở dark variant. `scripts/verify-skin-polarity.py` gate điều này. Source line cùng row với `LEGEND`, right-aligned mono 8px, nêu area encoding + dataset/date.

### Khai báo share

**Mọi cell đều mang `data-share` — kể cả cell quá nhỏ không label.** Đây là percentage của whole và là căn cứ verify area:

```svg
<rect x="X" y="Y" width="W" height="H" rx="2" data-share="18.29" fill="…" stroke="…"/>
```

Không có nó, verifier phải infer intended share từ text, vô tình bỏ qua sliver cell — nơi grid distortion lớn nhất. `scripts/verify-treemap.py` fail closed nếu cell thiếu `data-share`, đồng thời cross-check với percentage label.

### Cell element pattern

```svg
<!-- Opaque paper mask prevents the dot pattern showing through the tint -->
<rect x="X" y="Y" width="W" height="H" rx="2" fill="#f5f5f5"/>
<!-- Cell body -->
<rect x="X" y="Y" width="W" height="H" rx="2" data-share="18.29" fill="rgba(45,49,66,0.16)" stroke="rgba(45,49,66,0.30)" stroke-width="1"/>
<text x="X+16" y="Y+28" fill="#2d3142" font-size="13" font-weight="600" font-family="'Geist', sans-serif">NAME</text>
<text x="X+16" y="Y+46" fill="#4f5d75" font-size="9" font-family="'Geist Mono', monospace">VALUE · SHARE</text>
```

Focal cell: fill `rgba(235,108,54,0.16)`, stroke `#eb6c36` 1.5px.

## Honest-data rule

**Area là encoding duy nhất.** Không clip, floor hoặc log-scale cell để dễ nhìn; không drop cell vì nhỏ — treemap tuyên bố thể hiện whole nên bỏ part là sai. Part quá nhỏ cho label nhận legend entry và chỉ có info mark khi cell chứa được; part quá nhỏ để draw được merge thành `Other` có tên trung thực. Nếu nhiều cell vô hình ở target size, data muốn bar chart.

Kiểm tra cell nhỏ nhất kỹ nhất: grid snapping/gutter distort nó nhiều nhất. Đồng thời kiểm tra rounding hiển thị: các value rounded có thể không sum total. Hoặc giữ precision đủ reconcile, hoặc ghi `PARTS ROUNDED, MAY NOT SUM` trong source line.

Legend eyebrow literal là `LEGEND`; centered labels dùng `text-anchor="middle"`.

## Anti-pattern

- Hơn 8 cell mà không `Other` bucket.
- Stated total mâu thuẫn cell vượt display rounding hoặc rounding không disclose.
- Stripe layout thay squarified.
- Rainbow fill.
- Nest hơn hai level trong static diagram.
- 3-D hoặc shadowed cell.

## Ví dụ

- `assets/example-treemap.html` — minimal light
- `assets/example-treemap-dark.html` — minimal dark
- `assets/example-treemap-full.html` — full editorial
