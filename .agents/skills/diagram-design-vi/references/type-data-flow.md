# Data Flow

**Phù hợp nhất cho:** trực quan hoá cách data di chuyển qua pipeline *giữa các organisational role* — ai khởi tạo, ai xử lý, ai publish, ai consume. Use case chuẩn là data platform nhiều role (Admin → Engineers → Scientists → Consumers) với 4–6 process step. Dùng khi người đọc cần hiểu **ai làm gì ở mỗi stage**, không chỉ technical component.

Ưu tiên **Swimlane** chuẩn cho cross-functional business process (HR approval, support ticket). Dùng **Data flow** khi chủ đề là data pipeline có typed payload (raw file, table, report) và role-scoped access boundary.

Type này **parametric** — input schema ở §1 điều khiển mọi coordinate qua formula §2. Hai lần generate từ cùng input phải tạo SVG giống nhau về mặt thị giác.

---

## 1. Inputs — parameter contract

```yaml
lanes:                              # 1..4 horizontal swimlanes (top to bottom)
  - { name: ["DATA", "ADMINS"],     key: "ADM" }
  - { name: ["DATA", "ENGINEERS"],  key: "ENG" }
  - { name: ["DATA", "SCIENTISTS"], key: "SCI" }
  - { name: ["DATA", "CONSUMERS"],  key: "CON" }

steps:                              # 1..6 columns (left to right)
  - { number: "01", label: "COLLECT" }
  - { number: "02", label: "STORE" }
  - { number: "03", label: "TRANSFORM" }
  - { number: "04", label: "ANALYZE",  focal: true }   # focal step header chip — accent fill
  - { number: "05", label: "PUBLISH" }

nodes:                              # explicit per-cell entries; empty cells render nothing
  - { lane: "ADM", step: 0, title: "Project Setup",   sub: "create · assign roles",     tool: "Platform console" }
  - { lane: "ADM", step: 1, title: "Access Control",  sub: "bucket policies · LDAP",    tool: "MinIO · LDAP console",
      color: "#b85450" }            # tinted rust-red to flag governance/identity concern
  - { lane: "ENG", step: 0, title: "Source Ingest",   sub: "ext. sources → raw",        tool: "NiFi · API · SFTP",
      chips: {in: "WB", out: "DB"} }                    # web payload in, dataset out
  - { lane: "ENG", step: 1, title: "Raw Store",       sub: "raw landing zones",         tool: "MinIO raw",
      chips: {in: "DB", out: "DB"} }                    # raw stays raw inside the landing zone
  - { lane: "ENG", step: 2, title: "Clean & Stage",   sub: "raw → staging → anon",      tool: "NiFi · Trino",
      chips: {in: "DB", out: "TB"} }                    # raw dataset → analysis-ready table
  - { lane: "SCI", step: 3, title: "Explore & Model", sub: "anon data → insights",      tool: "JupyterHub · Trino",
      chips: {in: "TB", out: "FL"}, focal: true }       # focal — table in, file/report out
  - { lane: "SCI", step: 4, title: "Publish Findings", sub: "models → dashboards",      tool: "Superset · Reports",
      chips: {in: "FL", out: "FL"} }                    # report in, report out (pass-through to publish)
  - { lane: "CON", step: 4, title: "Query Insights",   sub: "aggregated views",         tool: "Trino (read-only)",
      chips: {in: "TB", out: "TB"} }                    # consumers read tables, hand off tables

arrows:                             # explicit edges; styles bind to topology (see §3)
  - { from: {lane: "ADM", step: 0}, to: {lane: "ADM", step: 1}, style: "muted" }
  - { from: {lane: "ADM", step: 0}, to: {lane: "ENG", step: 0}, style: "trigger" }   # dashed governance
  - { from: {lane: "ADM", step: 1}, to: {lane: "ENG", step: 1}, style: "trigger" }
  - { from: {lane: "ENG", step: 0}, to: {lane: "ENG", step: 1}, style: "muted" }
  - { from: {lane: "ENG", step: 1}, to: {lane: "ENG", step: 2}, style: "muted" }
  - { from: {lane: "ENG", step: 2}, to: {lane: "SCI", step: 3}, style: "accent",     # focal cross-role
      label: "anon data" }
  - { from: {lane: "SCI", step: 3}, to: {lane: "SCI", step: 4}, style: "muted" }
  - { from: {lane: "SCI", step: 4}, to: {lane: "CON", step: 4}, style: "link" }     # teal: published

dark: false
```

