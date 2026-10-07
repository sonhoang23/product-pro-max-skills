# High-Level

**Phù hợp nhất cho:** overview end-to-end của data stack — ingestion → storage → query → analytics → visualization — được deploy trên container orchestrator (Kubernetes, ECS, Nomad). Kết hợp phase chevron banner, deployment boundary, orchestration bar, identity footer và, tuỳ chọn, một vertical chevron strip bên phải cho các cross-cutting concern (Orchestration, Security, Observability).

Type này là **parametric**. Diagram được xác định hoàn toàn bởi một danh sách input nhỏ (chevron, source, component, connection). Các công thức bên dưới xác định chính xác từng shape sẽ nằm ở đâu từ các input đó — hai lần generate với cùng input phải tạo SVG giống nhau về mặt hình học.

---

## 1. Input — contract tham số

Trước khi vẽ, thu thập các input này từ người dùng hoặc nhận chúng dưới dạng YAML/JSON. Mọi thứ trong reference này đều được suy ra từ input. Không tự nghĩ geometry trong lúc vẽ.

```yaml
chevrons:                       # ordered left → right; reserved names auto-promote to vertical
  - { name: "Data sources",         columns: 1 }
  - { name: "Ingestion",            columns: 1 }
  - { name: "Storage",              columns: 1 }
  - { name: "Transformation",       columns: 1 }
  - { name: "Visualization",        columns: 1 }
  - { name: "Orchestration",        vertical: true }                     # reserved → pairs with the bar
  - { name: "Security",             vertical: true, color: "#b85450" }   # tinted to match the Identity bar below
  - { name: "Observability",        vertical: true }                     # reserved → pairs with crosscut #2

sources:                        # external; rendered in the dashed zone on the left
  - { name: "PostgreSQL", type: "db",     connects_to: ["NiFi"] }
  - { name: "SFTP drop",  type: "ftp",    connects_to: ["NiFi"] }
  - { name: "Web forms",  type: "web",    connects_to: ["NiFi"] }
  - { name: "Legacy",     type: "legacy", connects_to: ["NiFi"] }

components:                     # inside the cluster, plus bars and cross-cutting rows
  - { name: "NiFi",       chevron: "Ingestion",      kind: node,          icon: nifi,     role: "COLL"  }
  - { name: "MinIO",      chevron: "Storage",        kind: node,          icon: minio,    role: "STORE", focal: true }
  - { name: "Trino",      chevron: "Storage",        kind: node,          icon: trino,    role: "VIRT"  }
  - { name: "Notebooks",  chevron: "Transformation", kind: node,          icon: jupyter,  role: "ANLZ"  }
  - { name: "Superset",   chevron: "Visualization",  kind: node,          icon: superset, role: "DASH" }
  - { name: "Airflow",    chevron: "Orchestration",  kind: bar,           icon: airflow,    subtitle: "Apache Airflow" }
  - { name: "Identity",   chevron: "Security",       kind: cross-cutting, icon: keycloak,   subtitle: "Keycloak · LDAP · OIDC",     color: "#b85450" }
  - { name: "Monitoring", chevron: "Observability",  kind: cross-cutting, icon: prometheus, subtitle: "Prometheus · Grafana · Loki" }

connections:                    # explicit edges; focal-touching ones become accent automatically
  - { from: "NiFi",    to: "MinIO",                style: "primary" }
  - { from: "NiFi",    to: "Trino",                style: "secondary" }
  - { from: "MinIO",   to: "Notebooks",            style: "primary" }
  - { from: "Trino",   to: "MinIO",                style: "query" }   # read-back (dashed)
  - { from: "Notebooks", to: "Superset",           style: "secondary" }
  - { from: "Airflow", to: ["NiFi", "Trino", "Notebooks"], style: "trigger" }

focal: "MinIO"                  # exactly one; defaults to first kind=node under "Storage"
dark: false
```

**Tên chevron reserved** — luôn vertical kể cả khi bỏ `vertical: true`: `Orchestration`, `Security`, `Observability`, `Governance`, `Backup`.

