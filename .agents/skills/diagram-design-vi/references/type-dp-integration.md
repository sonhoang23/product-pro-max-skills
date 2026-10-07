# DP Integration

**Phù hợp nhất cho:** integration topology của data platform — source system nào plug in, consumer surface nào plug out và protocol mỗi bên dùng. Layout hub-and-spoke nằm trong layer **Data platform** rõ ràng; không có time/phase axis.

Dùng khi câu hỏi là *“platform này expose surface nào và qua wire/protocol nào?”* thay vì *“data di chuyển qua phase thế nào?”*.

Type này **parametric** — như `type-high-level.md`, mọi coordinate được derive từ input schema nhỏ. Cùng input phải generate SVG giống nhau về thị giác.

---

## 1. Inputs — parameter contract

```yaml
sources:                            # left column, 0..6 nodes
  - { name: "Databases",  type: "db",        subtitle: "SQL · MariaDB",
      connects_to: [{to: "NiFi", label: "JDBC"},
                    {to: "Trino", label: "FEDERATE", style: "federated"}] }
  - { name: "SFTP drops", type: "sftp",      subtitle: "scheduled pulls",
      connects_to: [{to: "NiFi", label: "SFTP"}] }
  - { name: "Email",      type: "mail",      subtitle: "IMAP attachments",
      connects_to: [{to: "NiFi", label: "IMAP"}] }
  - { name: "IBM legacy", type: "mainframe", subtitle: "file export",
      connects_to: [{to: "NiFi", label: "FILE"}] }

platform:
  name: "DATA PLATFORM"             # zone label (paper-masked top border)
  rows:                             # ordered top→bottom; each is bar or row
    - { kind: bar, name: "Trino",   icon: trino,   subtitle: "federated query · push-down",
        role: "SQL", focal: true }
    - { kind: row, nodes: [
        { name: "Apache NiFi",  icon: nifi,    role: "INGEST",   subtitle: "flow-based ETL" },
        { name: "MinIO",        icon: minio,   role: "STORE",    subtitle: "S3 object store · medallion", focal: true },
        { name: "JupyterLab",   icon: jupyter, role: "NOTEBOOK", subtitle: "Python · R · pandas" }
      ]}
    - { kind: bar, name: "Apache Airflow", icon: airflow,
        subtitle: "scheduler · DAG triggers · backfill", role: "DAG" }

consumers:                          # right column, 0..6 nodes
  - { name: "Desktop apps",   type: "monitor", subtitle: "SPSS · SAS · Stata",
      connects_from: [{from: "Trino", label: "ODBC"}] }
  - { name: "BI & reports",   type: "chart",   subtitle: "Tableau · Power BI",
      connects_from: [{from: "Trino", label: "JDBC"}] }
  - { name: "Public website", type: "globe",   subtitle: "NatStat portal",
      connects_from: [{from: "Trino", label: "HTTPS"}] }
  - { name: "API gateway",    type: "api",     subtitle: "3rd-party / OAuth2",
      connects_from: [{from: "Trino", label: "REST"}] }

footer:                             # 0..N cross-cutting bars stacked below zone (full-canvas width)
  - { name: "Active Directory", icon: key,        subtitle: "LDAP · SSO · group RBAC",
      color: "#b85450" }            # tinted red to flag the security concern
  # additional footer nodes (Observability, Backup, …) stack below this one

internal_connections:               # explicit platform-component edges
  - { from: "NiFi",        to: "MinIO",      style: "primary",   label: "WRITE" }
  - { from: "MinIO",       to: "JupyterLab", style: "secondary", label: "READ"  }
  - { from: "MinIO",       to: "Trino",      style: "secondary" }
  - { from: "JupyterLab",  to: "Trino",      style: "secondary", dashed: true }
  - { from: "Airflow",     to: ["Apache NiFi", "MinIO", "JupyterLab"], style: "trigger" }

focal_accent: "#eb6c36"             # one color for all focal components (default = SKILL accent)
dark: false
```

