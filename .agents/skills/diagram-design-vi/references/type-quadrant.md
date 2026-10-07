# Quadrant

**Phù hợp nhất cho:** prioritization (Impact × Effort), positioning (Reach × Frequency), portfolio map, khung quyết định 2×2.

## Quy ước layout
- Grid 2×2. Axis line: ink 1px cắt nhau ở center.
- **Axis label: Jobs-minimal.** Mỗi arrow tip chỉ có một từ — không nhúng glyph vào label, không `↑` / `→` / `←` / `↓`, không parenthetical, không modifier "HIGH / LOW". Geist Mono 9px regular, tracked 0.18em, uppercase. Label nằm flanking arrow tip — không bao giờ đè lên axis line. Rút ngắn arrow khoảng 60–80px tính từ viewBox edge để chừa breathing room cho label nằm phía ngoài tip.
- Không bao giờ label tại midpoint.
- Item: dot nhỏ có label (`r=4`) đặt trong quadrant. Label cách 8–10px; không để label cắt axis line.
- Coral dành cho item "do first", thường top-right.
- Giới hạn khoảng 12 item; nhiều hơn thì cluster hoặc split.

## Anti-pattern
- Bốn quadrant fill bốn màu khác nhau — position + label đã làm việc; color noise làm yếu signal.
- Item nằm đúng trên axis line — quadrant mơ hồ.
- Thiếu tên axis.

## Ví dụ
- `assets/example-quadrant.html` — minimal light
- `assets/example-quadrant-dark.html` — minimal dark
- `assets/example-quadrant-full.html` — full editorial
- `assets/example-quadrant-consultant.html` — consultant special, xem bên dưới

---

## Consultant special (ma trận scenario 2×2)

Một **layout variant** của quadrant chuẩn — vẫn dùng cùng house skin: warm paper, dot pattern, Instrument Serif title, Geist mono eyebrow và coral focal rule. Grammar thay đổi: axis giữ một **range** thay vì measurement; cell giữ **named scenario** thay vì positioned item.

**Dùng khi:** cần frame bốn future, archetype hoặc strategic option trên hai independent driver — classic scenario planning, positioning frame hoặc strategy deck 2×2 kiểu BCG/McKinsey. Reader phải rời figure với bốn named bet, không phải point cloud.

**Không dùng** cho prioritization, density map hoặc bất cứ trường hợp nào mà *position bên trong* cell mang nghĩa — trường hợp đó dùng quadrant chuẩn ở trên.

### Điều gì tạo nên consultant variant

| Move | Standard quadrant | Consultant special |
|---|---|---|
| Axis arrows | single-ended | **double-ended** — cả hai axis có `marker-start` + `marker-end` |
| Cell content | dot nhỏ có label | **named scenario + description 1–3 line** |
| Quadrant corner | short tag, ví dụ DO FIRST | **numbered tag + axis combination** (`01 · DIMENSION-A / DIMENSION-B`) |
| Focal accent | coral trên một *item* | coral trên một *quadrant* — tinted bg + coral stroke + coral corner tag |
| Axes | muted ink 1px | **ink 1.2px** — nặng hơn nhẹ vì axis gánh nhiều meaning hơn |

Cả hai variant dùng cùng Jobs-minimal axis label: một từ mỗi arrow tip, không glyph, không parenthetical. Khác biệt axis duy nhất là consultant variant dùng double-ended arrow thay single-ended.

Mọi thứ khác — paper, dot pattern, typography, legend strip, 4px grid, complexity budget — giữ house default. Không invent color hoặc font mới cho variant này.

### Style token — in-house

- **Paper / bg / pattern:** default từ `style-guide.md` — `paper`, dot pattern 22×22 ở 10% ink.
- **Axis line:** `ink` (`#2d3142`), `stroke-width: 1.2`, `marker-start` + `marker-end` cùng hướng ra ngoài.
- **Focal quadrant tint:** `rgba(235,108,54,0.04)` là full rect phía sau focal cell.
- **Focal cell:** fill `accent-tint`, stroke `accent` 1.2px. Corner tag dùng `accent`, weight 600.
- **Non-focal cell:** treatment `store` — `ink @ 0.04` fill, `muted @ 0.28` stroke.
- **Cell title:** Geist sans 16px, weight 600, `ink`.
- **Cell description:** Geist sans 11px, `muted`, 1–3 line, left-aligned trong cell.
- **Corner tag:** Geist Mono 8px, uppercase, tracked `0.18em`, `muted` — hoặc `accent` trên focal. Format `NN · DIMENSION-A / DIMENSION-B`; hai từ dimension phải khớp axis label chính xác.
- **Axis label:** Geist Mono 9px **regular weight**, tracked `0.18em`, uppercase, `ink`. **Một từ mỗi tip.** Không arrow glyph trong label, không `HIGH / LOW` parenthetical, không multi-line sublabel. Bản thân từ đó *là* label. Đặt label *beyond* arrow tip, không đặt trên axis line:
  - Top tip: `text-anchor="middle"`, khoảng 12px phía trên arrow tip
  - Bottom tip: `text-anchor="middle"`, khoảng 20px phía dưới arrow tip
  - Left tip: `text-anchor="end"`, khoảng 12px bên trái arrow tip, `dominant-baseline="middle"`
  - Right tip: `text-anchor="start"`, khoảng 12px bên phải arrow tip, `dominant-baseline="middle"`

### Quy ước layout

- Bốn cell bằng nhau — 240×160 hoặc 280×180 là default tốt — sắp quanh axis cross với gap 40–60px.
- Axis cross đi *giữa* cell, không xuyên qua chúng.
- Arrow tip nằm khoảng 20–40px ngoài outer cell edge; single-word axis label nằm khoảng 12px ngoài mỗi tip.
- Chính xác một focal cell. Không chọn cell nào biến output thành placeholder template; chọn hai cell xoá signal.
- Giữ legend strip + horizontal rule ở đáy như quadrant chuẩn. Legend swatch phải thể hiện cả "headline bet" — coral — và "candidate future" — neutral.

### Anti-pattern riêng của variant

- Plain white background — warm paper + dot pattern là load-bearing trên toàn skill; bỏ chúng để “trông consultant” làm diagram generic.
- Sans-serif H1 — page title vẫn dùng Instrument Serif. Tương phản title/diagram là house signature.
- Cell không có tên — "Scenario 1/2/3/4" — chỉ chấp nhận trong blank template, không trong finished artifact.
- Coral trên nhiều hơn một cell — cùng focal rule như toàn skill.
- Grid 3×3 hoặc 2×3 — đó là diagram khác, không phải variant này.
- Position dot *bên trong* cell — nếu position có meaning, dùng standard quadrant.
- Bold axis label, arrow glyph trong text như `↑ DRIVER`, hoặc parenthetical "HIGH / LOW" — đều cấm. Jobs-minimal là non-negotiable.
- Corner tag không khớp axis label, ví dụ axis nói `REMOTE / IN-PERSON` nhưng tag lại nói `HIGH REMOTE / LOW AI`. Reader nhìn ra bug này trong ba giây.