**Giá trị `kind` reserved:**
- `node` — box tiêu chuẩn bên trong cluster (mặc định).
- `bar` — horizontal strip span phần trên của cluster. Thường chỉ có một (Orchestration); xem pairing rule ở §5.
- `cross-cutting` — horizontal strip span body width, dừng trước strip margin và stack bên dưới cluster. **Cho phép zero hoặc nhiều hơn**; mỗi bar stack cách bar trước 44px (§2.5) và pair 1:1 với một vertical chevron (§5).

**`color` tuỳ chọn** cho từng component, dạng hex string: tint container và content của component nhưng không đổi connector. Xem §3.4. Dùng tiết chế — custom color là semantic flag, ví dụ đỏ = security concern, không phải decoration.

**Giá trị `type` của source** → icon mapping, dùng `references/primitive-icons.md`:
- `db` → `database`
- `ftp` → `bucket` hoặc upload arrow
- `web` → `internet`
- `legacy` → `server`
- `api` → `api`
- Chấp nhận cả bất kỳ icon name explicit nào trong `primitive-icons.md`.

---

## 2. Công thức layout — geometry deterministic

Mọi coordinate dưới đây đều được suy ra từ input. **Không hardcode number trong example nếu number đó không được biện minh ở đây.**

### 2.1 Canvas

```
has_vertical       = any(c.vertical or c.name in reserved_names for c in chevrons)
right_strip_w      = 28  if has_vertical else 0
strip_margin       = 8   if has_vertical else 0   # gap between body and right strip
effective_w        = 1000 - right_strip_w - strip_margin     # 1000 or 964

n_cross            = count of components with kind == "cross-cutting"
strip_y_bot        = max(428, 388 + n_cross * 44 - 4)        # extends to last crosscut row
viewBox_h          = max(540, strip_y_bot + 112)             # 112 reserved for legend
viewBox            = f"0 0 1000 {viewBox_h}"
```

Mọi horizontal element — chevron banner, cluster, orchestration bar, identity/cross-cutting bar — kết thúc tại `effective_w`. Right strip nằm ở `x = 1000 - right_strip_w` (= 972). Band 8px giữa chúng là khoảng thở trực quan — không đặt content vào đó.

`viewBox_h` tăng khi khai báo hơn một cross-cutting bar: 1 crosscut → 540, 2 → 600 — hoặc 584 nếu muốn tight; rule làm tròn lên multiple of 20 tiếp theo để grid sạch.

### 2.2 Horizontal chevron banner

```
y_banner           = 4
h_banner           = 28
horizontals        = [c for c in chevrons if not c.vertical and c.name not in reserved_names]
sum_columns        = sum(c.columns for c in horizontals)
base_unit          = floor_to_4(effective_w / sum_columns)        # multiple of 4
widths             = [max(120, base_unit * c.columns) for c in horizontals]
widths[-1]         += effective_w - sum(widths)                   # trailing absorbs remainder
x_boundaries       = cumulative_sum([0] + widths)                 # length sum_columns+1
chevron_cx(C)      = (x_boundaries[index(C)] + x_boundaries[index(C)+1]) / 2
```

**Polygon shape:**
- First, trái nhất: `(x0,4) (x1-12,4) (x1,18) (x1-12,32) (x0,32)`
- Middle: `(x0,4) (x1-12,4) (x1,18) (x1-12,32) (x0,32) (x0+12,18)`
- Last, phải nhất: `(x0,4) (effective_w,4) (effective_w,32) (x0,32) (x0+12,18)`

Fill xen kẽ `#2d3142` / `#3d4460` ở light mode hoặc `#3d4460` / `#4a5270` ở dark mode. Label dùng mono màu paper, `font-size=7`, `letter-spacing=0.14em`, `text-anchor=middle`, centered tại `chevron_cx, 21`.

**Color override** cho từng chevron, cả horizontal và vertical: chevron có thể khai báo `color: "#hex"` để thay alternation fill cho riêng chevron đó. Dùng để flag một phase pair với custom-colored component, ví dụ chevron `Security` đỏ khi Identity bar dùng `color: "#b85450"`. Quy tắc:

- Override chỉ áp dụng vào polygon fill. Label luôn paper-colored — không recolor chevron label.
- Alternation index không shift; neighbour giữ natural fill dù có thể xuất hiện hai chevron liền nhau cùng fill. Không cố “sửa” — override phải hiếm, ≤2 mỗi diagram.
- Ở dark mode, dùng cùng hex trừ khi contrast với paper label kém; khi đó chọn shade tối hơn cho dark mode và ghi thành field `color_dark` trên chevron.
- Chevron color override độc lập với color của paired component, nhưng dùng cùng hex trên chevron + bar là convention để toàn column đọc như một concern.

### 2.3 Source zone — dashed, external

```
sources_x          = 4
sources_y          = 40
sources_w          = x_boundaries[1] - 8           # width of the first chevron, minus 4px gutter each side
sources_h          = 336
```

Nét viền: `rgba(45,49,66,0.20)`, `stroke-width=0.8`, `stroke-dasharray=6,3`, `rx=6`. Fill của zone: `rgba(45,49,66,0.02)`.

### 2.4 Cluster boundary — solid

```
cluster_x          = x_boundaries[1] + 4           # starts at end of source zone + 4px gutter
cluster_y          = 40
cluster_w          = effective_w - cluster_x       # extends to right strip / canvas edge
cluster_h          = 336
```

Stroke: `rgba(45,49,66,0.18)`, `stroke-width=1.2`, `rx=8`. Fill: `rgba(45,49,66,0.02)`. K8s icon + label tại `(cluster_x + 16, 352)` cho icon và `(cluster_x + 40, 362)` cho text.

### 2.5 Cross-cutting bar — identity, observability, …

Zero hoặc nhiều component `kind: cross-cutting` stack bên dưới cluster. Mỗi component có row 40px riêng với gap 4px.

```
crosscuts          = [c for c in components if c.kind == "cross-cutting"]   # ordered as declared
cross_x            = 4
cross_y(k)         = 388 + k * 44                  # 388, 432, 476, …
cross_w            = effective_w - 4               # spans body width, stops at the strip margin
cross_h            = 40
```

Stroke `rgba(45,49,66,0.20)`, `stroke-width=0.8`, `rx=6`; fill `rgba(45,49,66,0.05)`. Icon tại `(16, cross_y(k) + 10)`, name centered tại `(effective_w / 2, cross_y(k) + 22)`, subtitle tại `(effective_w / 2, cross_y(k) + 34)`.

Các cross-cutting *concern* reserved mang tính thông tin; người dùng có thể đặt tên bar thực tế tuỳ ý:
- **Identity / Security** — Keycloak, LDAP/AD, Okta, Auth0, OIDC provider
- **Observability** — Prometheus + Grafana, Datadog, OpenTelemetry, Loki
- **Backup / DR** — Velero, Restic, snapshot orchestrator
- **Governance / Lineage** — OpenMetadata, DataHub, Apache Atlas
- **Secrets / config** — Vault, Sealed Secrets, External Secrets

Mỗi cross-cutting bar pair 1:1 với một vertical chevron trong right strip (§5).

### 2.6 Orchestration bar component — trong cluster

```
bar_x              = cluster_x + 12
bar_y              = 52
bar_w              = cluster_w - 24
bar_h              = 44
```

Stroke `rgba(45,49,66,0.18)`, `stroke-width=0.8`, `rx=4`; fill `rgba(45,49,66,0.05)`. Tool icon ở far right (`bar_x + bar_w - 50, 58`); name centered tại `(bar_x + bar_w/2, 71)`; subtitle tại `(bar_x + bar_w/2, 84)`.

### 2.7 Component node — trong cluster

```
node_w             = 152
node_h             = 80                            # focal same height, accent border
node_cx(N)         = chevron_cx(N.chevron)         # ← non-negotiable
node_x(N)          = node_cx(N) - node_w/2
```

Nếu một chevron có K node được assign, stack vertical:

```
first_top_y        = 120 if any bar in this column else 64
gap                = 16
row_top(k)         = first_top_y + k * (node_h + gap)   # k = 0..K-1
```