**Reserved `kind` cho `platform.rows`:**
- `bar` — strip full-zone-width. Default height 44px, focal bar 56px. Required `name`, `icon`; optional `subtitle`, `role`, `color`, `focal`.
- `row` — N node chia đều zone width. Required `nodes`; node có `name`, `icon`, optional `role`, `subtitle`, `color`, `focal`.

**Source/consumer `type` → icon mapping:**
- `db` → cylinder, `sftp` → folder-with-arrow, `mail` → envelope, `mainframe` → server-with-vents
- `monitor` → desktop screen, `chart` → bar-chart, `globe` → globe, `api` → curly braces
- `key` → key + ring
- Explicit icon name trong `primitive-icons.md` cũng được chấp nhận.

Per-component `color: "#hex"` là optional; xem §4.

---

Contract parametric mirror `type-high-level.md`; reserved collection là `platform.rows`. Source/consumer icon mapping mở rộng `references/primitive-icons.md`.

## 2. Layout formulas — deterministic geometry

```
# Canvas
viewBox_w        = 1200
n_sources        = len(sources)
n_consumers      = len(consumers)
n_footer         = len(footer)

# Side columns (sources left, consumers right)
col_top          = 92
col_node_h       = 64
col_gap          = 24                    # stride = col_node_h + col_gap = 88
col_h_min        = 336                   # default fits 4 sources (4 * 88 - 24)
col_h            = max(col_h_min, max(n_sources, n_consumers) * 88 - 24)
left_x           = 40
left_w           = 160
right_x          = 1000
right_w          = 160
col_node_y(k)    = col_top + k * 88
col_node_cy(k)   = col_node_y(k) + col_node_h/2     # 124, 212, 300, 388 by default

# Platform zone
zone_x           = 260
zone_w           = 696
zone_y           = 72
zone_h           = col_h                            # zone always matches column height
zone_cx          = zone_x + zone_w/2                # 608
zone_pad_x       = 16                               # inside left/right padding for bars
zone_label_y     = zone_y + 3                       # paper-masked label across top border

# Footer bars (below zone — each cross-cutting concern is a full-width bar)
footer_top       = zone_y + zone_h + 52             # 52-px gap below zone
footer_bar_h     = 56
footer_bar_x     = 40                               # aligned with source column left edge
footer_bar_w     = viewBox_w - 80                   # = 1120 — spans from source col left to consumer col right
footer_gap       = 8
footer_y(k)      = footer_top + k * (footer_bar_h + footer_gap)
footer_bottom    = footer_top + n_footer * (footer_bar_h + footer_gap) - footer_gap

viewBox_h        = max(600, footer_bottom + 84)     # 84 reserved for legend

# Platform.rows allocation inside zone
bar_h_focal      = 56
bar_h_default    = 44
row_h            = 72
row_gap          = 16
```

### 2.1 Row placement — cursor algorithm

First `kind=row` anchor vào side-column `row` 2 để connector ngang:

```
primary_row_idx  = index of first kind=row in platform.rows
primary_row_top  = col_node_y(1) - (row_h - col_node_h)/2     # 176 by default
                                                              # 4-px nudge so cy aligns with side row 2

# Place rows above primary
y = primary_row_top
for entry in platform.rows[:primary_row_idx] reversed:
    y -= row_gap
    entry.h     = bar_h_focal if (entry.kind == bar and entry.focal) else bar_h_default
    y          -= entry.h
    entry.y_top = y                                            # Trino bar lands at y=104

# Place primary row
platform.rows[primary_row_idx].y_top = primary_row_top         # NiFi/MinIO/Jupyter at y=176
platform.rows[primary_row_idx].h     = row_h

# Place rows below primary
y = primary_row_top + row_h
for entry in platform.rows[primary_row_idx+1:]:
    y          += row_gap
    entry.y_top = y
    entry.h     = bar_h_focal if (entry.kind == bar and entry.focal) else bar_h_default
    y          += entry.h

# Constraint: y <= zone_y + zone_h
```

Canonical top-bar/3-node-row/bottom-bar: Trino `y=104 h=56`, primary row `y=176 h=72`, Airflow `y=324 h=44`; gap 76px giữa primary row bottom 248 và Airflow top 324 là **có chủ đích** để Airflow align với side row 4 `cy=388`.

