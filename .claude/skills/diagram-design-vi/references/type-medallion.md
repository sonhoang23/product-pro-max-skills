# Medallion

**Phù hợp nhất cho:** tài liệu hóa một bố cục lưu trữ dữ liệu nhiều tầng, trong đó mỗi tier là một *mức chất lượng / quyền truy cập* riêng của cùng dataset — thường là raw landing zone, anonymised, staging/cleaned, aggregated business indicators và cold archive. Dùng khi người đọc cần thấy ngay *mỗi bucket chứa gì*, *ai ghi vào đó*, *bằng tool và format nào*, và *dữ liệu được promote giữa các tier ra sao*.

Ưu tiên **Process** nếu chủ đề là workflow có role lane. Ưu tiên **High-Level** nếu chủ đề là cluster architecture thay vì cách tổ chức storage tier.

Type này **parametric** — input schema ở §1 điều khiển mọi coordinate qua formula §2. Hai lần generation từ cùng input phải tạo SVG giống nhau về mặt hình học. Rule shape mirror `type-process.md` và `type-data-flow.md`, vì vậy color override, `focal` rule và reproducibility checklist đọc giống nhau giữa các type.

---

## 1. Inputs — parameter contract

```yaml
title:    "Five-Tier Medallion Architecture"
subtitle: "Quarterly survey through Raw → Anonymized → Staging → Aggregated → Archive"

tiers:                                # 3..6 tier columns, ordered left → right
  - { name: "Raw",        bucket: "raw-bucket",        style: "outer",
      fields: { tool: "NiFi · raw write",          format: "CSV · Parquet · JSON", writer: "Data Engineer",
                example: ["Q1 dump · w/ PII", "verbatim CAPI export"] } }
  - { name: "Anonymized", bucket: "anon-bucket",       style: "default",
      fields: { tool: "Trino INSERT",              format: "Iceberg · partitioned", writer: "Data Engineer",
                example: ["no name · address", "stable household ID"] } }
  - { name: "Staging",    bucket: "staging-bucket",    style: "default",  color: "#c9a23a",   # warm yellow — analytical working zone
      fields: { tool: "Trino · JupyterHub",        format: "Iceberg · cleaned",     writer: "Data Scientist",
                example: ["weighted records", "harmonised codings"] } }
  - { name: "Aggregated", bucket: "aggregated-bucket", style: "focal",  focal: true,
      fields: { tool: "Trino INSERT · SAS JDBC",   format: "Iceberg · indicators",  writer: "Data Scientist",
                example: ["unemployment rate", "labour participation"] } }
  - { name: "Archive",    bucket: "archive-bucket",    style: "cold",
      fields: { tool: "MinIO lifecycle",           format: "cold tier · immutable", writer: "Data Administrator",
                example: ["historical Q1–Q4 sets", "5+ years retained"] } }

example_label: "Quarterly survey example" # bottom field label (varies per domain)

promotions:                           # adjacent-tier arrows; len = n_tiers - 1
  - { from: 0, to: 1, label: "PII REMOVE",    style: "normal"    }
  - { from: 1, to: 2, label: "CLEAN+WEIGHT",  style: "normal"    }
  - { from: 2, to: 3, label: "AGGREGATE",     style: "focal"     }    # auto-accent because target is focal
  - { from: 3, to: 4, label: "LIFECYCLE",     style: "lifecycle" }    # dashed

paths:                                # 0..2 write-method cards at the bottom (optional)
  - { tag: "SQL PATH",      title: "Trino INSERT INTO … SELECT",
      sub: "filter · reshape · join · aggregate — set-based transforms" }
  - { tag: "NOTEBOOK PATH", title: "DuckDB + Python/R in JupyterHub",
      sub: "stats · ML · interactive analysis — row-iterative work" }

dark: false
```

**Semantic dành riêng cho field:**
- `tiers[i].style` — một trong `outer`, `default`, `focal`, `cold`. Điều khiển fill/stroke palette của card (§2.4).
- `tiers[i].focal: true` — chính xác **một** tier được phép khai báo. Override `style` thành `focal` và tự động chuyển promotion arrow *đi vào* tier này thành `focal`.
- `tiers[i].fields` — `{tool, format, writer, example}`. `example` là list 1 hoặc 2 item; section heading dùng `example_label`.
- `tiers[i].color` — optional `"#hex"` per-tier color override. Xem §4.
- `promotions[].style` — `normal` | `focal` | `lifecycle`. Connector rule (§3) bind mỗi style với stroke / dash / marker cố định.
- `paths` — 0–2 entry. Khi có 0 entry, bottom row bị bỏ và `viewBox_h` shrink tương ứng.