**Reserved field semantics:**
- `lanes[k].key` — text role chip 3 ký tự (ví dụ `ADM`, `ENG`, `SCI`, `CON`). Dùng trong mọi node ở lane đó.
- `lanes[k].name` — lane label hai dòng; cả hai dùng uppercase `eyebrow` role.
- `steps[j].focal: true` — chính xác **một** step được khai báo. Header chip render accent.
- `nodes[i].focal: true` — chính xác **một** node được khai báo. Render accent border (§5).
- `nodes[i].chips` — data-type chip của node. Chấp nhận hai dạng:
  - **Object form (ưu tiên):** `{in: "<CODE>", out: "<CODE>"}` — semantic input/output rõ ràng. Mỗi bên optional.
  - **Array form:** `["<INPUT_CODE>", "<OUTPUT_CODE>"]` — item đầu là input, item hai là output.
  - Code từ §8 (`WB`, `DB`, `TB`, `FL`, `LS`). Position **cố định**: input chip ở bottom-**left**, output chip ở bottom-**right**.
- `nodes[i].color` — optional **per-node color override**. Chấp nhận mọi `"#hex"` hợp lệ; palette §4 được khuyến nghị nhưng không bắt buộc. Mỗi node có thể có color riêng.

---

## 2. Layout formulas — deterministic geometry

```
label_col_w      = 140
step_slot_w      = 112
right_pad        = 28
n_steps          = len(steps)
n_lanes          = len(lanes)

# Canvas
viewBox_w        = label_col_w + n_steps * step_slot_w + right_pad   # 5 steps → 728
header_h         = 36
lane_h           = 80
has_color_row    = any(node.color or step.color or lane.color in inputs)
legend_h         = 100 if has_color_row else 80                      # 4 rows when colors are present
viewBox_h        = header_h + n_lanes * lane_h + legend_h            # 4 lanes, no colors → 436; with colors → 456

# Header strip (top)
header_y         = 0                                                  # ends at header_h = 36
step_chip_y      = 6                                                  # 16-px chip at y=6..22
step_label_y     = 29                                                 # text line below chip

# Lane positions
lane_y_top(k)    = header_h + k * lane_h                              # 36, 116, 196, 276
lane_y_mid(k)    = lane_y_top(k) + lane_h/2                           # 76, 156, 236, 316
lane_label_x     = label_col_w / 2                                    # 70

# Step / node center x
step_cx(j)       = label_col_w + j * step_slot_w + step_slot_w/2      # 196, 308, 420, 532, 644

# Nodes
node_w           = 100
node_h           = 64
node_x(j)        = step_cx(j) - node_w/2                              # 146, 258, 370, 482, 594
node_y(k)        = lane_y_top(k) + 8                                  # 44, 124, 204, 284

# Legend strip (bottom)
legend_y_top     = header_h + n_lanes * lane_h                        # 356
legend_row_y     = [legend_y_top + 16, legend_y_top + 37, legend_y_top + 59]
                                                                      # 372, 393, 415
```

### 2.1 Background structure

- Paper fill toàn viewBox.
- Dot pattern: grid 22×22, `circle r=0.8`, `fill ink @ 0.10`.
- Alternating lane tint: lane index 0, 2, … nhận fill `ink @ 0.018`.
- Lane divider: horizontal hairline tại mỗi `lane_y_top(k)` và `legend_y_top`, stroke `ink @ 0.12`, width 0.8.
- Border phải của label column: vertical hairline tại `x = label_col_w`, từ `y = header_h` tới `y = legend_y_top`.

### 2.2 Step header chip

Mỗi step `j`:

```
chip_x(j)        = step_cx(j) - 16        # 16×16 chip
chip_y           = 6
chip_w           = 32
chip_h           = 16
chip_rx          = 8                       # pill-shaped
number_anchor    = (step_cx(j), 14)
label_anchor     = (step_cx(j), 29)
```

