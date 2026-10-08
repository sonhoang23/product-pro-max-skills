# Process

**Phù hợp nhất cho:** quy trình nghiệp vụ tuần tự có nhiều actor/division, nơi người đọc cần thấy *ai* làm *việc gì*, *data nào* vào/ra từng step và *tool nào* được dùng — không chỉ thứ tự step. Bao gồm responsibility audit, data-quality gate review, cross-divisional handoff map và end-to-end workflow documentation.

Ưu tiên Swimlane — đơn giản hơn — khi data type và tool không quan trọng. Ưu tiên Process khi input/output payload và responsible team của từng step phải đọc được ngay.

Type này **parametric** — input schema §1 điều khiển mọi coordinate bằng formula §2. Cùng input phải sinh SVG giống nhau về hình học. Rule shape mirror `type-data-flow.md`, nên `color` override, IN/OUT chip semantic và reproducibility checklist nhất quán giữa các type.

---

## 1. Inputs — parameter contract

```yaml
lanes:                              # 1..6 horizontal swimlanes (top to bottom)
  - { name: ["RD&E"],                 key: "RDE" }
  - { name: ["IT"],                   key: "IT"  }
  - { name: ["FIELD", "SERVICES"],    key: "FLD" }
  - { name: ["SURVEY", "SERVICES"],   key: "SVY" }
  - { name: ["HOUSEHOLD", "UNIT"],    key: "HHU" }
  - { name: ["COMMS &", "MARKETING"], key: "CMM" }

steps:                              # 1..12 vertical step columns (left to right)
  - { number: "1",  label: "Design"   }
  - { number: "2",  label: "Build"    }
  - { number: "3",  label: "Test", focal: true }       # focal step header chip — accent fill
  - { number: "4",  label: "Train"    }
  # ... up to 12

nodes:                              # explicit per-cell entries; empty cells render nothing
  - { lane: "RDE", step: 0,  title: "Survey design",      sub: "questionnaire · sampling", tool: "Excel · CSPro",
      chips: {in: null,  out: "FL"} }              # first step has no input chip
  - { lane: "IT",  step: 1,  title: "Build app",          sub: "form + validation",        tool: "CSPro · scripts",
      chips: {in: "FL", out: "TB"}, color: "#5a7d9a" }    # slate-blue — data quality concern
  - { lane: "RDE", step: 2,  title: "Pilot test",         sub: "field debug",              tool: "tablet · script",
      chips: {in: "TB", out: "TB"}, focal: true }   # focal node — accent border
  - { lane: "FLD", step: 3,  title: "Train enumerators",  sub: "protocols · safety",       tool: "manual",
      chips: {in: "TB", out: "LS"}, color: "#b85450" }    # rust-red — governance / training
  # ... etc

arrows:                             # explicit edges; styles bind to topology (see §3)
  - { from: {lane: "RDE", step: 0}, to: {lane: "IT",  step: 1}, style: "normal" }
  - { from: {lane: "IT",  step: 1}, to: {lane: "RDE", step: 2}, style: "focal-in" }     # accent — into focal
  - { from: {lane: "RDE", step: 2}, to: {lane: "FLD", step: 3}, style: "focal-out" }    # accent — out of focal
  - { from: {lane: "RDE", step: 2}, to: {lane: "IT",  step: 1}, style: "trigger" }      # dashed trigger
  # ... etc

dark: false
```

**Semantic dành riêng cho field:**

- `lanes[k].key` — text badge role 3-letter được hiển thị bên trong mọi node thuộc lane đó.
- `lanes[k].name` — lane label 1 hoặc 2 dòng, uppercase mono.
- `steps[j].focal: true` — chính xác **một** step được khai báo; header chip dùng accent.
- `nodes[i].focal: true` — chính xác **một** node được khai báo; accent border (§5).
- `nodes[i].chips` — object `{in: "<CODE>", out: "<CODE>"}`; bên nào cũng có thể `null` để bỏ. Code từ §8. **Bỏ** input chip ở node thuộc first step và **bỏ** output chip ở node thuộc last step.
- `nodes[i].color` — optional per-node `"#hex"` `color` override. Palette §4 được khuyến nghị để giữ consistency cross-diagram.

---

