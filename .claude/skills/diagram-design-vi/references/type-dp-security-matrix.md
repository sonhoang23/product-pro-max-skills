# DP Security Matrix

**Phù hợp nhất cho:** document permission theo role/component trong data platform — mỗi row là platform component (Keycloak, MinIO bucket, Trino catalog, JupyterHub, NiFi, …), mỗi column là role/AD group. Mỗi intersection cell chứa permission value (`Admin`, `Full`, `R/W`, `Read`, `SELECT`, `Login`, `No access`) cùng visual category tương ứng. Một cell có thể focal để flag critical access rule.

Dùng khi stakeholder cần audit *ai có thể làm gì* trên platform. Ưu tiên **DP integration** khi câu hỏi là *ai có thể nói chuyện với cái gì* (topology/protocol), thay vì *ai có thể write/read gì* (permission).

Type này **parametric** — input schema §1 điều khiển coordinate qua formula §2. Rule shape mirror `type-medallion.md`, `type-process.md`, `type-data-flow.md`.

---

## 1. Inputs — parameter contract

```yaml
title:    "Platform Access Matrix"
subtitle: "Four canonical groups × platform components"

roles:                                  # 2..6 columns, ordered left → right
  - { name: "Data Administrators", code: "DL-DataAdmins"      }
  - { name: "Data Engineers",      code: "DL-DataEngineers"   }
  - { name: "Data Scientists",     code: "DL-DataScientists"  }
  - { name: "Data Consumers",      code: "DL-DataConsumers"   }

components:                             # 2..14 rows, ordered top → bottom
  - { name: "Keycloak",                          hint: "SSO" }   # `hint` = right-aligned aside in label cell
  - { name: "MinIO · raw bucket" }
  - { name: "MinIO · anon · staging · agg" }
  - { name: "Trino · raw catalog" }
  - { name: "Trino · anon-staging" }
  - { name: "Trino · aggregated" }
  - { name: "JupyterHub" }
  - { name: "NiFi" }

cells:                                  # explicit (row, col) entries; omitted → defaults to "none"
  # value = displayed text (free-form)
  # level = visual category: full | rw | read | none  (closed vocabulary, drives styling)
  # focal: true (max 1)            — overrides level to focal styling
  # sub: "second-line text"        — used inside focal cell
  # color: "#hex"                  — optional per-cell color override (§4)
  - { row: 0, col: 0, value: "Admin", level: "full" }
  - { row: 0, col: 1, value: "Login", level: "read" }
  - { row: 0, col: 2, value: "Login", level: "read" }
  - { row: 0, col: 3, value: "Login", level: "read" }

  - { row: 1, col: 0, value: "Full",       level: "full" }
  - { row: 1, col: 1, value: "R/W",        level: "rw"   }
  - { row: 1, col: 2, value: "No access",  level: "none" }
  - { row: 1, col: 3, value: "No access",  level: "none" }

  # ... rows 2..4 follow the same pattern ...

  - { row: 5, col: 0, value: "Full",       level: "full" }
  - { row: 5, col: 1, value: "R/W",        level: "rw"   }
  - { row: 5, col: 2, value: "SELECT",     level: "read" }
  - { row: 5, col: 3, value: "SELECT only", sub: "sole consumer access", focal: true }

  # ... rows 6..7 ...

none_label: "No access"                 # default text rendered when a cell is omitted
dark: false
```

**Reserved field semantics:**
- `roles[j].name` — primary role label (`node-name` 11px, white trên `ink` banner).
- `roles[j].code` — secondary AD-group identifier (`sublabel`, white opacity 0.85).
- `components[i].hint` — optional right-aligned `sublabel` trong label cell.
- `cells[k].level` — closed vocabulary `full | rw | read | none`, drive styling §2.4.
- `cells[k].value` — free-form display text; domain-specific label không cần new `level`.
- `cells[k].focal: true` — chính xác **một** cell được phép; override `level` thành focal styling.
- `cells[k].sub` — optional second line dưới primary value, `sublabel` 8px.
- `cells[k].color: "#hex"` — optional per-cell `color` override (§4).