### 2.2 Node placement trong `row`

```
N            = len(row.nodes)
node_w       = (zone_w - 2*zone_pad_x - (N-1) * 16) / N
node_x(j)    = zone_x + zone_pad_x + j * (node_w + 16)
node_cx(j)   = node_x(j) + node_w/2
```

Canonical 3-node row cho `node_w=210.67`. Shipped example dùng fixed `node_w=160` với x `288,480,672` để cx align connector. **Cả hai hợp lệ**; formula trên là default. Mọi deviation phải ghi comment trong rendered SVG.

Với canonical 3-node row, `node_w = (696 - 32 - 32) / 3 = 210.67`. Shipped example dùng fixed `node_w=160` với custom x positions (`288, 480, 672`) để mỗi node `cx` align thuận tiện cho connector.

### 2.3 Bar placement

```
bar_x      = zone_x + zone_pad_x         # 276
bar_w      = zone_w - 2*zone_pad_x       # 664
bar_cx     = zone_cx                     # 608
```

Focal bar dùng `bar_h_focal=56`, fill `rgba(focal_accent, 0.08)`, stroke `focal_accent`. Non-focal bar dùng height 44, fill `rgba(45,49,66,0.05)`, stroke `rgba(45,49,66,0.32)`.

### 2.4 Source / consumer placement

```
source_y(k)       = col_top + k * 88            # 92, 180, 268, 356, …
source_cy(k)      = source_y(k) + col_node_h/2  # 124, 212, 300, 388, …
consumer_y(k)     = source_y(k)                 # mirrored
consumer_cy(k)    = source_cy(k)
```

Side node fixed `w=160 h=64`, fill `rgba(79,93,117,0.06)`, stroke `#7a8399`, width 1.

---

## 3. Connector rule — bắt buộc

Năm style, khóa theo topology. User không được override style trên edge chạm focal, edge xuất phát từ bar hoặc Trino→consumer.

| `style` | Stroke | Width | Dash | Marker | Khi bắt buộc |
|---|---|---|---|---|---|
| `primary` | `#eb6c36` | 1.4 | — | `arrow-accent` | Mọi edge có endpoint focal; mọi Trino→consumer edge |
| `secondary` | `#4f5d75` | 1.2 | — | `arrow` | Default internal và source→platform không chạm focal |
| `federated` | `#2e5aa8` | 1.0 | `4,3` | `arrow-link` | Federation query |
| `trigger` | `#4f5d75` | 1.0 | `4,3` | `arrow` | Mọi edge từ `kind: bar`; không label |
| `auth` | `#eb6c36` | 1.2 | `5,4` | `arrow-accent` | Mọi edge footer→zone bottom; **không bao giờ tới component cụ thể** |

**Defs block bắt buộc, đúng năm marker:**

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-link"   markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#2e5aa8"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
  <marker id="arrow-dim"    markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="rgba(45,49,66,0.45)"/></marker>