Default fill: `ink @ 0.12`, number text ink, label text muted. Focal fill: `accent @ 0.20`, number + label accent. Per-step `color` override (§4) đổi fill thành `rgba(C, 0.20)` và text fill thành `C`.

### 2.3 Lane label

Label role `eyebrow` hai dòng, uppercase, muted:
- Line 1 tại `(lane_label_x, lane_y_mid(k) - 4)`
- Line 2 tại `(lane_label_x, lane_y_mid(k) + 8)`

Per-lane `color` override (§4) đổi label fill thành `C` và lane tint thành `rgba(C, 0.04)` thay `ink @ 0.018`.

### 2.4 Node content layout trong rect 100×64

```
role_chip          rect 18×10 at (node_x+4, node_y+4),  rx=3
role_chip_text     centered at (node_x+13, node_y+9), eyebrow role, font-size=6, weight=600
title              centered at (step_cx(j), node_y+23), node-name role, font-size=9
sub                centered at (step_cx(j), node_y+35), sublabel role, font-size=6.5, muted
tool               centered at (step_cx(j), node_y+47), sublabel role, font-size=6.5, soft
data chip IN       rect 16×8 at (node_x+4,   node_y+54), rx=3      # payload type entering the node
data chip OUT      rect 16×8 at (node_x+80,  node_y+54), rx=3      # payload type leaving the node
```

Empty cell không có node entry render **nothing** — không placeholder rect, role chip hay label.

---

## 3. Arrow rule (bắt buộc)

Bốn style, khóa theo topology. Connector được vẽ **trước** mọi node rect.

| `style` | Stroke | Width | Dash | Marker | Khi bắt buộc |
|---|---|---|---|---|---|
| `muted` | `muted` | 1.0 | — | `arr-muted` | Data hand-off chuẩn giữa step hoặc trong lane |
| `trigger` | `muted` | 1.0 | `4,3` | `arr-muted` | Governance trigger; admin action enable downstream work; không label |
| `accent` | `accent` | 1.2 | — | `arr-accent` | Focal cross-role handoff; **chính xác một mỗi diagram**, có label |
| `link` | `link` | 1.0 | — | `arr-link` | Published / externally-consumed output |

**Defs block** bắt buộc, ba marker:

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="0.8" fill="{ink @ 0.10}"/>
  </pattern>
  <marker id="arr-muted"  markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{muted}"/></marker>
  <marker id="arr-accent" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{accent}"/></marker>
  <marker id="arr-link"   markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{link}"/></marker>
</defs>
```

### 3.1 Routing rule — không thương lượng

- **Single-bend:** horizontal-first rồi vertical. Exit từ **right edge**; enter từ **left** khi same-lane horizontal hoặc **top/bottom** khi cross-lane vertical.
- **Không diagonal.** Bend dùng Q-bezier radius 8px.
- **Same-step cross-lane vertical:** line trực tiếp giữa `(step_cx(j), lane_y_top(k_to)−12)` và `(step_cx(j), lane_y_top(k_to))`.
- **Cross-lane cross-step focal:** exit right, chạy ngang qua source right edge tới corridor x trước target step rồi drop vertical.
- **Label:** chỉ `accent` arrow có label. Dùng opaque paper-filled rect mask, clear 6px phía sau text. Arrow khác không label.
- **Z-order:** emit mọi arrow trước node rect.

---

## 4. Component color override

Node, lane hoặc step có thể khai báo `color: "#hex"`. Rule này mirror high-level §3.4 và dp-integration §4.

### 4.1 Per-node `color`

| Element | Light | Dark |
|---|---|---|
| Container fill (`rect`) | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| Container stroke | `rgba(C, 0.35)` width 1 | `rgba(C_light, 0.45)` |
| Role chip fill | `rgba(C, 0.18)` | `rgba(C_light, 0.22)` |
| Role chip text | `C` | `C_light` |
| Title text | `C` | `C_light` |
| Sub-label | **không đổi** (muted) | **không đổi** |
| Tool label | **không đổi** (soft) | **không đổi** |
| Data-type chips | **không đổi** | **không đổi** |
| Arrow chạm node | **không đổi** — topology-driven | **không đổi** |

`C_light` = cùng hex lightened ~15% cho dark-mode contrast, ví dụ `#b85450` → `#d97a78`.