---

Reserved semantics mirror `type-medallion.md` và `type-process.md`: `roles[j].name` dùng role `node-name`; `roles[j].code` và `components[i].hint` dùng `sublabel`. Hint ví dụ gồm `"SSO"` và `"S3 API"`; display value có thể là `"R/W"`, `"SELECT"` hoặc `"Login"` mà không tạo level mới.

## 2. Layout formulas — deterministic geometry

```
# Constants
left_pad         = 12
right_pad        = 48
comp_col_w       = 208
comp_role_gap    = 12
role_col_w       = 148
role_col_gap     = 16
header_h         = 52
row_h            = 36
row_stride       = 40

# Counts
n_roles          = len(roles)        # 2..6
n_components     = len(components)   # 2..14

# Canvas
viewBox_w        = left_pad + comp_col_w + comp_role_gap
                   + n_roles * role_col_w + (n_roles - 1) * role_col_gap
                   + right_pad
                   # 4 roles → 12 + 208 + 12 + 592 + 48 + 48 = 920

header_y         = 72
row_y(k)         = 140 + k * row_stride                  # 140, 180, 220, ...
rows_bottom      = row_y(n_components - 1) + row_h       # 8 rows → 456
legend_y_top     = rows_bottom + 20                      # 476 for 8-row canonical
viewBox_h        = legend_y_top + 44                     # 520 for 8-row canonical

# Column positions
comp_col_x       = left_pad                                                       # 12
role_col_x(j)    = left_pad + comp_col_w + comp_role_gap
                   + j * (role_col_w + role_col_gap)
                                                                                  # 232, 396, 560, 724
role_col_cx(j)   = role_col_x(j) + role_col_w / 2                                 # 306, 470, 634, 798
```

### 2.1 Background

Solid paper fill toàn viewBox. Không dot pattern.

### 2.2 Header row `y=72 h=52`

**Component-column header:** rect white + stroke `ink @ 0.12` 0.8 `rx=6`; two-line centered `Component` / `vs. AD group`, lần lượt `node-name` 11px ink và `sublabel` muted.

**Role banner:** rect tại `role_col_x(j)`, fill `ink`, `rx=6`; role name `y=92` `node-name` 11px white, role code `y=108` `sublabel` white opacity 0.85.

Header contract đầy đủ: `y = 72, h = 52`. Component header rect là `(comp_col_x, header_y, comp_col_w, header_h)`; hai label anchor tại `(comp_col_x + comp_col_w/2, header_y+24)` và `(…, header_y+40)` với text `"Component"` / `"vs. AD group"`. Role banner rect là `(role_col_x(j), header_y, role_col_w, header_h)`.

### 2.3 Data row `y=row_y(k), h=36`

**Component label cell:** white rect, stroke `ink @ 0.12` 0.8, `rx=4`; name left at `comp_col_x+12`, `hint` optional right at `comp_col_x+comp_col_w−12`.

**Value cell:** rect tại role column, `rx=4`, stroke `ink @ 0.12` 0.6; fill/text theo `level`. Value centered tại `role_col_cx(j), row_y(k)+22`. Focal dùng primary y+18 + sub y+30.

Data row contract là `y = row_y(k), h = 36`. Component label rect là `(comp_col_x, row_y(k), comp_col_w, row_h)`; name tại `(comp_col_x + 12, row_y(k) + 22)` và hint tại `(comp_col_x + comp_col_w − 12, row_y(k) + 22)`. Value rect là `(role_col_x(j), row_y(k), role_col_w, row_h)`, value tại `(role_col_cx(j), row_y(k) + 22)`. Focal primary/sub dùng `y=18` và `y=30` tương đối trong cell.

### 2.4 Cell style