**Focal node:** `fill="rgba(235,108,54,0.08)"`, `stroke="#eb6c36"`, `stroke-width=1.2`. Title text dùng accent. Node khác: white fill, `stroke=rgba(45,49,66,0.25)`, `stroke-width=1`.

Role badge ở top-left tại `(node_x+8, node_y+6)`, cao 12. Icon top-right tại `(node_x+node_w-32, node_y+6)`, 24×24, monochrome qua `currentColor`. Name centered tại `(node_cx, node_y+44)` size 11 sans semibold. Subtitle tại `(node_cx, node_y+56)` size 8 mono `muted`.

### 2.8 Source node — trong dashed zone

```
src_node_w         = sources_w - 8
src_node_h         = 64                            # uniform; chosen to fit ≤ 4 sources
src_node_x         = sources_x + 4
src_first_top_y    = 60
src_gap            = 16
src_row_top(k)     = src_first_top_y + k * (src_node_h + src_gap)
```

Dùng cùng pattern role-badge / icon / name / subtitle như cluster node — icon tại `src_node_x+54, row_top(k)+6`; name centered tại `src_node_x+src_node_w/2, row_top(k)+42`; subtitle ở line dưới. Role badge text: `EXT`. Cap 4 source; nhiều hơn thì split thành diagram khác.

### 2.9 Right strip — vertical chevron

```
strip_x            = 1000 - right_strip_w       # 972 when present
strip_w            = 28
verticals          = [c for c in chevrons if c.vertical or c.name in reserved_names]
strip_y_top        = 40
strip_y_bot        = max(428, 388 + n_cross * 44 - 4)   # extends to last crosscut row (see §2.1)
strip_h_total      = strip_y_bot - strip_y_top
heights            = [floor_to_4(strip_h_total / len(verticals))] * len(verticals)
heights[-1]       += strip_h_total - sum(heights)       # last absorbs remainder
```

Ví dụ:
- 2 vertical — Orchestration + Security — 1 crosscut → `heights = [192, 196]`, layout `[40..232, 232..428]`.
- 3 vertical — Orchestration + Security + Observability — 2 crosscut → `strip_y_bot = 472`, `strip_h_total = 432`, `heights = [144, 144, 144]`, layout `[40..184, 184..328, 328..472]`.

Adjacent edge chia sẻ cùng y, không gap, giống horizontal chevron chia sẻ x ở boundary.

**Polygon shape** theo flow top-to-bottom, mirror horizontal §2.2:
- First, topmost: flat top, point ở bottom — `(strip_x, y0) (strip_x+strip_w, y0) (strip_x+strip_w, y1-12) (strip_x+strip_w/2, y1) (strip_x, y1-12)`
- Middle: notch trên, point dưới — `(strip_x, y0) (strip_x+strip_w/2, y0+12) (strip_x+strip_w, y0) (strip_x+strip_w, y1-12) (strip_x+strip_w/2, y1) (strip_x, y1-12)`
- Last, bottommost: notch trên, flat bottom — `(strip_x, y0) (strip_x+strip_w/2, y0+12) (strip_x+strip_w, y0) (strip_x+strip_w, y1) (strip_x, y1)`

Fill xen kẽ `#2d3142` / `#3d4460`, cùng palette horizontal. Label dùng mono paper-colored `font-size=7`, `letter-spacing=0.14em`, **rotate −90°**, anchor tại `(strip_x + strip_w/2, (y0+y1)/2)`.

Vertical chevron tuân theo per-chevron `color` override ở §2.2 — apply hex vào polygon fill, giữ rotated label paper-colored. Pair override với cùng hex của paired bar/crosscut để bind trực quan thành một concern.

---

## 3. Quy tắc connector — bắt buộc

Các rule này không thương lượng. Chọn style **tự động** từ topology — không cho user override style của edge chạm focal hoặc xuất phát từ bar.

| `style` | Stroke | Width | Dash | Marker | Khi bắt buộc |
|---|---|---|---|---|---|
| `primary` | `#eb6c36` | 1.2 | — | `arrow-accent` | Mọi edge có endpoint là `focal` node. |
| `secondary` | `#4f5d75` | 1.0 | — | `arrow` | Mặc định source→component và component→component khi không endpoint nào focal. |
| `trigger` | `#4f5d75` | 1.0 | `4,3` | `arrow-sm` | Mọi edge bắt đầu từ component `kind: bar`. |
| `query` | `rgba(45,49,66,0.30)` | 1.0 | `4,3` | `arrow` | Read-back edge, ví dụ focal ↔ Trino. |