### 4.2 Per-step `color`

Đổi step header chip fill thành `rgba(C, 0.20)` và number + label thành `C`. Legend step tương ứng dùng cùng color.

### 4.3 Per-lane `color`

Đổi lane stripe tint thành `rgba(C, 0.04)` và lane label thành `C`. Dùng tiết chế; lane tint rất dễ over-apply.

### 4.4 Rule

- **Không áp dụng trên focal node / focal step.** Accent thắng; `color` trên focal bị ignore.
- **Không áp dụng lên arrow.** Arrow topology-driven. Muốn edge màu khác thì chọn `style` §3.
- **Tối đa 3 custom-colored element** mỗi diagram (node + lane + step), ngoài focal pair.
- **Subtitle/tool label giữ muted.** Chỉ primary identity (border + role chip + title + icon) mang color signal.

### 4.5 Semantic palette khuyến nghị

- `#b85450` rust-red — Security / Identity / Governance
- `#5a7d9a` slate-blue — Observability / Quality
- `#7a8c47` olive-green — Governance / Lineage
- `#8c6d3f` warm-brown — Backup / DR / Archive

---

## 5. Focal rule

Diagram được xây quanh **một cross-role handoff**. Ba focal slot, mỗi slot chính xác một entry:

- **Một focal step** (`steps[j].focal: true`) — thường là analytical pivot. Header + legend chip accent.
- **Một focal node** (`nodes[i].focal: true`) — node *nhận* focal handoff. Accent border + accent role chip + ink title.
- **Một focal arrow** (`arrows[i].style: "accent"`) — cross-role handoff vào focal node. Solid accent + short payload label.

Nếu focal slot nào có zero hoặc >1 declaration, **dừng và hỏi người dùng**.

---

Các focal slot giữ đúng literal nguồn: **một focal step** (`steps[j].focal: true`), **một focal node** (`nodes[i].focal: true`), và focal arrow có short payload label, ví dụ `anon data`.

## 6. Dark mode

| Token | Light | Dark |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Soft | `soft` | `rule-solid` |
| Accent | `accent` | `accent` |
| Link | `link` | `link` |
| Dot pattern | `ink @ 0.10` | `paper @ 0.10` |
| Lane tint | `ink @ 0.018` | `paper @ 0.025` |
| Dividers | `ink @ 0.12` | `paper @ 0.12` |
| Default chip fill | `ink @ 0.12` | `paper @ 0.12` |
| Focal chip fill | `accent @ 0.20` | `accent @ 0.22` |
| Default node fill | `paper` | `paper @ 0.04` |
| Default node stroke | `ink @ 0.25` | `paper @ 0.20` |
| Focal node fill | `accent @ 0.07` | `accent @ 0.12` |
| Focal node stroke | `accent` | `accent` |
| Custom component colors | `C` | `C_light` |

---

## 7. Reproducibility checklist

1. `viewBox = "0 0 {viewBox_w} {viewBox_h}"` từ `n_steps`, `n_lanes` theo §2.
2. Header strip `y=0..36`; legend strip từ `legend_y_top` tới `viewBox_h`.
3. Mọi node tại `(step_cx(j) - 50, lane_y_top(k) + 8)`, size `100×64`.
4. Empty cell render nothing.
5. Chính xác **một** focal step.
6. Chính xác **một** focal node.
7. Chính xác **một** focal arrow `style: accent`, có label + paper mask.
8. Arrow khác không label.
9. Mọi arrow emit trước node rect.
10. Single-bend routing only; không diagonal; Q-bezier `r=8`.
11. Custom component color ≤3 ngoài focal pair; arrow không recolor bởi component `color`.
12. Subtitle/tool label giữ muted dù component có `color`.

---

Trong checklist hình học, legend strip chạy tại `y=legend_y_top..viewBox_h`, với `legend_y_top = 36 + n_lanes * 80`.

## 8. Data-type chip reference — input + output