| `level` | Fill | Stroke | Text color | Weight |
|---|---|---|---|---|
| `full` | `ink @ 0.08` | `ink @ 0.12` | `ink` | 600 |
| `rw` | `#FFFFFF` | `ink @ 0.12` | `ink` | 400 |
| `read` | `muted @ 0.08` | `ink @ 0.12` | `muted` | 400 |
| `none` | `paper` | `ink @ 0.12` | `soft` | 400 |
| **focal** | `accent @ 0.07` | `accent` width 1.4 | `accent` | 600 |

Focal cell có thể có second line `sub`, `accent`, `sublabel` 8px opacity 0.85.

### 2.5 Legend

Hairline separator tại `legend_y_top`. Bên dưới là một row swatch chỉ cho style thực sự dùng. `LEGEND` `eyebrow` tại `(left_pad, legend_y_top+20)`. Item stride khoảng 120px; wrap second visual row chỉ nếu `n_roles ≥ 6`.

---

Legend contract là `y_top = legend_y_top, h ≈ 30`; `LEGEND` đặt tại `(left_pad, legend_y_top + 20)`, swatch dùng `rx=2`.

## 3. Cell, không connector

Matrix **không có connector** — không arrow giữa cell, không flow line. Information nằm hoàn toàn ở cell content + styling. Focal cell `accent` border chỉ là callout intersection, không phải connector.

Không emit edge. Không thêm arrow vào/giữa cell.

---

## 4. Color override

Ba axis độc lập: per-cell, per-component row, per-role column. Tất cả optional, cùng field `color: "#hex"`.

Ba override axis mirror `type-high-level.md`; ký hiệu màu là `C`.

### 4.1 Per-cell `color`

| Element | Light | Dark |
|---|---|---|
| Cell fill | `rgba(C, 0.08)` | `rgba(C_light, 0.12)` |
| Cell stroke | `rgba(C, 0.45)` width 1.0 | `rgba(C_light, 0.55)` width 1.0 |
| Value text | `C` | `C_light` |
| Sub text | `rgba(C, 0.85)` | `rgba(C_light, 0.95)` |

`C_light` = same hex lightened ~15%.

### 4.2 Per-component `color` — `components[i].color`

Chỉ tint **row label cell**; data cell giữ `level` styling.

| Element | Light | Dark |
|---|---|---|
| Label cell fill | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| Label cell stroke | `rgba(C, 0.45)` width 0.8 | `rgba(C_light, 0.55)` width 0.8 |
| Component name | `C` | `C_light` |
| Hint | unchanged muted | unchanged muted |

### 4.3 Per-role `color` — `roles[j].color`

Chỉ tint **column banner**; body cell giữ `level`. Banner fill `C`; role name/code text `#FFFFFF` nếu luminance ≤0.5, ngược lại `ink`. `roles[j].text_color` có thể override auto-pick.

Role banner auto-contrast có thể override bằng `roles[j].text_color: "#hex"`; warm-yellow ví dụ là `#c9a23a`.

### 4.4 Rule

- **Focal cell thắng**; ignore `color` trên focal.
- Per-cell `color` override `level` styling ở cell đó.
- Per-component/per-role override chỉ scope label/banner, không lan vào body.
- Tổng custom-colored entity ≤5 (cell + component + role).

### 4.5 Palette khuyến nghị

- `#b85450` rust-red — Security elevation / break-glass / SoX-flagged
- `#5a7d9a` slate-blue — Quality / monitoring / observability gate
- `#7a8c47` olive-green — Approved / governance-cleared / publication-ready
- `#c9a23a` warm yellow — Working / sandbox / data-scientist zone
- `#8c6d3f` warm-brown — Archive / cold / DR

---

## 5. Focal rule

Chính xác **một** focal cell mỗi diagram (hoặc zero theo source contract). Focal cell:
- accent fill + accent stroke 1.4 + bold accent text;
- có thể 2-line content: primary `value` tại `row_y(k)+18`, `sub` tại `row_y(k)+30`;
- nêu central security claim của diagram.