Rule shape mirror `type-data-flow.md`. Reserved focal literals là `steps[j].focal: true` và `nodes[i].focal: true`.

## 2. Layout formulas — deterministic geometry

```
label_col_w      = 140
step_slot_w      = 112                                # 100-px node + 12-px corridor
right_pad        = 28
n_steps          = len(steps)
n_lanes          = len(lanes)

# Canvas
viewBox_w        = label_col_w + n_steps * step_slot_w + right_pad   # 11 steps → 1400
header_h         = 36
lane_h           = 80
has_color_row    = any(node.color or step.color or lane.color in inputs)
legend_h         = 100 if has_color_row else 80       # 4 rows when colors are present
viewBox_h        = header_h + n_lanes * lane_h + legend_h            # 6 lanes, no colors → 596; with → 616

# Header strip (top)
chip_y           = 8
chip_w           = 16                                  # 20 if step.number has 2 digits
chip_h           = 16
chip_rx          = 8                                   # pill

# Lane positions
lane_y_top(k)    = header_h + k * lane_h               # 36, 116, 196, 276, 356, 436
lane_y_mid(k)    = lane_y_top(k) + lane_h/2            # 76, 156, 236, 316, 396, 476
lane_label_x     = label_col_w / 2                     # 70

# Step / node centers
step_cx(j)       = label_col_w + 8 + j * step_slot_w + node_w/2      # 198, 310, 422, ...
                                                                      # (8-px gutter inside content area)

# Nodes
node_w           = 100
node_h           = 64
node_x(j)        = step_cx(j) - node_w/2
node_y(k)        = lane_y_top(k) + (lane_h - node_h)/2     # 8-px top/bottom margin inside lane

# Legend strip (bottom)
legend_y_top     = header_h + n_lanes * lane_h
legend_row_y     = [legend_y_top + 16, legend_y_top + 37,
                    legend_y_top + 58, legend_y_top + 79]
```

### 2.1 Background structure

- Paper fill trên toàn viewBox.
- Dot pattern: grid 22×22, `circle r=0.8`, `fill rgba(45,49,66,0.10)`. Opacity 0.55.
- Alternating lane tint: lane index 0, 2, … nhận `rgba(45,49,66,0.018)` fill từ `x=140` tới `viewBox_w`.
- Lane divider: horizontal hairline tại mọi `lane_y_top(k)` và `legend_y_top`; stroke `rgba(45,49,66,0.12)` width 0.8.
- Right border của label column: vertical hairline `x=label_col_w`, stroke `rgba(45,49,66,0.20)` width 1, từ `y=header_h` đến `y=legend_y_top`.

Label-column divider nằm tại `x = label_col_w`, từ `y = header_h` tới `y = legend_y_top`.

### 2.2 Step header chip + label

Cho step `j`:

```
chip_w(j)        = 20 if len(step.number) >= 2 else 16
chip_x(j)        = step_cx(j) - chip_w(j)/2
number_anchor    = (step_cx(j), chip_y + 11)
label_anchor     = (step_cx(j), 32)              # 8-px gap below chip
```

**Chip** — numbered pill ở đầu mỗi column:

- Default fill: `rgba(45,49,66,0.12)`, number text ink.
- Focal fill: `rgba(235,108,54,0.20)`, number text accent (§5).
- Per-step `color` override (§4): fill `rgba(C,0.20)`, number `C`.

**Label** — uppercase mono text dưới chip:

- Render `steps[j].label` uppercased tại `label_anchor`.
- Geist Mono 6px, weight 500, `letter-spacing="0.12em"`, `text-anchor="middle"`.
- Default fill muted; focal fill accent.
- Per-step `color`: fill=`C`.
- Giữ label ngắn ≤9 char. Label dài bị truncate; cần dài hơn thì abbreviate.

### 2.3 Lane labels

Mono label 1–2 dòng, uppercase, letter-spacing 0.08em, 8px, muted, centered tại `(lane_label_x,lane_y_mid(k))`:

- một dòng: `(lane_label_x, lane_y_mid(k)+4)`;
- hai dòng: y=`lane_y_mid(k)-4` và `+4`.

Per-lane `color` override đổi label thành `C` và lane stripe tint thành `rgba(C,0.04)`.

