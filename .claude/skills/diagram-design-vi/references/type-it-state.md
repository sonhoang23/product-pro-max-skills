# IT current-state

**Phù hợp nhất cho:** tài liệu hoá bức tranh *trước khi hiện đại hoá* trong một modernization proposal — landscape IT legacy được nhóm theo phase hoặc department (Collection → Processing → Dissemination, hoặc Frontend / Backend / Storage, hoặc Survey → Analysts → Reports), trong đó pain-point được flag, hand-off dựa trên file được label (CSV / Excel / Email / Copy), và tooling trước platform được nhìn thấy rõ. Đây là companion của `type-dp-integration.md`: type này cho thấy khoảng trống mà proposal data platform sẽ đóng lại.

Dùng khi stakeholder cần nhìn thấy friction trong setup hiện tại — script siloed, chuyển file thủ công, thiếu version control, single-point-of-failure — và đường chuyển từ hiện trạng đó tới target platform topology.

Type này là **parametric** — input schema ở §1 điều khiển mọi coordinate qua công thức §2. Rule shape mirror `type-dp-integration.md` (zone + cross-cutting footer bar), `type-process.md` (connector right-angle bo góc) và `type-medallion.md` (per-element `color` override), để focal rule, color override, dark mode và reproducibility checklist đọc nhất quán giữa các type.

---

## 1. Input — contract tham số

```yaml
title:    "Current IT Landscape"
subtitle: "Data pipeline before the platform"
eyebrow:  "NatStat · Before the platform"

orientation: horizontal      # horizontal (default, zones L→R) | vertical (zones T→B)

zones:                       # 2..4 zones, ordered along the orientation axis
  - name: "COLLECTION"
    components:              # 1..5 components per zone
      - id: survey-solutions
        name: "Survey Solutions"
        sub:  "CAPI · PostgreSQL"
        icon: postgres               # any id from references/primitive-icons.md
        kind: standard               # standard | focal | external (external → dashed stroke)
      - { id: aspnet,    name: "ASP.NET Apps",    sub: "migration · admin portals", icon: server }
      - { id: civil-reg, name: "Civil Registry",  sub: "external · CRVS data",      icon: database, kind: external }
  - name: "PROCESSING"
    components:
      - { id: shared-drive,  name: "Shared Drive",     sub: "No version control · Windows file share", icon: file,      kind: focal }
      - { id: analyst-mach,  name: "Analyst Machines", sub: "SPSS · SAS · Stata · Excel",              icon: desktop }
      - { id: sql-server,    name: "SQL Server",       sub: "on-premises · core RDBMS",                icon: sqlserver, color: "#7a8c47" }  # custom olive
  - name: "DISSEMINATION"
    components:
      - { id: legacy-portal,   name: "LegacyPortal",      sub: "manual bottleneck",     icon: cloud,    kind: focal }
      - { id: natstat-website, name: "NatStat Website",   sub: "public · static pages", icon: internet }
      - { id: ministry,        name: "Ministry Partners", sub: "~6 ministries",         icon: users,    kind: external }

connectors:                   # ordered list; each links two component ids
  - { from: survey-solutions, to: shared-drive,   label: "CSV",     icon: csv,   style: link }
  - { from: aspnet,           to: shared-drive,   label: "EMAIL",   icon: file,  style: link }      # `mail` MISSING in catalog → falls back to `file`
  - { from: civil-reg,        to: shared-drive,   label: "EXCEL",   icon: excel, style: link, dashed: true }
  - { from: shared-drive,     to: analyst-mach,   label: "COPY",                 style: accent, dashed: true }
  - { from: analyst-mach,     to: sql-server,     label: "LOAD",                 style: neutral }
  - { from: analyst-mach,     to: legacy-portal,   label: "EXCEL",  icon: excel, style: accent }
  - { from: legacy-portal,    to: natstat-website, label: "WEB",                 style: neutral }
  - { from: natstat-website,  to: ministry,        label: "CSV DL", icon: csv,   style: link, dashed: true }

footer:                       # 0..3 optional full-canvas-width bars (cross-cutting concerns)
  - { name: "Identity Manager", sub: "Active Directory · LDAP · SSO", icon: active-directory }
  - { name: "Observability",    sub: "logs · metrics · alerts",       icon: monitoring }

legend:                       # auto-generated from styles used; user can override labels
  - { swatch: link,    label: "data flow" }
  - { swatch: accent,  label: "pain-point" }
  - { swatch: dashed,  label: "external" }
  - { swatch: focal,   label: "bottleneck" }

dark: false
```