Nếu zero hoặc >1 `focal: true` cell được khai báo, **dừng và hỏi người dùng**.

---

Focal cell primary value nằm tại `y = row_y(k) + 18`; `sub:` nếu có nằm tại `y = row_y(k) + 30`.

Component label và value text dùng role `node-name`; hint/sub-line dùng `sublabel`, và legend label cũng dùng `sublabel`. Focal primary/sub nằm tại `y = row_y(k) + 18` và `y = row_y(k) + 30`. Worked proof bên dưới map tới `example-dp-security-matrix.html`.

## 6. Dark mode

| Token | Light | Dark |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Soft | `soft` | `muted` |
| Accent | `accent` | `accent` |
| Role-banner fill | `ink` | `ink` |
| Header / row stroke | `ink @ 0.12` | `paper @ 0.18` |
| Full / Admin fill | `ink @ 0.08` | `paper @ 0.10` |
| R/W fill | `#FFFFFF` | `paper @ 0.06` |
| Read fill | `muted @ 0.08` | `soft @ 0.12` |
| No-access fill | `paper` | `paper @ 0.02` |
| Focal fill | `accent @ 0.07` | `accent @ 0.12` |
| Focal stroke | `accent` | `accent` |
| Custom colors | `C` | `C_light` |

---

## 7. Reproducibility checklist

1. `viewBox` derive theo §2; 4 role × 8 component → `920 × 520`.
2. Header row `y=72 h=52`; component header white, role banner ink.
3. Data row start `y=140`, stride 40, h=36.
4. Component label `rx=4`, name left, hint optional right.
5. Mọi value cell `rx=4`, stroke `ink @ 0.12` 0.6, style theo §2.4.
6. Chính xác **một** focal cell (hoặc zero); stroke accent 1.4; primary/sub position đúng.
7. Cell omit khỏi `cells:` render `level: "none"` với `none_label` default `"No access"`.
8. Custom-colored cell ≤2 ngoài focal.
9. Không có connector element trong SVG.
10. Legend tại `legend_y_top`, swatch cho `level` thực sự dùng.
11. `viewBox_h` tăng theo component; `viewBox_w` tăng theo role.

---

Checklist canonical dùng `viewBox = "0 0 {viewBox_w} {viewBox_h}"`, header label `Component / vs. AD group`, `rows_bottom = 140 + (n_components−1)·40 + 36`, name tại `x=24` và hint tại `x = comp_col_x + comp_col_w − 12`. Cả `n_components` và `n_roles` đều làm viewBox tăng theo contract.

## 8. Anti-pattern

- Hơn một focal cell.
- Connector ở bất kỳ đâu.
- Freeform `level`; closed vocabulary là `full | rw | read | none`; free-form text dùng `value`.
- Per-row hoặc per-column color tint — theo source rule, hãy apply `color` per cell để tránh over-emphasis.
- Dùng `none_label` làm placeholder `TBD`; `none` nghĩa là *no access*.
- Hơn 6 role — split matrix.
- Hơn 14 component — split theo domain.
- Dùng matrix để document *cách permission được grant* — dùng process/sequence; matrix chỉ nói *permission hiện có là gì*.

---

## 9. Ví dụ

- `assets/example-dp-security-matrix.html` — minimal light.
- `assets/example-dp-security-matrix-dark.html` — dark.
- `assets/example-dp-security-matrix-full.html` — full editorial.

---

## 10. Worked YAML — full inputs cho example