**Defs block** — bắt buộc, chính xác bốn marker sau:

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
  <marker id="arrow-dim"    markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="rgba(45,49,66,0.45)"/></marker>
</defs>
```

### 3.1 Side exit / entry — không thương lượng

| Edge kind | Side exit của source | Side entry của target |
|---|---|---|
| Source → cluster node | **right** của source node | **left** của target |
| Component → component trong cluster | **right** | **left** |
| Bar component → node | **bottom** của bar | **top** của node |
| Cross-cutting bar | — không phát edge | — |
| Vertical chevron | — chỉ label, không phát edge | — |

### 3.2 Routing

- Orthogonal elbow, **tối đa hai bend** mỗi path.
- Dùng Q-bezier corner radius 8px tại mỗi bend.
- Z-order: draw **mọi connector trước mọi node rectangle** để node fill mask đầu line.
- Chính xác một `marker-end` mỗi `<path>` / `<line>`. Không dùng đồng thời `marker-start` và `marker-end`.
- Label: mọi connector `primary` và `secondary` có label — small mono với `rect` mask fill paper opaque phía sau. Connector `trigger` và `query` không label.

### 3.3 Crossing

- Tránh. Re-route qua chevron divider trunk (§4) trước khi chấp nhận crossing.
- Nếu không tránh được, path vẽ thứ hai có arc hop 6px qua path thứ nhất.

### 3.4 Component color override

Component có thể khai báo `color: "#hex"` — CSS color string. Override **chỉ** retint container và content của component; connector tuyệt đối không recolor. Edge giữ topology-driven style từ §3.

**Vị trí áp color**, với `C = color`:

| Element | Light mode | Dark mode |
|---|---|---|
| Container fill | `rgba(C, 0.06)` | `rgba(C, 0.10)` |
| Container stroke | `rgba(C, 0.35)` (`stroke-width=1` node, `0.8` bar) | `rgba(C, 0.45)` |
| Role badge stroke — node | `rgba(C, 0.40)` | `rgba(C, 0.55)` |
| Role badge text — node | `rgba(C, 0.85)` | `rgba(C, 1.0)` |
| Icon fill / stroke | `C` | lighten `C` khoảng 15%, hoặc giữ `C` nếu đã sáng |
| Name text | `C` | lighten `C` |
| Subtitle text | **không đổi** — `muted` | **không đổi** |
| Connector chạm component | **không đổi**, vẫn topology-driven | **không đổi** |

Subtitle giữ muted vì nó là parenthetical metadata — chỉ primary identity, name + icon + border, mang color signal.

**Quy tắc:**

- **Không bao giờ trên focal node.** Focal đã mang accent (§2.7). `color` trên focal bị ignore — accent thắng.
- **Không bao giờ trên source node.** Source ở ngoài cluster và luôn neutral.
- **Cap 2 custom-colored component** mỗi diagram, ngoài focal. Ba trở lên xoá signal — cùng lý do §1 giới hạn accent 1–2 element.
- **Không color connector.** Nếu muốn edge màu, chọn `style` khác trong §3, không override color.

**Semantic use khuyến nghị:**
- `#b85450` rust-red — Security / Identity, Keycloak, Vault
- `#5a7d9a` slate-blue — Observability, Prometheus, Datadog
- `#7a8c47` olive-green — Governance / Lineage, OpenMetadata
- `#8c6d3f` warm-brown — Backup / DR

Bám palette này trừ khi brand yêu cầu khác. Random hex mỗi component chính là failure mode skill này tránh.

---

## 4. Quy tắc block branching — fan-out

Đây là nguồn rủi ro reproducibility lớn nhất. Khoá các rule này lại thì diagram trở nên predictable.

### 4.1 Source fan-out — một source → N component

```
exit_x   = source.right
trunk_x  = cluster_x - 8                     # 4-px gutter before cluster border
```