Lane label center tại `(lane_label_x, lane_y_mid(k))`; single-line dùng `(lane_label_x, lane_y_mid(k) + 4)`, two-line dùng `(lane_label_x, lane_y_mid(k) - 4)` và `(lane_label_x, lane_y_mid(k) + 4)`. Per-lane tint dùng `rgba(C, 0.04)`.

### 2.4 Node content layout — bên trong 100×64 `rect`

```
role_chip          rect 14×10 at (node_x+4, node_y+4),  rx=2
role_chip_text     centered at (node_x+11, node_y+12), font-size=6, weight=600
                                                                # text = lanes[k].key (3-letter lane code)
title              centered at (step_cx(j), node_y+26),  font-size=9 sans semibold
in→out             centered at (step_cx(j), node_y+40),  font-size=6.5 mono muted
tool               centered at (step_cx(j), node_y+52),  font-size=6.5 mono soft
data chip IN       rect 16×8 at (node_x+4,   node_y+54), rx=2      # payload entering
data chip OUT      rect 16×8 at (node_x+80,  node_y+54), rx=2      # payload leaving
```

**Role chip text rule:** badge trong node render `lanes[k].key`, trong đó `k` là lane index của node — **không** phải step number. Step number đã nằm trên column header chip §2.2. Lane key làm node tự có “who” identifier ngay cả khi node bị excerpt riêng. Rule này mirror `type-data-flow.md` §2.4.

Empty cell không render **gì cả** — không placeholder rect, role chip hay label.

**Chip-vs-tool-text collision:** chip ở `node_y+54..62`, tool baseline `node_y+52`. Nếu node có two-line title — hiếm — tăng node_h thành 72 **hoặc** bỏ chips. Default: bỏ chip khi collision.

---

Chip collision contract: chip nằm `node_y + 54..62`, tool baseline ở `node_y + 52`.

## 3. Connector rules — bắt buộc

Ba `style` bind topology. Connector vẽ **trước** mọi node rect.

| `style` | Stroke | Width | Dash | Marker | Khi bắt buộc |
|---|---|---:|---|---|---|
| `normal` | `#4f5d75` muted | 1.0 | — | `arrow` | Standard handoff. Unlabelled. |
| `focal-in` / `focal-out` | `#eb6c36` accent | 1.2 | — | `arrow-accent` | Edge có target là focal hoặc origin là focal. |
| `trigger` | `#4f5d75` muted | 1.0 | `4,3` | `arrow-sm` | Orchestration trigger. Unlabelled. |

**Defs block** bắt buộc:

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="0.8" fill="rgba(45,49,66,0.10)"/>
  </pattern>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
</defs>
```

### 3.1 Routing rules — non-negotiable

**Single-bend right-angle:** exit RIGHT → corridor → enter TOP nếu destination thấp hơn, hoặc BOTTOM nếu destination cao hơn.

- Source: `(node_x+100, lane_y_mid(src_lane))` — right edge, vertical center.
- Destination: `(step_cx(dst_step), node_y(dst_lane))` khi xuống; hoặc `(step_cx(dst_step), node_y(dst_lane)+64)` khi lên.
- Corner radius 8px Q-bezier.
- Same-lane adjacent step: horizontal `<line>` từ src right sang dst left.
- **Không diagonal. Không left-side entry. Không exit top/bottom của source.**

```svg
<!-- Downward (destination lane > source lane) -->
<path d="M {rx},{src_cy} H {dst_cx - 8} Q {dst_cx},{src_cy} {dst_cx},{src_cy + 8} V {dst_top}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>

<!-- Upward (destination lane < source lane) -->
<path d="M {rx},{src_cy} H {dst_cx - 8} Q {dst_cx},{src_cy} {dst_cx},{src_cy - 8} V {dst_bottom}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>

<!-- Same lane (adjacent step) -->
<line x1="{src_right}" y1="{lane_cy}" x2="{dst_left}" y2="{lane_cy}"
      stroke="…" stroke-width="…" marker-end="…"/>