</defs>
```

### 3.1 Exit/entry side — không thương lượng

| Edge kind | Source exit | Target entry |
|---|---|---|
| Source → platform | **right** | **left** |
| Platform → platform cùng row | **right** | **left** |
| Bar → row node | **bottom** tại `node_cx(target)` | **top** |
| Platform → consumer | **right** | **left** |
| Footer → zone | **top** tại `footer_auth_x(k)` | zone bottom `y=zone_y+zone_h` |
| Footer → specific component | **forbidden** |

### 3.2 Routing

- Orthogonal elbow tối đa hai bend; Q-bezier `r=8` mỗi corner.
- **Fan-out staggering:** một node fan ra N target cùng side thì stagger exit y ±4px/index; corridor cũng stagger.
- **Z-order:** connector trước `rect`.
- **Marker:** đúng một `marker-end` mỗi `<line>/<path>`; không `marker-start`.
- **Label:** mọi `primary`, `secondary`, `federated`, `auth` edge có protocol label Geist Mono 8px + paper mask gap 6–10px. `trigger` không label.

### 3.3 Footer → zone trunk

N=1: vertical line tại `x=zone_cx` từ `footer_y(0)` tới zone bottom.

N≥2:

```
footer_auth_x(k) = zone_cx + (k - (N-1)/2) * 32     # 32-px stride per footer
```

Examples source giữ nguyên: N=1 → 560; N=2 → 544,576; N=3 → 528,560,592. Mỗi AUTH line từ `(footer_auth_x(k), footer_y(k))` tới zone bottom; label ngay trên arrowhead.

Footer contract giữ đúng geometry: N=1 dùng `x = zone_cx`; mọi AUTH line kết thúc ở `y = zone_y + zone_h`, và với footer index `k` endpoint là `(footer_auth_x(k), zone_y + zone_h)`. Marker rule áp dụng cho từng `<line>` / `<path>`.

### 3.4 Crossing

Tránh crossing. Reroute qua corridor x trước. Nếu bất khả kháng, path vẽ thứ hai dùng arc hop 6px.

---

## 4. Component `color` override

Source, consumer, platform node/bar hoặc footer chấp nhận `color: "#hex"`.

| Element | Light | Dark |
|---|---|---|
| Container fill | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| Container stroke | `rgba(C, 0.35)` | `rgba(C_light, 0.45)` |
| Role badge stroke | `rgba(C, 0.40)` | `rgba(C_light, 0.55)` |
| Role badge text | `rgba(C, 0.85)` | `rgba(C_light, 1.0)` |
| Icon stroke/fill | `C` | `C_light` |
| Name text | `C` | `C_light` |
| Subtitle | **không đổi** muted | **không đổi** |
| Connector chạm component | **không đổi** topology-driven | **không đổi** |

`C_light` = hex lightened ~15%.

Rule:
- **Không focal component** — `focal_accent` thắng, `color` ignored.
- **Không connector** — chọn `style`, không `color` override.
- **Tối đa 2 custom-colored component** ngoài focal pair.

Palette khuyến nghị:
- `#b85450` rust-red — Security / Identity
- `#5a7d9a` slate-blue — Observability
- `#7a8c47` olive-green — Governance / Lineage
- `#8c6d3f` warm-brown — Backup / DR

---

Trong color override, ký hiệu nguồn là `C = color`. Container là `rect`; node dùng `stroke-width=1`, bar dùng `0.8`. Với dark contrast, ví dụ `#b85450` → `#d97a78`.

## 5. Focal rule

**Chính xác hai focal component.** Default: storage hub (MinIO/S3) và federation engine (Trino/Dremio). Hai surface này phân biệt “platform” với “pile of tools”. Mọi thứ khác giữ ink/muted.

- Mark `focal: true`.
- Focal `kind: bar` dùng height 56 + accent styling.
- Focal row node giữ row_h 72 + accent styling.
- **Trino → mọi consumer** edge luôn `primary`, bất kể consumer focal flag — serve-flow rule.
- Ít hơn hoặc nhiều hơn 2 focal component → **dừng và hỏi người dùng**.

---

Focal contract dùng `focal: true` cho đúng hai component. Focal `kind: bar` dùng `bar_h_focal=56`; focal `kind: row` node giữ `row_h=72`. Non-focal bar dùng `bar_h_default=44`.

Trong input contract, federation bar mang `focal: true`, storage hub mang `focal: true`; checklist/validation cũng đếm component khai báo `focal: true`. Footer AUTH trunk kết thúc tại `zone_y + zone_h`.

## 6. Dark mode

| Token | Light | Dark |
|---|---|---|
| Page paper | `#f5f5f5` | `#2d3142` |
| Ink | `#2d3142` | `#f5f5f5` |
| Muted | `#4f5d75` | `#bfc0c0` |
| Accent | `#eb6c36` | `#f08a59` |
| Link | `#2e5aa8` | `#6a95d8` |
| Side-column fill | `rgba(79,93,117,0.06)` | `rgba(245,245,245,0.06)` |
| Side-column stroke | `#7a8399` | `rgba(245,245,245,0.30)` |
| Zone fill | `rgba(45,49,66,0.025)` | `rgba(245,245,245,0.04)` |
| Zone stroke | `rgba(45,49,66,0.32)` | `rgba(245,245,245,0.30)` |
| Non-focal bar fill | `rgba(45,49,66,0.05)` | `rgba(245,245,245,0.06)` |
| Focal fill | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| Focal stroke | `#eb6c36` | `#f08a59` |
| Custom colors | `C` | `C_light` |