**Semantics của field reserved:**

- `orientation` — `horizontal` (zone chạy L→R, component stack vertical trong từng zone) hoặc `vertical` (zone stack T→B, component chạy L→R trong từng zone).
- `zones[i].name` — label uppercase ngắn, ≤14 char. Render ở top-left zone box bằng role `eyebrow`, tracking 0.14em, nằm trên đoạn border được paper-mask.
- `components[i][k].id` — slug globally unique; được `connectors[].from/to` tham chiếu.
- `components[i][k].name` — role `node-name`, label con người đọc được.
- `components[i][k].sub` — role `sublabel` 10px, màu muted; technical sub-label, tối đa 2 line qua auto-wrap khi component height tăng lên 72.
- `components[i][k].icon` — bất kỳ id nào trong `references/primitive-icons.md`. Nếu thiếu → không icon, name shift trái. Catalog có 41 icon; `mail` hiện còn thiếu nên dùng `icon: file` làm fallback cho email hand-off.
- `components[i][k].kind` — `standard | focal | external`. `focal` kích hoạt accent palette (§5); `external` chuyển stroke sang dashed `4,2` và muted ink để báo “ngoài scope của chúng ta”.
- `components[i][k].color` — optional per-component color override (§4). Bị ignore trên `kind: focal` vì accent thắng.
- `connectors[k].from` / `connectors[k].to` — tham chiếu component `id`. Cross-zone, cross-row, same-zone vertical và same-zone horizontal đều hợp lệ; routing do §3 chọn.
- `connectors[k].label` — uppercase text ngắn, ≤8 char. Role `arrow-label` 9px, weight 600.
- `connectors[k].icon` — optional inline icon bên trái text. Cùng catalog với component icon.
- `connectors[k].style` — `neutral | link | accent`. Điều khiển stroke color + marker.
- `connectors[k].dashed` — `true | false`.
- `footer[k]` — optional cross-cutting bar, span full canvas width trừ margin. Không connector nào vẽ ra từ footer.
- `legend[k].swatch` — `link | accent | dashed | focal | neutral`. Auto-curated theo những style diagram thực sự dùng; user có thể reorder hoặc rename.

---

## 2. Công thức layout — geometry deterministic

```
# Horizontal orientation (default)
left_pad        = 16
right_pad       = 16
zone_gap        = 20
zone_y          = 52
zone_h          = 360
n_zones         = len(zones)

# Zone widths: base 200 + 24 per component to give vertical room for icons + 2-line subs.
# In the canonical example (3 / 3 / 3 components) the replication used 256 / 360 / 272 —
# the formula approximates that with hand-picked widths in the worked YAML (§10).
zone_w(i)       = base + n_components_i * comp_slack             # base ≈ 200, slack ≈ 24
viewBox_w       = left_pad + Σ zone_w(i) + (n_zones-1) * zone_gap + right_pad

# Component placement within zone i
comp_pad_x      = 20                                              # x-inset from zone border
comp_h          = 56                                              # 68 for focal (2-line sub), 72 if both sub lines present
comp_gap        = 32
comp_y(i, k)    = zone_y + 28 + k * (comp_h + comp_gap)

# Component centerlines (used for connector routing)
comp_x(i)       = zone_x(i) + comp_pad_x
comp_w(i)       = zone_w(i) - 2 * comp_pad_x
comp_cx(i)      = comp_x(i) + comp_w(i)/2
comp_cy(i, k)   = comp_y(i, k) + comp_h/2

# Footer bars (if present)
footer_bar_h    = 56
footer_gap      = 8
footer_top      = zone_y + zone_h + 24
footer_y(k)     = footer_top + k * (footer_bar_h + footer_gap)
footer_bottom   = footer_top + N_footer * (footer_bar_h + footer_gap) - footer_gap

# Total canvas height
legend_block_h  = 40
content_bottom  = N_footer > 0 ? footer_bottom : zone_y + zone_h
viewBox_h       = content_bottom + legend_block_h + 24
```