---

## 2. Layout formulas — deterministic geometry

```
# Tier dimensions
tier_w           = 172
tier_h           = 380
tier_gap         = 16
left_pad         = 16
right_pad        = 100
n_tiers          = len(tiers)

# Canvas
viewBox_w        = left_pad + n_tiers * tier_w + (n_tiers - 1) * tier_gap + right_pad
                                                    # 5 tiers → 16 + 860 + 64 + 100 = 1040
arc_band_h       = 80                               # space above tiers reserved for promotion arcs
path_h           = 56
path_gap         = 16                               # gap between tier row and path row
bottom_pad       = 16
viewBox_h        = arc_band_h + tier_h + (path_gap + path_h if paths else 0) + bottom_pad
                                                    # with paths → 80+380+72+16 = 548
                                                    # without paths → 80+380+16 = 476

# Tier positions
tier_x(i)        = left_pad + i * (tier_w + tier_gap)    # 16, 204, 392, 580, 768
tier_y           = arc_band_h                            # 80 — tier tops sit just below the arc band
tier_cx(i)       = tier_x(i) + tier_w/2                  # 102, 290, 478, 666, 854

# Promotion arcs (between adjacent tiers — over the top, anchored at tier top-centers)
arc_src_x(i)     = tier_cx(i)                            # top-center of tier i      (102, 290, 478, 666)
arc_dst_x(i)     = tier_cx(i+1)                          # top-center of tier i+1    (290, 478, 666, 854)
arc_peak_x(i)    = (arc_src_x(i) + arc_dst_x(i)) / 2     # midpoint                  (196, 384, 572, 760)
arc_label_y      = 50                                    # label sits inside the arc, 30px below tier top

# Path row (bottom)
path_y           = tier_y + tier_h + path_gap            # 476
path_w           = (viewBox_w - 2*left_pad - path_gap) / 2 if len(paths) == 2 else (viewBox_w - 2*left_pad)
                                                          # Canonical 5-tier shape uses path_w=460 explicitly (see §2.5)
```

### 2.1 Background

Solid paper fill trên toàn `viewBox`. Không dot pattern.

### 2.2 Tier card (`172 × 380`)

Mỗi tier render thành rounded-rect card có tinted header band, bucket name căn giữa, bốn labeled field row và section `example_label` tách riêng gần đáy.

```
tier_x(i),  tier_y       =  card top-left  (tier_y = 80, just below the arc band)
header_band_h            = 40            # band from y=tier_y to y=tier_y+40 (i.e., 80..120)
header_band_extra        = 10            # 10-px extension below band, same tint

# Inside the card (absolute y; tier_y = 80):
title_text            at (tier_cx(i), 106)                # node-name role, 13px, weight 700, ink
bucket_text           at (tier_cx(i), 144)                # sublabel role, muted (accent on focal tier)

field_x               = tier_x(i) + 16                    # 16-px left inset for field text
field_w               = 140                               # 172-px tier_w minus two 16-px insets
field rows (absolute y):
  tool_label  at 180,    tool_value  at 186 (foreignObject, height 24)
  format_label at 220,   format_value at 226 (foreignObject, height 24)
  writer_label at 260,   writer_value at 266 (foreignObject, height 24)
  # gap (open whitespace below writer row, above the example section)
  example_label_text at 360,  example_line_0 at 374,  example_line_1 at 388
```

**Quy tắc wrap field value:** field value `tool` / `format` / `writer` render trong SVG `<foreignObject>` chứa HTML `<div>` để tự wrap khi text vượt 140px. Mỗi `foreignObject` rộng 140 × cao 24, vừa 2 dòng ở role `sublabel` với line-height 1.25. Khoảng 26px tới label của field kế tiếp hấp thụ dòng thứ hai sạch sẽ.

```svg
<foreignObject x="{field_x}" y="{value_top}" width="140" height="24">
  <div xmlns="http://www.w3.org/1999/xhtml"
       style="font-family: {sublabel}; color: {muted}; line-height: 1.25;">
    {field_value}
  </div>
</foreignObject>
```

HTML namespace declaration trên `<div>` là bắt buộc để SVG render inline content. Browser và Playwright/Chromium render chính xác; nếu export target không hỗ trợ `<foreignObject>` — một số build Inkscape cũ — hãy hand-split value dài thành hai `<tspan>` line.

Field label dùng role `node-name` 11px màu ink. Field value dùng `sublabel` màu muted. Bucket và field value có thể được retint bởi `color` override (§4).

Tier row giữ `tier_y = 80`; focal top-center canonical là `(tier_cx(1), 80)` khi tier index tương ứng được chọn.