Badge nhỏ `16×8 rx=3` ở bottom mỗi node; position **không thương lượng**:
- **Input chip** `(node_x+4, node_y+54)` — bottom-**left**.
- **Output chip** `(node_x+80, node_y+54)` — bottom-**right**.

Mỗi chip có thể omit. Đọc input → output sẽ cho thấy payload transformation qua từng hand-off.

### Chip codes

| Code | Color | Meaning |
|---|---|---|
| `WB` | `#6e6479` (mauve) | Web / Public data |
| `DB` | `#5e7a9b` (steel-blue) | Dataset / Raw file |
| `TB` | `#b8915a` (amber) | Table / Analysis-ready |
| `FL` | `#9c6b50` (sienna) | File / Report / Export |
| `LS` | `#4a7c59` (forest) | Live stream / Event |

Text trong chip: white, `eyebrow` role 5px, weight 700.

Data-type chip color là **semantic axis riêng** với per-node color override (§4): chip mô tả *payload format*, node color mô tả *concern type*. Không conflated; một node có thể cùng lúc có `out: TB` amber chip và rust-red border.

---

## 9. Legend — strip 3 hoặc 4 row

Mỗi row có category label tại `x=144`. Default **3 row** (`STEPS` / `DATA TYPE` / `FLOW`); nếu có `color` override, thêm row `CONCERN` và tăng `legend_h=100`.

- **Row 1 — `STEPS`** tại `legend_y_top + 16`: lặp header chip + label. Focal step giữ accent.
- **Row 2 — `DATA TYPE`** tại `legend_y_top + 37`: swatch cho chip type thực sự dùng. Thêm sub-hint muted: `left chip = input · right chip = output`.
- **Row 3 — `CONCERN`** chỉ khi color override: `legend_y_top + 58`; mini-rect cho custom color + semantic label. Focal accent swatch cũng hiển thị để thấy các colored axis cạnh nhau.
- **Row 4 — `FLOW`** là row cuối; line segment + marker + label cho arrow style thực sự dùng.

Legend item nằm horizontal trong mỗi row; không stack dọc trong box.

---

Khi có color override, thêm row `CONCERN`, đặt `legend_h` thành 100 và suy ra `viewBox_h = header_h + n_lanes·80 + 100`. Các row dùng đúng anchor `y = legend_y_top + 16`, `y = legend_y_top + 37` và `y = legend_y_top + 58`; hint dùng role `sublabel`. Semantic label mẫu giữ nguyên `Identity · Governance` và `Data Quality · Observability`.

## 10. Complexity budget

| Dimension | Max |
|---|---|
| Lanes (roles) | 4 |
| Steps | 6 |
| Nodes per lane | Nodes = active steps only — empty cells invisible |
| Labelled arrows | 1 (focal accent only) |
| Data-type chips per node | 2 |
| Custom-colored elements (§4) | 3 ngoài focal node + focal step |

Trên 4 lane hoặc 6 step: split thành hai diagram.

---

## 11. Anti-pattern

- **Placeholder empty cell** — role không tham gia step thì để trống hoàn toàn.
- **Hơn một labelled arrow** — chỉ focal cross-role handoff có label.
- **Diagonal arrow** — horizontal-first rồi vertical, single right-angle bend.
- **`title` role cho node title** — node dùng `node-name`; chỉ page `<h1>` dùng `title`.
- **Accent hơn một node, một step, một arrow** — focal = one+one+one max.
- **`node-name` role cho role label** — lane label luôn uppercase `eyebrow`.
- **`color` override trên focal** — ignored; accent thắng.
- **Custom-colored arrow** — topology-driven.
- **Lane tint over-applied** — áp dụng ≤1 lane.

---

## 12. Ví dụ

- `assets/example-data-flow.html` — minimal light.
- `assets/example-data-flow-dark.html` — dark skin.
- `assets/example-data-flow-full.html` — editorial-card frame.
- `assets/example-data-flow-extended.html` — thử color override với Access Control rust-red và Clean & Stage slate-blue; focal Analyze + Explore & Model + anon-data arrow không đổi.
- `assets/example-data-flow-extended-dark.html` — extended dark.
- `assets/example-data-flow-extended-full.html` — extended full.