### 2.1 Background và zone frame

Solid paper fill toàn `viewBox`. Không dot pattern. Mỗi zone box:

```svg
<rect x="zone_x(i)" y="zone_y" width="zone_w(i)" height="zone_h"
      fill="{ink @ 0.02}" stroke="{ink @ 0.10}" stroke-width="0.8" rx="8"/>
<!-- paper-masked break for the zone label -->
<rect x="zone_x(i)+20" y="zone_y-8" width="{label_w}" height="16" fill="{paper}"/>
<text x="zone_x(i)+24" y="zone_y+4" fill="{ink @ 0.40}"
      font-family="{eyebrow}" letter-spacing="0.14em">{name}</text>
```

### 2.2 Component box

Ba visual kind:

| `kind` | Fill | Stroke | Stroke width | Stroke dash | Name ink | Sub ink |
| --- | --- | --- | --- | --- | --- | --- |
| `standard` | `#FFFFFF` | `ink` | 1 | — | `ink` | `muted` |
| `focal` | `accent @ 0.07` | `accent` | 1.4 | — | `ink` | `accent` line 1 + `muted` line 2 |
| `external` | `#FFFFFF` | `muted` | 1 | `4,3` | `ink` | `muted` |

**Icon placement** — 24×24, monochrome qua `currentColor`; xem `references/primitive-icons.md`:

```svg
<g transform="translate(comp_x + 12, comp_y + (comp_h - 24)/2)" color="{ink_for_kind}">
  <use href="#icon-{name}"/>            <!-- or inline the SVG path from the catalog -->
</g>
```

Icon chiếm 24×24 → total footprint horizontal 36px với left pad 12px. Baseline name và sub-label shift phải 40px.

**Baseline name + sub**, left-aligned, icon ở trái:

```
name_x = comp_x + 44
name_y = comp_y + (comp_h/2) - 2
sub_y  = comp_y + (comp_h/2) + 14
```

### 2.3 Connector geometry — §3 giữ routing rule

```
src_right  = comp_x(i_src) + comp_w(i_src)
src_left   = comp_x(i_src)
src_top    = comp_y(i_src, k_src)
src_bot    = src_top + comp_h_src
src_cy     = src_top + comp_h_src/2

dst_left   = comp_x(i_dst)
dst_right  = comp_x(i_dst) + comp_w(i_dst)
dst_top    = comp_y(i_dst, k_dst)
dst_bot    = dst_top + comp_h_dst
dst_cx     = comp_cx(i_dst)
dst_cy     = dst_top + comp_h_dst/2

# Corridor x for cross-zone H+Q+V routing
corridor_x = dst_cx                            # land arrow on dst horizontal center, enter via top/bot
```

### 2.4 Footer bar

```svg
<rect x="left_pad" y="footer_y(k)" width="viewBox_w - 2*left_pad" height="footer_bar_h"
      fill="{ink @ 0.03}" stroke="{ink @ 0.18}" stroke-width="0.8" rx="8"/>
<g transform="translate(left_pad + 20, footer_y(k) + (footer_bar_h - 24)/2)" color="{ink}">
  <use href="#icon-{name}"/>
</g>
<text x="left_pad + 56" y="footer_y(k) + 24" font-family="{node-name}" font-size="14" fill="{ink}">{name}</text>
<text x="left_pad + 56" y="footer_y(k) + 40" font-family="{sublabel}" font-size="12" fill="{muted}">{sub}</text>
```

Footer bar là service layer-wide. **Không connector nào phát ra từ chúng.** Chúng nằm trực quan dưới các zone để người đọc thấy cross-cutting concern ngay lập tức.

### 2.5 Legend strip