### 2.3 Tier styles

Bốn canonical style được chọn qua `tiers[i].style`. Mapping mặc định nếu bỏ `style`: tier 0 → `outer`, tier cuối → `cold`, focal tier nếu có → `focal`, phần còn lại → `default`.

| `style` | Card fill | Card stroke | Header band fill | Bucket text | Example value text |
|---|---|---|---|---|---|
| `outer` | `#FFFFFF` | `muted` 1.0 solid | `muted @ 0.10` | `muted` | `muted` |
| `default` | `#FFFFFF` | `ink` 1.0 solid | `ink @ 0.06` | `muted` | `muted` |
| `focal` | `accent @ 0.07` | `accent` 1.6 solid | `accent @ 0.14` | `accent` | `accent` |
| `cold` | `paper-2` | `muted` 1.0 dashed `5,3` | `muted @ 0.18` | `muted` | `muted` |

`rx = 6` trên mọi card rect.

**Lưu ý focal styling:** accent treatment của focal tier lan sang bucket text và example-value line. Các field value khác — tool/format/writer — vẫn muted; chỉ bucket name và example payload mang focal signal để card không chìm hoàn toàn trong coral.

### 2.4 Promotion arcs — phía trên tiers

Mỗi promotion là một **cubic Bézier arc** anchor tại **top-center** của hai tier kề nhau — `(tier_cx(i), tier_y)` tới `(tier_cx(i+1), tier_y)`. Arc đi lên `arc_band` 80px phía trên card và peak khoảng y ≈ 20. Connector cùng label đều visible đầy đủ — không paper mask, không overlap card content.

```svg
<path d="M {tier_cx(i)},{tier_y} C {tier_cx(i)},0 {tier_cx(i+1)},0 {tier_cx(i+1)},{tier_y}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>
```

Cụ thể cho canonical 5-tier shape (`tier_y=80`, center x=102, 290, 478, 666, 854):

- 0→1: `M 102,80 C 102,0 290,0 290,80`
- 1→2: `M 290,80 C 290,0 478,0 478,80`
- 2→3: `M 478,80 C 478,0 666,0 666,80` — focal, accent
- 3→4: `M 666,80 C 666,0 854,0 854,80` — lifecycle, dashed

Hình học cubic: anchor y=80, control y=0. Peak tại t=0.5 có y ≈ 20, tính từ `0.125·80 + 0.375·0 + 0.375·0 + 0.125·80 = 20`. Mỗi arc span một tier-stride đầy đủ — 188px canonical — để connector có vertical excursion đủ rõ.

**Marker orientation:** `marker-end` với `orient="auto"` xoay arrow theo path tangent tại endpoint. Control point nằm thẳng phía trên anchor nên tangent khi hạ xuống là thẳng **xuống** — arrowhead vào top-center của tier *i+1* sạch, hướng vào header band.

**Chained anchors:** các arc liên tiếp dùng chung meeting point — arc 0→1 kết thúc tại `(tier_cx(1),80)`, chính là nơi arc 1→2 bắt đầu. Top-center của mỗi tier đọc như “joint”: data tới card, transform bên trong rồi rời top sang tier kế. Arrowhead hạ xuống cộng arc kế tiếp đi thẳng lên đọc như một payload-handoff motion liên tục.

| `style` | Stroke | Width | Dash | Marker |
|---|---|---|---|---|
| `normal` | `muted` | 1.4 | — | `arrow` |
| `focal` | `accent` | 1.6 | — | `arrow-accent` |
| `lifecycle` | `muted` | 1.4 | `4,3` | `arrow` |

**Auto-style rules:**

- Nếu `promotions[k].to` trỏ tới **focal tier**, style tự promote thành `focal`.
- Nếu target tier có **`color` override** (§4), arrow inherit hex đó — stroke=`C`, label fill=`C`, marker-end dùng color-matched marker như `arrow-yellow` cho `#c9a23a`. Width vẫn 1.4 vì đây là concern signal, không phải focal promotion. Lifecycle/dashed arrow giữ dash nhưng nhận màu.
- Focal thắng nếu cả hai cùng áp dụng.

**Label bên trong arc:**

- Anchor ở `(arc_peak_x(k), arc_label_y)` = `((arc_src_x + arc_dst_x)/2, 50)`.
- Role `arrow-label` 10px, `letter-spacing=0.08em`, uppercase. Color match arrow stroke.
- **Không cần mask rect** — curve peak y≈20, label y=50, nằm thấp hơn curve trong open space được arc bao quanh.