```

- Z-order: connector trước node rect.
- Marker: đúng một `marker-end`, không `marker-start`.
- Arrow mặc định không label. Step number + actor lane đã mang semantic. Chỉ label edge khi nó là non-step concept như re-test loop/escalation; dùng paper mask và 6.5px mono text.

Routing endpoint source là `(node_x + 100, lane_y_mid(src_lane))`; destination phía trên dùng `(step_cx(dst_step), node_y(dst_lane) + 64)`. Connector element là `<line>` hoặc `<path>`, được emit trước node `<rect>`. Edge ra khỏi focal dùng `focal-out`.

### 3.2 Crossings

Tránh. Corridor x — 8px trước destination node — là routing column duy nhất. Nếu hai arrow sẽ cross ở đó, **đổi step assignment** hoặc **split thành hai diagram** thay vì invent bend-around. Crossing che underlying control flow.

---

## 4. Component `color` override

Node, lane hoặc step có thể có optional `color: "#hex"`. Mirror `type-data-flow.md` §4 và `type-high-level.md` §3.4.

### 4.1 Per-node `color`

| Element | Light | Dark |
|---|---|---|
| Container fill | `rgba(C,0.06)` | `rgba(C_light,0.10)` |
| Container stroke | `rgba(C,0.35)` width 1 | `rgba(C_light,0.45)` |
| Role chip fill | `rgba(C,0.18)` | `rgba(C_light,0.22)` |
| Role chip text | `C` | `C_light` |
| Title | `C` | `C_light` |
| Sub-label in→out | **không đổi** muted | **không đổi** |
| Tool label | **không đổi** soft | **không đổi** |
| Data-type chips | **không đổi** | **không đổi** |
| Arrow touching node | **không đổi** — topology-driven | **không đổi** |

`C_light` = same hex lightened ~15%.

Per-node color contract mirror `type-high-level.md`: container `rect` dùng `rgba(C, 0.06)` / `rgba(C_light, 0.10)`, stroke `rgba(C, 0.35)` / `rgba(C_light, 0.45)`, role chip `rgba(C, 0.18)` / `rgba(C_light, 0.22)`. Ví dụ dark-lightening: `#b85450` → `#d97a78`.

### 4.2 Per-step `color`

Header chip fill `rgba(C,0.20)`, number `C`; legend entry match.

Per-step chip dùng `rgba(C, 0.20)`; dark token map giữ `#4f5d75` → `#bfc0c0` và `#eb6c36` → `#f08a59`.

### 4.3 Per-lane `color`

Lane stripe `rgba(C,0.04)`, lane label `C`. Dùng tiết chế.

### 4.4 Rules

- Focal node/step ignore custom `color`; accent thắng.
- Arrow không nhận component `color`; muốn edge `color` thì dùng style §3.
- Tối đa 3 custom-`color`ed element ngoài focal pair.
- Subtitle/tool label vẫn muted/soft.

### 4.5 Semantic palette khuyến nghị

- `#b85450` — Security / Identity / Governance
- `#5a7d9a` — Observability / Quality
- `#7a8c47` — Data Products / Publication
- `#8c6d3f` — Backup / DR / Archive

---

## 5. Focal rule

Process có ba focal slot:

- **Một focal step** — `steps[j].focal: true` — thường là analytical/decision pivot; header/legend chip accent.
- **Một focal node** — `nodes[i].focal: true` — node nhận critical handoff; accent border + role chip, title vẫn ink để đọc rõ.
- **Một focal arrow set** — `focal-in` và `focal-out` — edge vào/ra focal node.

Nếu có 0 hoặc >1 focal step/node, dừng và hỏi user.

---

Để giữ nguyên literal contract nguồn, per-step tint dùng `rgba(C, 0.20)`, per-lane tint dùng `rgba(C, 0.04)`; semantic palette mirror `type-dp-integration.md`; khi color row xuất hiện, biến chiều cao legend là `legend_h`.

## 6. Dark mode

| Token | Light | Dark |
|---|---|---|
| Paper | `#f5f5f5` | `#2d3142` |
| Ink | `#2d3142` | `#f5f5f5` |
| Muted | `#4f5d75` | `#bfc0c0` |
| Soft | `#7a8399` | `#8e98ac` |
| Accent | `#eb6c36` | `#f08a59` |
| Dot pattern | `rgba(45,49,66,0.10)` | `rgba(245,245,245,0.10)` |
| Lane tint | `rgba(45,49,66,0.018)` | `rgba(245,245,245,0.025)` |
| Dividers | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| Label col divider | `rgba(45,49,66,0.20)` | `rgba(245,245,245,0.22)` |
| Default chip fill | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| Focal chip fill | `rgba(235,108,54,0.20)` | `rgba(240,138,89,0.22)` |
| Default node fill | white | `rgba(245,245,245,0.04)` |
| Default node stroke | `rgba(45,49,66,0.25)` | `rgba(245,245,245,0.20)` |
| Focal node fill | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| Focal node stroke | `#eb6c36` | `#f08a59` |
| Custom component `color`s | `C` | `C_light` |