Hairline divider tại `y = content_bottom + 16`, sau đó row swatch + label tại `y = content_bottom + 36`. Chỉ những style thực sự được `connectors[]` dùng — cộng `focal` và `external` nếu component kind tương ứng có mặt — xuất hiện trong legend.

---

## 3. Quy tắc connector — bắt buộc

### 3.1 Path shape — rounded right-angle Q-bezier, r = 8

Reuse nguyên rule từ `type-process.md` §3.1. Không diagonal — bao giờ cũng vậy.

```svg
<!-- Same zone, adjacent component (same vertical column): single vertical line -->
<line x1="{src_cx}" y1="{src_bot}" x2="{dst_cx}" y2="{dst_top}"
      stroke="…" stroke-width="…" marker-end="…"/>

<!-- Cross-zone or cross-row: exit right → H → Q-bend → V → enter top (or bottom) -->
<path d="M {src_right},{src_cy}  H {dst_cx - 8}  Q {dst_cx},{src_cy} {dst_cx},{src_cy ± 8}  V {dst_top_or_bottom}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>
```

- Dùng `{src_cy + 8}` và `V {dst_top}` khi destination nằm DƯỚI source.
- Dùng `{src_cy − 8}` và `V {dst_bottom}` khi destination nằm TRÊN source.

### 3.2 Side exit / entry — configurable, mặc định như dưới

| Topology | Default exit side source | Default entry side destination |
| --- | --- | --- |
| Same zone, dst below | bottom | top |
| Same zone, dst above | top | bottom |
| Cross-zone, horizontal flow | right | top hoặc bottom, chọn phía gần `src_cy` hơn |
| Vertical-orientation diagram | bottom | top |

Connector có thể override qua `connectors[k].from_side` / `connectors[k].to_side` (`top | right | bottom | left`). **Backward reference** — right→left trong horizontal orientation hoặc đi lên trong vertical orientation — chỉ được phép khi ít nhất một endpoint có `kind: external` và bắt buộc `dashed: true`.

### 3.3 Marker PHẢI chạm destination rectangle

Command cuối của path phải kết thúc tại edge của destination rectangle — `V {dst_top}` hoặc `H {dst_left}` — **không** phải centroid. Sau khi áp `refX=7` trên marker, triangle nằm flush với border. Dừng line trước edge hoặc gửi nó vào centroid rồi chôn arrowhead trong rect là hard fail.

### 3.4 Style → stroke + marker

| `style` | Stroke color | Stroke width | Marker |
| --- | --- | --- | --- |
| `neutral` | `muted` | 1.0 | `url(#arrow)` |
| `link` | `link` | 1.2 | `url(#arrow-link)` |
| `accent` | `accent` | 1.4 | `url(#arrow-accent)` |

Thêm `stroke-dasharray="4 3"` khi `dashed: true`.

**Defs block** — luôn emit đủ ba:

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{muted}"/></marker>
  <marker id="arrow-link"   markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{link}"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{accent}"/></marker>
</defs>
```

### 3.5 Connector label = inline icon + text, đặt ở ĐẦU connector với margin vuông góc

Label nằm **gần source end** của connector, không nằm giữa segment, và **offset vuông góc với line** để không overlap stroke. Icon, khi có `icon:`, nằm trong paper-fill mask của label bên trái text.

```svg
<g transform="translate({label_cx}, {label_cy})">
  <rect x="-{w/2}" y="-9" width="{w}" height="18" rx="3" fill="{paper}" stroke="none"/>
  <use href="#icon-{icon}" x="-{w/2 + 4}" y="-6" width="12" height="12" color="{stroke_color}"/>     <!-- if icon set -->
  <text x="{icon ? (-(w/2) + 22) : 0}" y="3" text-anchor="{icon ? 'start' : 'middle'}"
        font-family="{arrow-label}" font-size="9" font-weight="600"
        letter-spacing="0.08em" fill="{stroke_color}">{label}</text>