---

## 7. Reproducibility checklist

1. `viewBox = "0 0 1200 {viewBox_h}"`, `viewBox_h=max(600, footer_bottom+84)`.
2. Platform zone `x=260 y=72 w=696 h=col_h`; zone label paper-mask top border tại `y=zone_y+3`.
3. Left column `x=40..200`, right `x=1000..1160`, width 160.
4. Source/consumer row top `y=92`, stride 88.
5. `platform.rows` stack theo cursor algorithm; total y-span ≤ `zone_h`.
6. Node x-center trong `kind: row` chia đều zone width.
7. **Chính xác 2** focal component.
8. Edge từ `kind: bar` dùng `trigger`, dashed, unlabelled.
9. Trino→consumer dùng `primary`.
10. Footer chỉ nối zone bottom bằng `auth`; **không** nối specific component.
11. Custom color ≤2 ngoài focal pair; connector không recolor.
12. Connector trước rect.

---

Checklist dùng `viewBox_h = max(600, footer_bottom + 84)`. Mọi edge từ bar dùng `style: trigger`; mọi Trino → consumer edge dùng `style: primary`. API icon được mô tả bằng curly braces `{}`.

## 8. Source/consumer icon library

Định nghĩa icon là `<g id="ico-…">` trong `<defs>`, draw tại translate(cx,cy), `stroke="currentColor"`.

- `ico-db`, `ico-sftp`, `ico-mail`, `ico-mainframe`
- `ico-monitor`, `ico-chart`, `ico-globe`, `ico-api`
- `ico-key`, `ico-monitoring`

Cần icon khác thì xem `assets/icons.html` và define matching `<symbol>`.

---

## 9. Identity/common service → nối layer, không component

**Active Directory** hoặc Keycloak/IAM/OPA/secrets store cross-cutting authenticate *mọi* component. Nối bằng một arrow tới bottom edge platform zone, label `AUTH`, không nối riêng tool.

Rule này áp dụng cho centralized logging, secrets vault, observability, audit sink, mTLS root. Mỗi service vào `footer`, mỗi service một row và AUTH line riêng stagger theo §3.3. Visual meaning: platform layer delegates tới các service đó.

---

## 10. Budget — type này vượt default có chủ đích

Một integration thực tế có:
- 4–6 source node
- 5 platform component
- 4–6 consumer node
- 1–3 footer node

Tổng **14–20 node**. Complexity là nội dung chính. Khi quá unwieldy, combine source thật sự identical hoặc split theo integration plane.

---

Nếu có nhiều source giống nhau, có thể gộp bốn MariaDB thành node `Databases` với sublabel `4 × MariaDB`; đây là compression được source cho phép.

## 11. Anti-pattern

- Collapse source/consumer thành một node khi có ≥3 distinct item — dùng Architecture/High-level nếu muốn collapse.
- Một bus arrow từ “sources” tới “platform” — mỗi wire phải label protocol.
- Per-tool color coding trong zone — chỉ 2 focal accent + tối đa 2 custom cross-cutting color.
- Hơn 2 focal component.
- `color` override trên focal — ignored.
- Footer nối một specific tool trừ khi scope thực sự chỉ tool đó.
- Footer/identity nằm trong zone — sai trust model.
- Phase chevron trên top — thuộc `high-level`.
- Custom-colored connector — connector topology-driven.

---

## 12. Ví dụ

- `assets/example-dp-integration.html` — minimal light.
- `assets/example-dp-integration-dark.html` — dark.
- `assets/example-dp-integration-full.html` — editorial-card frame.
- `assets/example-dp-integration-extended.html` — color override + multi-footer.
- `assets/example-dp-integration-extended-dark.html` — extended dark.
- `assets/example-dp-integration-extended-full.html` — extended full.