Path cho mỗi target: `M exit_x,source_cy → H trunk_x → V target_cy → H target.left`. Dùng Q-bezier corner.

### 4.2 Component fan-out — một component → N component

```
exit_x   = node.right
trunk_x  = x_boundaries[index(source.chevron) + 1] + 4   # 4 px past the chevron divider
```

Path mỗi target: `M exit_x,source_cy → H trunk_x → V target_cy → H target.left`.

### 4.3 Fan-out cap

**Tối đa 3 outgoing edge mỗi node.** Trên 3, thêm hub — thường là `focal` node. Chevron banner là legend; nếu node fan-out tới bốn downstream target thì thực tế nó là hub — làm điều đó explicit.

### 4.4 Bar drop — Airflow → N node

```
drop_x(target) = target.cx
drop_y_start   = bar.bottom
drop_y_end     = target.top
```

Straight vertical line, `style: trigger`. Một line mỗi target. Không bend — bar drop không bao giờ elbow.

### 4.5 Source vertical staggering

Khi nhiều source cùng connect tới một target, ví dụ bốn source → NiFi, stagger entry y trên target:

```
entry_y(k) = target.top + 8 + k * (target_h - 16) / (N - 1)   # k = 0..N-1, evenly spaced
```

Việc này tránh arrowhead overlap tại left edge của target.

---

## 5. Vertical chevron — semantics

Tên reserved `Orchestration`, `Security`, `Observability`, `Governance`, `Backup` luôn render trong right strip (§2.9). Bất kỳ chevron có `vertical: true` đều được xử lý như reserved-style vertical bất kể name. Quy tắc:

- **Pairing rule bắt buộc, 1:1:** mọi vertical chevron pair với chính xác một cross-spanning component và mọi cross-spanning component pair với chính xác một vertical chevron. Hai kind component được pair:
  - `kind: bar` — nằm trong cluster, top row. Convention pair với `Orchestration`.
  - `kind: cross-cutting` — nằm dưới cluster, một row mỗi component. Pair với `Security`, `Observability`, `Governance`, v.v.

  Nếu input khai báo vertical chevron không có paired component hoặc ngược lại, dừng và hỏi user — diagram chưa complete.

- **Count constraint:** `len(verticals) == len(bars) + len(crosscuts)`. Right strip chia đều cho vertical (§2.9), nên visual alignment giữa chevron và bar/row chỉ approximate — *label* mới là thứ mang nghĩa, không phải match y-pixel.

- **Ordering convention:** khai báo vertical top-down theo thứ tự bar-paired trước — Orchestration — rồi crosscut-paired theo đúng thứ tự crosscut xuất hiện dưới cluster. Điều này giữ visual reading order nhất quán.

- **Không edge:** vertical chevron không phát connector. Chúng là *label cho một column cross-cutting concern*.

- **Không node placement:** không `kind: node` nào được assign vào vertical chevron. Node luôn thuộc horizontal phase.

- **Right strip presence:** nếu có bất kỳ vertical chevron, right strip được reserve (`effective_w = 964`) và **mọi** horizontal chevron width cùng cluster geometry co theo. Không vẽ vertical chevron đè lên cluster.

Visual contract: column của vertical chevron “own” bar/cross-cutting row ở y-band tương ứng gần đúng. Orchestration ở top strip ↔ Airflow bar ở top cluster. Security ↔ Identity bar. Observability ↔ monitoring bar bên dưới identity. Và tương tự.

---

## 6. Dark mode

Khi `dark: true`, swap token:

| Token | Light | Dark |
|---|---|---|
| Page paper | `#f5f5f5` | `#1c1f2e` |
| Ink | `#2d3142` | `#f5f5f5` |
| Muted text | `#4f5d75` | `rgba(245,245,245,0.65)` |
| Chevron dark fill | `#2d3142` | `#3d4460` |
| Chevron light fill | `#3d4460` | `#4a5270` |
| Chevron label | `#f5f5f5` | `#f5f5f5` — không đổi |
| Dashed border | `rgba(45,49,66,0.20)` | `rgba(245,245,245,0.22)` |
| Cluster border | `rgba(45,49,66,0.18)` | `rgba(245,245,245,0.18)` |
| Node fill | white | `rgba(245,245,245,0.06)` |
| Node stroke | `rgba(45,49,66,0.25)` | `rgba(245,245,245,0.20)` |
| Focal fill | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| Focal stroke | `#eb6c36` | `#f08a59` |
| Accent connector | `#eb6c36` | `#f08a59` |
| Dot pattern | `rgba(45,49,66,0.10)` | `rgba(245,245,245,0.10)` |