</g>
```

**Công thức placement** — label box cao 18px × width `w`, centered tại `{label_cx, label_cy}`:

| Segment rời source | `label_cx` | `label_cy` | Hiệu ứng |
| --- | --- | --- | --- |
| Horizontal — right exit | `src_right + 6 + w/2` | `src_cy − 14` | Label nằm 6px sau source, 5px trên line |
| Horizontal — left exit, backward | `src_left − 6 − w/2` | `src_cy − 14` | Label nằm 6px trước source, 5px trên line |
| Vertical — bottom exit | `src_cx + 6 + w/2` | `src_bot + 14` | Label nằm 6px bên phải line, 5px dưới source edge |
| Vertical — top exit, backward | `src_cx + 6 + w/2` | `src_top − 14` | Label nằm 6px bên phải line, 5px trên source edge |

Với route cross-zone H+Q+V, label bind vào **horizontal** segment vì segment này anchored tại source. Đặt label sớm trên horizontal run — không bao giờ trên Q-bend hoặc vertical tail.

- `w = text_w + (icon ? 30 : 12)` — auto-fit.
- Mask `fill` resolve thành `paper` ở light mode và `ink` ở dark mode. Mask vẫn được giữ như safety pad — dù label không còn nằm trên line, nó có thể chạm zone background hoặc component fill; mask giữ contrast.
- `stroke_color` theo §3.4 — text + icon inherit accent/link/neutral của connector.

### 3.6 Z-order

Mọi connector — path + line + label — emit TRƯỚC component rect để node fill mask line end. Connector label là exception nhỏ: nó draw SAU line của chính nó để mask nằm trên stroke.

---

## 4. Component color override — per-component `color: "#hex"`

Per-component, cùng shape với mọi parametric type khác trong skill.

| Element | Light | Dark |
| --- | --- | --- |
| Container fill | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| Container stroke | `rgba(C, 0.45)` — width 1 | `rgba(C_light, 0.55)` |
| Component name text | `C` | `C_light` |
| Icon glyph | inherit ink qua `currentColor`, không đổi | inherit ink, không đổi |
| Sub-label | muted, không đổi | muted, không đổi |
| Connector chạm component | **không đổi** — topology-driven | **không đổi** |

`C_light` = cùng hex lightened khoảng 15% cho dark-mode contrast, ví dụ `#7a8c47` → `#9aac67`, `#b85450` → `#d97a78`.

**Quy tắc:**
- **Không trên focal component.** `kind: focal` luôn render accent; `color` bị silently ignored.
- **Không trên connector.** Connector style topology-driven; muốn edge màu thì chọn `style: accent` / `link` / `neutral`, không dùng component color.
- **Cap ≤3 custom-colored component mỗi diagram**, ngoài focal. Trên 3 visual signal bắt đầu fragment.

**Cross-type palette khuyến nghị** — cùng `type-medallion.md` / `type-process.md` / `type-dp-integration.md` / `type-dp-security-matrix.md`:

- `#b85450` rust-red — security / governance / pain-point không phải focal
- `#5a7d9a` slate-blue — observability / quality / monitoring gate
- `#7a8c47` olive-green — survivor system, tool platform mới vẫn giữ
- `#c9a23a` warm yellow — sandbox / dev / scratch
- `#8c6d3f` warm-brown — archive / cold / DR

---

Trong component input, explicit icon field dùng literal `icon:`; giá trị sau field này vẫn là icon ID từ catalog.

## 5. Focal rule

- Component `kind: focal`: **≤2 mỗi diagram**; zero cũng hợp lệ nếu không có một dominant pain-point duy nhất.
- Auto-styling: accent stroke 1.4, accent-tinted fill 7%, `node-name` ink-bold, line-1 `sublabel` accent.
- Bất kỳ connector có focal endpoint đều auto render `style: accent`; YAML `style:` bị ignore.
- Custom `color: "#hex"` trên focal bị silently ignore — accent luôn thắng.

Nếu diagram cần hơn 2 focal component, bạn đã gộp hai narrative. Split: một diagram “collection pain-points” + một diagram “dissemination pain-points”.

---

## 6. Dark mode