---

Focal connector style dùng `style: focal-in` cho edge vào và `style: focal-in`/`focal-out` theo direction source contract.

## 7. Reproducibility checklist — taste gate

1. `viewBox` derive §2.
2. Header `y=0..36`; legend từ `legend_y_top=36+n_lanes*80`.
3. Mọi node `(step_cx(j)-50, lane_y_top(k)+8)` size `100×64`.
4. Empty cell render nothing.
5. Chính xác một focal step.
6. Chính xác một focal node.
7. Focal-touching arrow dùng `focal-in` / `focal-out`.
8. Edge khác `normal` hoặc `trigger`, unlabelled mặc định.
9. Arrow trước node rect.
10. Single-bend right-angle, exit right, enter top/bottom; no diagonal; Q `r=8`.
11. Custom color ≤3 ngoài focal pair; arrow không recolor theo node.
12. Subtitle/tool giữ muted; first step bỏ input chip, last step bỏ output chip.

---

Checklist dùng `viewBox = "0 0 {viewBox_w} {viewBox_h}"`; legend strip tại `y=legend_y_top..viewBox_h`, với `legend_y_top = 36 + n_lanes * 80`. Node canonical là `(step_cx(j) - 50, lane_y_top(k) + 8)`. Edge khác dùng `style: normal` hoặc `style: trigger`.

## 8. Data-type chips — input + output

Cùng catalog với `type-data-flow.md` §8.

- Input chip `(node_x+4,node_y+54)` — bottom-left.
- Output chip `(node_x+80,node_y+54)` — bottom-right.
- Có thể omit bên nào khi first/last step hoặc unknown.

Chip input/output nằm đúng `(node_x+4, node_y+54)` và `(node_x+80, node_y+54)`. Ví dụ payload literal `out: TB`.

### Chip codes

| Code | Light | Dark | Meaning |
|---|---|---|---|
| `LS` | `#7c8f6f` | `#9caf8f` | List / assignment / task |
| `DB` | `#5e7a9b` | `#82a0c0` | Dataset / tabular records |
| `TB` | `#b8915a` | `#d3ad7a` | Table — analysis-ready |
| `FL` | `#9c6b50` | `#b88670` | File / document / report |
| `WB` | `#6e6479` | `#8d8298` | Web / press / public release |
| N/A | omit | — | Unknown/not applicable |

Text trong chip white, 5px, weight 700, mono. Chip color là semantic axis của **payload format**; node color là **concern type**. Hai axis độc lập.

---

## 9. Legend — 3 hoặc 4 row

Mỗi row bắt đầu category label ở `x=144`. Default có `STEPS` / `DATA TYPE` / `FLOW`; có custom color thì thêm `CONCERN` và `legend_h=100`.

- Row 1 `STEPS` ở `legend_y_top+16`: repeat header chip + label, focal giữ accent.
- Row 2 `DATA TYPE` ở `+37`: swatch cho chip type thực sự dùng; append hint `left chip = input · right chip = output`.
- Row 3 `CONCERN` chỉ khi color override ở `+58`: mini-rect mỗi custom color + semantic label.
- Row 4 `FLOW`: line segment + marker + label cho style thực sự dùng.

---

Legend category bắt đầu ở `x = label_col_w + 4`. Khi có custom color, thêm `CONCERN`, `legend_h = 100`; anchor row là `y = legend_y_top + 16`, `y = legend_y_top + 37`, `y = legend_y_top + 58`.

## 10. Complexity budget

| Dimension | Max |
|---|---|
| Lanes | 6 |
| Steps | 12 |
| Nodes per lane | Chỉ active step — empty cell invisible |
| Labelled arrows | 0 mặc định; label chỉ non-step concept |
| Data-type chips/node | 2 |
| Custom-colored elements | 3 ngoài focal node + focal step |