---

## 7. Checklist reproducibility — taste gate

Trước khi emit SVG, verify **mọi** item. Item nào fail thì sửa, không ship.

1. Mọi cluster `node.cx` bằng `cx` của chevron tương ứng (§2.2 + §2.7). Đây là thứ biến chevron banner thành legend thực sự.
2. Mọi chevron `width` là multiple of 4 và ≥120.
3. Reserved right strip 28px tồn tại **iff** có vertical chevron. Nếu có, `effective_w = 964`; nếu không, `effective_w = 1000`.
4. Chính xác **một** `focal` node. Nếu input không set `focal`, mặc định first `kind: node` dưới chevron `"Storage"`.
5. Mọi edge có endpoint là focal dùng `style: primary` — accent stroke + `arrow-accent` marker.
6. Mọi edge xuất phát từ component `kind: bar` dùng `style: trigger` — dashed + `arrow-sm`.
7. Cross-cutting bar nếu có phát **zero** edge.
8. Không node nào có >3 outgoing edge, trừ khi chính nó là declared `focal` / hub.
9. Mọi `<path>` và `<line>` connector emit **trước** bất kỳ node `<rect>` nào — z-order.
10. Mỗi vertical chevron pair **1:1** với chính xác một `bar` hoặc `cross-cutting` component (§5). `len(verticals) == len(bars) + len(crosscuts)`.
11. `viewBox_h = max(540, strip_y_bot + 112)` — grow canvas khi có nhiều crosscut để legend vẫn fit.
12. Custom component color (§3.4) chỉ áp container + icon + name; connector vẫn topology-driven. Cap 2 custom-colored component ngoài focal.
13. Diagram pass SKILL.md §9 — grid 4px; ≤2 accent element; mono chỉ cho technical content; hairline; không shadow; không `rounded-2xl`.

---

## 8. Anti-pattern

- Bỏ chevron banner — nó là key map visual column sang functional phase.
- Node x-center lệch chevron (§7 #1) — phá contract “banner-as-legend”.
- Vertical chevron vẽ đè trên cluster thay vì trong reserved right strip.
- Hơn một focal node — MinIO/S3 hoặc storage hub tương ứng là *the* focal point.
- External zone dùng solid border — dashed border là signal component nằm ngoài cluster.
- Identity bar nằm trong cluster boundary — nó áp cho mọi component và phải span full canvas width.
- Vertical chevron không paired bar/cross-cutting component — xem pairing rule §5.
- Edge từ bar component vẽ solid — orchestration trigger bắt buộc dashed.
- Source fan-out >3 component mà không có hub.

---

## 9. Ví dụ

- `assets/example-high-level.html` — horizontal-only, 5 phase, light skin.
- `assets/example-high-level-dark.html` — tương tự, dark skin.
- `assets/example-high-level-full.html` — tương tự, editorial-card frame.
- `assets/example-high-level-vertical.html` — thêm vertical Orchestration + Security chevron, Airflow bar, Keycloak cross-cutting. **Reference render của full parametric pattern.**
- `assets/example-high-level-vertical-dark.html` — vertical pattern, dark skin.
- `assets/example-high-level-vertical-full.html` — vertical pattern, editorial-card frame.
- `assets/example-datalake.html` — five-phase data stack không cluster (Sources → Ingest → Data Lake → Query → Consume), zone-based flow không có container-orchestrator boundary. MinIO lake là focal node; vertical concern được flatten vào horizontal chevron banner. Light skin.
- `assets/example-datalake-dark.html` — tương tự, dark skin.
- `assets/example-datalake-full.html` — tương tự, editorial-card frame.