Nếu inter-tier gap bị override ngắn hơn default 16px, `arc_inset` có thể phải giảm tương ứng để arc vẫn visible.

Promotion label dùng role `arrow-label`; focal marker là `arrow-accent`. Auto-style đọc target qua `promotions[k].to`, và label anchor canonical là `((arc_src_x + arc_dst_x) / 2, 50)`. Khoảng ngang giữa tier là `tier_gap`, còn vùng arc phía trên là `arc_band_h = 80`.

### 2.5 Path row — đáy, optional

Tối đa **2** write-method card. Canonical 5-tier:

```
path_y      = 476       # tier_y + tier_h + path_gap = 80 + 380 + 16
path_h      = 56
path_x[0]   = 16
path_w[0]   = 460
path_x[1]   = 16 + 460 + 16 = 492
path_w[1]   = 460
```

Hai path rộng 460 dù viewBox 1040 — right pad được lấy từ tier strip, không từ path strip. Giữ `path_w=460` cho canonical shape. Với tier count khác, derive `path_w = (viewBox_w - 2*left_pad - path_gap)/2`.

Mỗi card:

- Container rect: white fill, `ink @ 0.20` stroke width 1, `rx=6`.
- Tag chip: `(path_x+8, path_y+6)`, `h=12 rx=2`, fill transparent, stroke `ink @ 0.30` width 0.8; text `eyebrow` centered, `letter-spacing=0.08em`.
- Title tại `(path_x+80, path_y+30)`: `node-name` 11px ink.
- Sub tại `(path_x+80, path_y+46)`: `sublabel` muted.

---

Path row dùng `path_w = (viewBox_w - 2*left_pad - path_gap) / 2` khi có hai path. Tag/title/sub anchor lần lượt dùng `(path_x + 8, path_y + 6)`, `(path_x + 80, path_y + 30)` và `(path_x + 80, path_y + 46)`.

## 3. Connector rules — bắt buộc

Ba style bind với topology, mirror `type-process.md` §3:

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{muted}"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{accent}"/></marker>
  <!-- Per-color markers: declare one per custom tier color in use. -->
  <marker id="arrow-yellow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#c9a23a"/></marker>
</defs>
```

Thêm `<marker>` cho mỗi `color` override được dùng. Naming: `arrow-{semantic}` như `arrow-yellow`, `arrow-slate`, `arrow-red`.

**Z-order:** promotion arc được vẽ **trước** mọi tier card rect để card nằm trên và mask arc overshoot bên trong card.

**Arc shape rule:** Medallion promotion luôn là **cubic arc phía trên** tier strip, anchor top-center của source/target, control point thẳng phía trên ở y=0. Không dùng horizontal line xuyên qua gap — arc-over-top là thứ làm connector + label visible rõ.

---

## 4. Component color override

Mọi tier hoặc path entry có thể có `color: "#hex"`. Mirror `type-process.md` §4 / `type-data-flow.md` §4.

### 4.1 Per-tier `color`

| Element | Light | Dark |
|---|---|---|
| Card fill | `rgba(C, 0.07)` | `rgba(C_light, 0.10)` |
| Card stroke | `C` width 1.4 | `C_light` width 1.4 |
| Header band fill | `rgba(C, 0.14)` | `rgba(C_light, 0.18)` |
| Title text | ink — không đổi | ink — không đổi |
| Bucket text | `C` | `C_light` |
| Example values | `C` | `C_light` |
| Field labels / values | **không đổi** — ink / muted | **không đổi** |
| Connectors touching this tier | **không đổi** — topology-driven | **không đổi** |

`C_light` = cùng hex nhưng sáng hơn khoảng 15% cho dark-mode contrast.

### 4.2 Per-path `color`

Path card stroke thành `rgba(C,0.45)`, tag chip stroke `rgba(C,0.55)`. Tag text và title dùng `C`; sub vẫn muted.

### 4.3 Rules

- **Không bao giờ áp lên focal tier.** Accent đã mang signal đó; `color` trên focal bị ignore.
- **Không dùng trên `cold` tier cùng dashed treatment.** Chọn dashed-cold hoặc custom color, không cả hai.
- **Tối đa 2 custom-colored element** ngoài focal tier.
- **Promotion arrow inherit màu target tier** theo auto-style §3. Ví dụ `color: "#c9a23a"` trên Staging khiến CLEAN+WEIGHT arc đi vào Staging cũng vàng — connector, label, arrowhead match. Arrow không inherit màu source; arc đi *ra* colored tier quay lại muted hoặc nhận màu/style của target kế tiếp.

### 4.4 Semantic palette khuyến nghị

- `#b85450` rust-red — Security / Identity / Governance
- `#5a7d9a` slate-blue — Observability / Quality
- `#7a8c47` olive-green — Data Products / Publication
- `#c9a23a` warm yellow / gold — Analytical / Working zones
- `#8c6d3f` warm-brown — Backup / DR / Archive