```yaml
title:    "Platform Access Matrix"
subtitle: "Four canonical groups × platform components"

roles:
  - { name: "Data Administrators", code: "DL-DataAdmins"      }
  - { name: "Data Engineers",      code: "DL-DataEngineers"   }
  - { name: "Data Scientists",     code: "DL-DataScientists"  }
  - { name: "Data Consumers",      code: "DL-DataConsumers"   }

components:
  - { name: "Keycloak",                          hint: "SSO" }
  - { name: "MinIO · raw bucket" }
  - { name: "MinIO · anon · staging · agg" }
  - { name: "Trino · raw catalog" }
  - { name: "Trino · anon-staging" }
  - { name: "Trino · aggregated" }
  - { name: "JupyterHub" }
  - { name: "NiFi" }

cells:
  # Row 0 — Keycloak
  - { row: 0, col: 0, value: "Admin", level: "full" }
  - { row: 0, col: 1, value: "Login", level: "read" }
  - { row: 0, col: 2, value: "Login", level: "read" }
  - { row: 0, col: 3, value: "Login", level: "read" }
  # Row 1 — MinIO raw
  - { row: 1, col: 0, value: "Full", level: "full" }
  - { row: 1, col: 1, value: "R/W",  level: "rw"   }
  - { row: 1, col: 2, value: "No access", level: "none" }
  - { row: 1, col: 3, value: "No access", level: "none" }
  # Row 2 — MinIO anon/staging/agg
  - { row: 2, col: 0, value: "Full", level: "full" }
  - { row: 2, col: 1, value: "R/W",  level: "rw"   }
  - { row: 2, col: 2, value: "Read", level: "read" }
  - { row: 2, col: 3, value: "No access", level: "none" }
  # Row 3 — Trino raw catalog
  - { row: 3, col: 0, value: "Full", level: "full" }
  - { row: 3, col: 1, value: "R/W",  level: "rw"   }
  - { row: 3, col: 2, value: "No access", level: "none" }
  - { row: 3, col: 3, value: "No access", level: "none" }
  # Row 4 — Trino anon-staging
  - { row: 4, col: 0, value: "Full",   level: "full" }
  - { row: 4, col: 1, value: "R/W",    level: "rw"   }
  - { row: 4, col: 2, value: "SELECT", level: "read" }
  - { row: 4, col: 3, value: "No access", level: "none" }
  # Row 5 — Trino aggregated (focal cell at col 3)
  - { row: 5, col: 0, value: "Full",        level: "full" }
  - { row: 5, col: 1, value: "R/W",         level: "rw"   }
  - { row: 5, col: 2, value: "SELECT",      level: "read" }
  - { row: 5, col: 3, value: "SELECT only", sub: "sole consumer access", focal: true }
  # Row 6 — JupyterHub
  - { row: 6, col: 0, value: "Admin", level: "full" }
  - { row: 6, col: 1, value: "R/W",   level: "rw"   }
  - { row: 6, col: 2, value: "R/W",   level: "rw"   }
  - { row: 6, col: 3, value: "No access", level: "none" }
  # Row 7 — NiFi
  - { row: 7, col: 0, value: "Admin", level: "full" }
  - { row: 7, col: 1, value: "R/W",   level: "rw"   }
  - { row: 7, col: 2, value: "Read",  level: "read" }
  - { row: 7, col: 3, value: "No access", level: "none" }

dark: false
```

Worked proof của `example-dp-security-matrix.html` dùng `n_roles = 4`, `n_components = 8`; `row_y(k)` tạo `140, 180, 220, 260, 300, 340, 380, 420`; `rows_bottom = 420 + 36 = 456`, `legend_y_top = 476`, `viewBox_h = 520`, `role_col_x(j) = [232, 396, 560, 724]`. Focal cell `(row=5, col=3)` render rect `(724, 340, 148, 36)`.

### 10.1 YAML này chứng minh gì

- `n_roles=4`, `n_components=8`, no color override, one focal cell.
- `viewBox_w = 12 + 208 + 12 + 4·148 + 3·16 + 48 = 920` ✓
- `row_y(k) = 140, 180, 220, 260, 300, 340, 380, 420` ✓
- `rows_bottom=456`; `legend_y_top=476`; `viewBox_h=520` ✓
- `role_col_x(j)=[232,396,560,724]` ✓
- Focal `(row=5,col=3)` → rect `(724,340,148,36)`, accent stroke 1.4 ✓

Fresh generation từ YAML này phải visually indistinguishable với shipped example.