| Role | Light | Dark |
| --- | --- | --- |
| paper | `paper` | `ink` |
| ink | `ink` | `paper` |
| muted | `muted` | `muted` |
| accent | `accent` | `accent` |
| link | `link` | `link` |
| zone background | `ink @ 0.02` | `paper @ 0.04` |
| zone border | `ink @ 0.10` | `paper @ 0.14` |
| standard component fill | `#FFFFFF` | `paper @ 0.04` |
| standard component stroke | `ink` | `paper @ 0.32` |
| focal fill | `accent @ 0.07` | `accent @ 0.12` |
| focal stroke | `accent` | `accent` |
| external stroke | `muted` dashed | `muted` dashed |
| footer fill | `ink @ 0.03` | `paper @ 0.05` |
| footer stroke | `ink @ 0.18` | `paper @ 0.20` |
| label mask fill | `paper` | `ink` |
| custom-color component | `C` | `C_light` — ≈ +15% |

---

## 7. Checklist reproducibility — taste gate

Trước khi emit SVG, verify **mọi** item:

1. Eyebrow + title + subtitle có mặt tại canonical y-position 24 / 36 / 52; body padding 32px.
2. Có 2..4 zone; mỗi zone có uppercase label tại top-left zone box, nằm trên paper-masked break của border.
3. Mọi component có `id`, `name`. `sub`, `icon`, `kind`, `color` optional.
4. ≤2 component `kind: focal`; focal styling auto-applied — accent fill 7%, accent stroke 1.4, italic line-1 sub.
5. Mọi connector exit bên right hoặc bottom của source và enter top hoặc left của destination; rounded right-angle Q-bezier `r=8` ở mỗi bend; marker triangle visibly chạm destination rectangle edge.
6. Connector label nằm ở **đầu** connector, không phải mid-segment, và offset **vuông góc** line — gap 5px phía trên horizontal segment, 6px bên phải vertical segment — không overlap stroke. Giữ paper-fill mask phía sau text; icon nếu có nằm bên trái text trong cùng mask.
7. ≤3 custom-colored component; không component nào focal.
8. ≤3 footer bar; mỗi bar span `viewBox_w − 2*left_pad`; không connector phát ra từ footer.
9. Legend dưới cùng: hairline separator + một swatch cho mỗi style thực sự dùng.
10. Dùng `arrow-label` cho connector label, `eyebrow` cho page eyebrow và zone label, `title` cho page title, `node-name` cho subtitle và component name, `sublabel` cho technical sub-label.
11. Marker `#arrow` / `#arrow-link` / `#arrow-accent` defined một lần trong `<defs>`; không inline marker definition.
12. Dark variant: resolve mọi semantic token qua dark-mode value; custom color lightened khoảng 15%.

---

## 8. Anti-pattern

- **Diagonal arrow.** NatStat replication có một arrow analyst → LegacyPortal. Type mới cấm — luôn rounded right-angle Q-bezier.
- **Marker không chạm target.** Path end ở centroid hoặc dừng trước border.
- **Connector label là inline `text` không có mask rect.** Connector line có thể bleed qua text và làm label khó đọc.
- **Label nằm chồng lên connector line ở mid-segment.** Label thuộc về *đầu* connector với perpendicular margin, xem §3.5 — chôn label giữa line vừa che direction source→destination vừa bắt mắt người đọc vật lộn với mask.
- **Tiny text badge dùng làm icon.** Source dùng badge 7px `DB` / `APP` / `EXT`; type này dùng real catalog icon 24px. Text badge chỉ chấp nhận làm label text, không phải component “icon”.
- **Custom color trên focal component.** Focal luôn thắng; user-set `color` silently ignored trên `kind: focal`.
- **Footer bar wire vào một component.** Footer = cross-cutting layer-wide concern; connector từ footer tới một tool cụ thể là category error. Chỉ dùng AUTH-line pattern của `type-dp-integration.md` khi footer service thực sự authenticate *mọi* component, và khi đó line land ở zone bottom edge, không phải tool cụ thể.
- **>16 total component hoặc >5 mỗi zone.** Density cap; split thành hai diagram.
- **Mix orientation trong một diagram.** Chọn một — `horizontal` hoặc `vertical` — và áp cho mọi zone.
- **Dùng `kind: focal` flag mọi thứ đau.** Focal chỉ dành ≤2 narrative pain-point; với “xấu nhưng không headline-bad”, dùng `color: "#b85450"` rust-red.