---

Per-tier color stroke dùng `rgba(C, 0.45)` ở light và `rgba(C, 0.55)` ở dark.

## 5. Focal rule

Chính xác **một** focal tier mỗi diagram. Mặc định tier marked `focal: true`; nếu không mark thì analytical pivot — thường `Aggregated` hoặc tier downstream consumer query.

Focal tier:

- dùng `style: focal` — accent fill + stroke 1.6 + accent header band;
- bucket text + example value dùng accent;
- **incoming** promotion tự `style: focal`;
- **outgoing** promotion nếu có giữ user-declared style, thường `lifecycle` dashed.

Nếu có 0 hoặc >1 tier mang `focal: true`, dừng và hỏi user.

---

## 6. Dark mode

| Token | Light | Dark |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Accent | `accent` | `accent` |
| Fog — cold tier fill | `paper-2` | `paper @ 0.06` |
| White — default card fill | `#FFFFFF` | `paper @ 0.04` |
| Card stroke ink | `ink` | `paper @ 0.30` |
| Header band ink-tint | `ink @ 0.06` | `paper @ 0.08` |
| Header band muted-tint | `muted @ 0.10` | `soft @ 0.16` |
| Header band cold-tint | `muted @ 0.18` | `soft @ 0.24` |
| Header band accent-tint | `accent @ 0.14` | `accent @ 0.20` |
| Custom component colors | `C` | `C_light` — +15% |

---

## 7. Reproducibility checklist — taste gate

Trước khi emit SVG, verify **mọi** item:

1. `viewBox="0 0 {viewBox_w} {viewBox_h}"` derive §2 — 5 tier + 2 path → 1040×548.
2. Mỗi tier card tại `(tier_x(i),80)`, size `172×380`, `rx=6`.
3. Header band `(tier_x(i),80,172,40)` cộng 10px extension.
4. Chính xác **một** focal tier; incoming arc auto focal.
5. Promotion arc là cubic Bézier phía trên adjacent tier; anchor `(tier_cx(i),80)` → `(tier_cx(i+1),80)`, control y=0. Label `(arc_peak_x,50)`, no mask.
6. Bottom path row chỉ present khi `len(paths)>0`; card `y=476`, h=56.
7. Custom color ≤2 ngoài focal tier. Không tự recolor arrow ngoài target-inheritance rule.
8. Mọi promotion arrow + label được emit **trước** tier rect.
9. Bucket + example của focal dùng accent; phần còn lại muted theo rule.
10. `rx=6` mọi tier/path card; `rx=2` tag chip.

---

Reproducibility contract dùng `viewBox = "0 0 {viewBox_w} {viewBox_h}"`; tier top-left là `(tier_x(i), 80)`, card rect `(tier_x(i), 80, 172, 40)` cho header band, promotion nối `(tier_cx(i), 80)` tới `(tier_cx(i+1), 80)` với peak `(arc_peak_x, 50)`. Path row chỉ render khi `len(paths) > 0`.

## 8. Anti-patterns

- **Hơn một focal tier** — làm mất signal của analytical surface trung tâm.
- **Cold styling trên non-archive tier** — dashed fog dành cho retention/archive.
- **Bidirectional promotion arrow** — promotion luôn trái→phải; backflow cần diagram khác.
- **Custom-colored arrow không theo rule** — connector topology-driven; color tier chỉ ảnh hưởng incoming arrow theo target rule.
- **Path card giải thích tier semantics** — path mô tả *write method*, không mô tả tier chứa gì.
- **Thiếu `example_label` content** — mọi tier cần concrete example payload để diagram không trở nên abstract.
- **Promotion label dài quá 14 char** — rút gọn như `AGGREGATE`; label dài phá rhythm.

---

## 9. Examples

- `assets/example-medallion.html` — minimal light, NatStat quarterly survey: 5 tier, 2 path card, Aggregated focal.
- `assets/example-medallion-dark.html` — cùng data, dark skin.
- `assets/example-medallion-full.html` — editorial-card frame với subtitle + summary cards.

---

## 10. Worked YAML

YAML ở §1 là **complete** input definition cho shipped `example-medallion.html`. Mọi coordinate trong SVG của file đó derive từ §2 áp lên input này. Cùng YAML được embed dưới dạng top-of-file HTML comment trong `example-medallion.html`, để source view hiển thị parametric input ngay phía trên SVG.