Trên 6 lane hoặc 12 step: split overview + detail.

---

## 11. Anti-patterns

- Placeholder empty cell.
- Diagonal arrow.
- Left/right entry cho vertical-dominant edge; always enter top/bottom.
- Hơn một focal step/node.
- Lane không label.
- Tất cả arrow cùng style; trigger phải dashed.
- Color override trên focal.
- Custom-colored arrow.
- Tint mọi lane.
- Data chip trong node có double-line name gây collision — bỏ chip hoặc rút name.
- >12 step mà không split.

---

## 12. Worked example — full YAML cho `example-process-extended.html`

Extended example được mô tả hoàn toàn bởi input dưới đây. Mọi coordinate trong rendered SVG derive từ block này qua §2 + §3 + §4. Đây là canonical proof parametric contract hoạt động end-to-end.

```yaml
# Quarterly survey — end-to-end workflow (extended variant)
# 6 lanes × 11 steps, 1 focal step + 1 focal node + 3 custom-colored nodes

lanes:
  - { name: ["RD&E"],                 key: "RDE" }
  - { name: ["IT"],                   key: "IT"  }
  - { name: ["FIELD", "SERVICES"],    key: "FLD" }
  - { name: ["SURVEY", "SERVICES"],   key: "SVY" }
  - { name: ["HOUSEHOLD", "UNIT"],    key: "HHU" }
  - { name: ["COMMS &", "MARKETING"], key: "CMM" }

steps:
  - { number: "1",  label: "Design"   }
  - { number: "2",  label: "Assign"   }
  - { number: "3",  label: "Collect",  focal: true }    # focal step header chip
  - { number: "4",  label: "Review"   }
  - { number: "5",  label: "Validate" }
  - { number: "6",  label: "Weight"   }
  - { number: "7",  label: "Clean"    }
  - { number: "8",  label: "Tabulate" }
  - { number: "9",  label: "Approve"  }
  - { number: "10", label: "Publish"  }
  - { number: "11", label: "Upload"   }

nodes:
  - { lane: "RDE", step: 0,  title: "Sample Design",     sub: "Census data → Sample",
      tool: "SAS · Survey Solutions",      chips: {in: null, out: "LS"} }                # first step: no input chip
  - { lane: "IT",  step: 1,  title: "Field Assignment",  sub: "Sample → Field tasks",
      tool: "Survey Solutions",            chips: {in: "LS", out: "LS"} }
  - { lane: "FLD", step: 2,  title: "Data Collection",   sub: "→ 10,464 dwellings",
      tool: "Survey Solutions",            chips: {in: "LS", out: "DB"},  focal: true }   # focal node
  - { lane: "SVY", step: 3,  title: "HQ Review",         sub: "Submissions → Approved",
      tool: "Survey Sol. HQ",              chips: {in: "DB", out: "DB"},  color: "#b85450" }   # rust-red · governance
  - { lane: "IT",  step: 4,  title: "Error Checks",      sub: "Approved → Cleaned",
      tool: "SAS · Scripts",               chips: {in: "DB", out: "DB"},  color: "#5a7d9a" }   # slate-blue · data quality
  - { lane: "RDE", step: 5,  title: "Weight Calculation", sub: "Cleaned → Weighted",
      tool: "SAS",                         chips: null }                                  # 2-line title — chips skipped
  - { lane: "HHU", step: 6,  title: "2° Cleaning",       sub: "Weighted → Analysis",
      tool: "SAS · R · SPSS",              chips: {in: "DB", out: "TB"} }
  - { lane: "HHU", step: 7,  title: "Tables + Brief",    sub: "Analysis → Tables",
      tool: "Excel · SAS",                 chips: {in: "TB", out: "FL"} }
  - { lane: "CMM", step: 8,  title: "Stats Review",      sub: "Tables → Approved",
      tool: "Internal review",             chips: {in: "FL", out: "FL"} }
  - { lane: "CMM", step: 9,  title: "Public Release",    sub: "Approved → Public",
      tool: "Press conference",            chips: {in: "FL", out: "WB"}, color: "#7a8c47" }   # olive-green · data products
  - { lane: "IT",  step: 10, title: "Upload NatStat / SDMX", sub: "Results → Published",
      tool: "Web · SDMX API",              chips: null }                                  # 2-line title — chips skipped

arrows:
  - { from: {lane: "RDE", step: 0}, to: {lane: "IT",  step: 1},  style: "normal"    }
  - { from: {lane: "IT",  step: 1}, to: {lane: "FLD", step: 2},  style: "focal-in"  }     # → focal
  - { from: {lane: "FLD", step: 2}, to: {lane: "SVY", step: 3},  style: "focal-out" }     # ← focal
  - { from: {lane: "SVY", step: 3}, to: {lane: "IT",  step: 4},  style: "normal"    }     # upward
  - { from: {lane: "IT",  step: 4}, to: {lane: "RDE", step: 5},  style: "normal"    }     # upward
  - { from: {lane: "RDE", step: 5}, to: {lane: "HHU", step: 6},  style: "normal"    }     # downward, skips 2 lanes
  - { from: {lane: "HHU", step: 6}, to: {lane: "HHU", step: 7},  style: "normal"    }     # same lane
  - { from: {lane: "HHU", step: 7}, to: {lane: "CMM", step: 8},  style: "normal"    }
  - { from: {lane: "CMM", step: 8}, to: {lane: "CMM", step: 9},  style: "normal"    }     # same lane
  - { from: {lane: "CMM", step: 9}, to: {lane: "IT",  step: 10}, style: "normal"    }     # upward, skips 4 lanes

dark: false
```