---

## 9. Ví dụ

- `assets/example-it-state.html` — minimal light, NatStat canonical: 3 zone, 9 component, 8 connector, 0 footer bar, SQL Server tinted olive. Gallery default.
- `assets/example-it-state-dark.html` — tương tự, dark skin.
- `assets/example-it-state-full.html` — tương tự, editorial-card frame với summary card.
- `assets/example-it-state-extended.html` — exercise §4 color override + footer bar: 2 footer bar (Identity Manager + Observability) dưới zone, custom color thứ ba trên Analyst Machines — slate-blue, data-quality concern.
- `assets/example-it-state-extended-dark.html` — extended pattern, dark skin.

---

## 10. Worked YAML — full input cho `example-it-state.html`

Đây là complete input map vào shipped canonical example. Mọi coordinate trong SVG đó đều suy ra được từ §2 áp lên input này.

```yaml
title:    "Current IT Landscape"
subtitle: "Data pipeline before the platform"
eyebrow:  "NatStat · Before the platform"

orientation: horizontal

zones:
  - name: "COLLECTION"
    components:
      - { id: survey-solutions, name: "Survey Solutions", sub: "CAPI · PostgreSQL",          icon: postgres }
      - { id: aspnet,           name: "ASP.NET Apps",     sub: "migration · admin portals", icon: server   }
      - { id: civil-reg,        name: "Civil Registry",   sub: "external · CRVS data",      icon: database, kind: external }
  - name: "PROCESSING"
    components:
      - { id: shared-drive,  name: "Shared Drive",     sub: "No version control · Windows file share", icon: file,      kind: focal }
      - { id: analyst-mach,  name: "Analyst Machines", sub: "SPSS · SAS · Stata · Excel",              icon: desktop }
      - { id: sql-server,    name: "SQL Server",       sub: "on-premises · core RDBMS",                icon: sqlserver, color: "#7a8c47" }
  - name: "DISSEMINATION"
    components:
      - { id: legacy-portal,   name: "LegacyPortal",      sub: "manual bottleneck",     icon: cloud,    kind: focal }
      - { id: natstat-website, name: "NatStat Website",   sub: "public · static pages", icon: internet }
      - { id: ministry,        name: "Ministry Partners", sub: "~6 ministries",         icon: users,    kind: external }

connectors:
  - { from: survey-solutions, to: shared-drive,   label: "CSV",    icon: csv,   style: link }
  - { from: aspnet,           to: shared-drive,   label: "EMAIL",  icon: file,  style: link }
  - { from: civil-reg,        to: shared-drive,   label: "EXCEL",  icon: excel, style: link, dashed: true }
  - { from: shared-drive,     to: analyst-mach,   label: "COPY",                style: accent, dashed: true }
  - { from: analyst-mach,     to: sql-server,     label: "LOAD",                style: neutral }
  - { from: analyst-mach,     to: legacy-portal,   label: "EXCEL",  icon: excel, style: accent }
  - { from: legacy-portal,    to: natstat-website, label: "WEB",                 style: neutral }
  - { from: natstat-website,  to: ministry,        label: "CSV DL", icon: csv,   style: link, dashed: true }

dark: false
```

### 10.1 YAML này chứng minh điều gì