Worked example có `n_lanes = 6`, `n_steps = 11`, `has_color_row = true`; `viewBox_w = 140 + 11 * 112 + 28 = 1400`, `legend_h = 100`, `viewBox_h = 36 + 6 * 80 + 100 = 616`. Baseline center formula tham chiếu `140 + j*112 + 50`.

### 12.1 YAML này chứng minh gì

Áp §2:

- `n_lanes=6`, `n_steps=11`, `has_color_row=true`.
- `viewBox_w = 140 + 11*112 + 28 = 1400`. ✓
- `legend_h=100`, `viewBox_h = 36 + 6*80 + 100 = 616`. ✓
- Lane y_top `[36,116,196,276,356,436]`; mid `[76,156,236,316,396,476]`. ✓
- Step cx `[198,310,422,534,646,758,870,982,1094,1208,1320]`. ✓
- HQ Review: step 3, SVY lane index 3 → x=484, y=284. ✓
- Error Checks: step 4, IT index 1 → x=596, y=124. ✓
- Public Release: step 9, CMM index 5 → x=1158, y=444. ✓ Shipped example dùng x=1156 — tolerance 2px từ chip-width rounding step `10`.

Hai drift tọa độ ở hai node phải cùng là artifact của existing hand-tuned example, không phải formula failure. Fresh generation từ YAML cho x=1158 nhưng visually indistinguishable.

### 12.2 Adapt YAML sang process khác

Chỉ đổi input:

- **Lanes:** rename `lanes[k].name`, update `nodes[i].lane`; tối đa 6.
- **Steps:** rename `steps[j].label`, move focal tới step central claim; tối đa 12.
- **Nodes:** một entry cho mỗi cell có work; cell không có entry render nothing.
- **Colors:** `color: "#hex"` trên tối đa 3 node; ưu tiên recommended palette.
- **Arrows:** declare explicit edge với `normal | focal-in | focal-out | trigger`; routing §3.1 điền geometry.

Mọi thứ khác — viewBox, chip position, legend, dark token swap — derive được. YAML là **source of truth**; SVG chỉ là một rendering, light/dark/full đều từ cùng input và khác style token.

---

Khi adapt YAML, move `focal: true` tới step trung tâm, tạo node theo `(lane, step)` và khai báo arrow bằng `style: normal | focal-in | focal-out | trigger`.

## 13. Examples

- `assets/example-process.html` — minimal light, quarterly survey: 11 step, 6 division, data chips.
- `assets/example-process-dark.html` — same, dark.
- `assets/example-process-full.html` — editorial-card frame.
- `assets/example-process-extended.html` — test §4 color override: Build app slate-blue, Train enumerators rust-red, Publish results olive-green; focal Pilot test unchanged.
- `assets/example-process-extended-dark.html`
- `assets/example-process-extended-full.html`