- `n_zones = 3`, component mỗi zone `= [3, 3, 3]`, custom color count = 1 (SQL Server), focal count = 2 (Shared Drive, LegacyPortal), external count = 2 (Civil Registry, Ministry Partners).
- Zone width canonical: 256 / 360 / 272 ⇒ `viewBox_w = 16 + 256 + 20 + 360 + 20 + 272 + 16 = 960` ✓
- `viewBox_h = 52 + 360 + 40 + 24 = 500` khi không footer bar ✓
- Shared Drive focal tại zone 2, row 0: `x = 340, y = 80, w = 264, h = 68`; focal stretch tới 68 để fit sub 2 line ✓
- LegacyPortal focal tại zone 3, row 0: `x = 704, y = 80, w = 208, h = 60` ✓
- SQL Server custom olive tại zone 2, row 2: container fill `rgba(122,140,71,0.06)`, stroke `rgba(122,140,71,0.45)`, name text `#7a8c47` ✓
- Connector 4, 5 trong zone 2 và 7, 8 trong zone 3 là vertical `<line>` đơn giản. Cross-zone connector dùng route đúng rule — xem SKILL.md §6 rule 4 & 5:
  - **Cả ba connector Survey-side → Shared Drive (C1 / C2 / C3) enter LEFT edge của Shared Drive.** Nếu enter top-edge, marker body — lùi 7px theo hướng đi do `refX = 7` — sẽ bị đẩy *vào trong* destination box, nơi paper-fill của box che nó; chỉ tip 1px ló ra trên stroke. Enter left edge với path đi sang phải giữ body bên ngoài box, khoảng 7px hiện bên trái edge. Ba left-edge attach point fan tại **y = 108 / 124 / 140**, spacing 16px, lớn hơn rule-4 minimum 12px.
  - **C1** — Survey → Shared Drive — source y trùng landing y: horizontal đơn `M 252,108 H 340`. Không cần bend.
  - **C2** — ASP.NET → Shared Drive — detour lên qua background zone 2; vertical tại `x = 316`, clear left edge Shared Drive `x = 340`: `H 308 Q 316,196 316,188 V 132 Q 316,124 324,124 H 340`. Land tại `(340, 124)`.
  - **C3** — Civil Registry → Shared Drive — detour lên qua background zone 2; vertical tại `x = 332`, clear Analyst Machines bắt đầu `x = 340`: `H 324 Q 332,284 332,276 V 148 Q 332,140 340,140`. Land tại `(340, 140)` qua final Q-bend, không cần trailing H.
  - **C6** — Analyst Machines → LegacyPortal — không thể dùng direct H+Q+V vào left edge LegacyPortal vì hai node nằm khác row, và horizontal trực tiếp ở `y = 268` sẽ cắt NatStat Website. Route detour qua zone gap và **phía trên** LegacyPortal: `H 654 Q 662,268 662,260 V 72 Q 662,64 670,64 H 800 Q 808,64 808,72 V 80` — vertical tại `x = 662` trong zone gap, horizontal tại `y = 64` phía trên LegacyPortal top, sau đó đi xuống top center của LegacyPortal. Path enter LegacyPortal từ **trên đi xuống**, nên arrow body nằm trên box và visible; chỉ tip 1px đi vào box.

**Rule of thumb về marker visibility:** với standard arrow marker (`markerWidth = 8`, `refX = 7`), arrow body kéo dài 7px *ngược lại* hướng path từ endpoint. Để marker còn visible, tail 7px đó phải nằm *ngoài* destination box. Suy ra:
- Enter **TOP edge khi path đi LÊN** — box ở dưới → body nằm trong box, **chỉ 1px visible. Tránh.**
- Enter **TOP edge khi path đi XUỐNG** — box ở dưới → body nằm trên box, ~7px visible. ✓
- Enter **LEFT edge khi path đi PHẢI** → body bên trái box, ~7px visible. ✓
- Enter **RIGHT edge khi path đi TRÁI** → body bên phải box, ~7px visible. ✓
- Enter **BOTTOM edge khi path đi XUỐNG** — box ở trên → body nằm trong box, **chỉ 1px visible. Tránh.**
- Enter **BOTTOM edge khi path đi LÊN** — box ở trên → body dưới box, ~7px visible. ✓

Khi source row khớp y-range của destination row, ví dụ Survey y=108 với Shared Drive y=80–148, ưu tiên **side-edge entry** — horizontal path đơn với arrow fully visible. Khi source row offset, detour qua background gần nhất của destination zone để enter side edge thay vì tiếp cận top/bottom edge từ phía sai.

Extended example ở §9 dòng 4 chứng minh footer bar + custom color thứ ba và chứng minh `viewBox_h` grow đúng khi `N_footer > 0`.
