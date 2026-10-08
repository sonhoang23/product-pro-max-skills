# Loop

**Phù hợp nhất cho:** reinforcing cycle, flywheel, feedbac`k` loop và operating loop — nơi bước cuối quay lại bước đầu và shared hub tích luỹ state. Dùng Loop `k`hi người đọc cần thấy đồng thời hai motion: work tiến clockwise quanh ring, mỗi pass ghi durable state về một center chung.

Ưu tiên **Flowchart** khi path kết thúc, branch về outcome hoặc không thực sự quay lại step đầu. Ưu tiên **Cycle** khi center không tích luỹ shared state. Dashed write-back spoke là defining signal: bỏ chúng thì figure chỉ còn circular process.

Type này **parametric**. Input ở §1 quyết định station count, angle, edge intersection, connector path và viewBox bound. Input giống nhau phải tạo geometry giống nhau.

---

## 1. Input — parameter contract

```yaml
title: "The self-improving loop"
subtitle: "Every pass improves the shared operating record"

hub:                                  # exactly one
  name: "Shared memory"
  sublabel: "one record, every loop"

stations:                             # 5..8, clockwise from top
  - { name: "Capture",  sublabel: "signals in",       spoke_label: "SIGNALS" }
  - { name: "Research", sublabel: "evidence pulled" }
  - { name: "Decide",   sublabel: "human approves",   focal: true }
  - { name: "Act",      sublabel: "work ships",        spoke_label: "OUTCOMES" }
  - { name: "Measure",  sublabel: "outcomes logged" }
  - { name: "Learn",    sublabel: "playbook updated" }

station_w: 160
station_h: 64
hub_w: 200
hub_h: 104
radius: 240
margin: 64
dark: false
```

**Budget (hard):** **5–8 station + chính xác một hub.** Trên 8 station, split overview Loop + detail diagram. Chính xác một hub; hai hub là hai diagram. Tối đa một station `focal: true`; zero được phép.

Station order là semantic. `stations[0]` ở top, sau đó clockwise. Station cuối luôn nối về station 0; nếu return đó sai, dùng Flowchart.

---

## 2. Layout math — deterministic geometry

Dùng SVG coordinate với y dương hướng xuống. Hub center `C = (cx, cy)`, station count `N`, ring radius `R`, station half-size `a = station_w/2`, `b = station_h/2`, hub half-size `A = hub_w/2`, `B = hub_h/2`.

### 2.1 Station center

```text
theta_k = -90deg + k * (360deg / N)
u_k     = (cos(theta_k), sin(theta_k))
P_k     = C + R * u_k

station_center_x(k) = cx + R * cos(theta_k)
station_center_y(k) = cy + R * sin(theta_k)
station_x(k)        = station_center_x(k) - station_w/2
station_y(k)        = station_center_y(k) - station_h/2
```

Station 1 ở top và `k` tăng theo clockwise. Round station rectangle về 4px grid gần nhất sau ideal geometry; preserve symmetry khi round paired station. Giữ ring-circle intersection tới ba decimal để arc cùng circle.

### 2.2 Solid ring-flow endpoint

Ring connector từ station `k` tới `j = (k + 1) mod N` bằng circular SVG arc trên chính station circle. Mọi segment cùng center `C`, radius `R`, clockwise sweep. Station box interrupt circle; connector bắt đầu tại clockwise exit khỏi source box và kết thúc ngay trước counterclockwise entry vào destination, để marker tip chạm destination stroke.

Tìm circle/rectangle intersection với bốn edge. Với vertical edge `x = x_e`:

```text
y = cy +/- sqrt(R^2 - (x_e - cx)^2)
```

Giữ candidate có `y` trong edge. Với horizontal edge `y = y_e`:

```text
x = cx +/- sqrt(R^2 - (y_e - cy)^2)
```

Giữ candidate có `x` trong edge. Hai point còn lại classify theo normalized polar angle quanh `C`:

```text
q_entry(k) = circle/box intersection immediately before theta_k clockwise
q_exit(k)  = circle/box intersection immediately after  theta_k clockwise
```

Compensate marker tip trước khi emit destination endpoint. Với canonical marker (`refX=7`, polygon tip `x=8`) và ring stroke `1.2`, `marker_overhang = 1.2`:

```text
phi_entry = atan2(q_entry(j).y - cy, q_entry(j).x - cx)
phi_end   = phi_entry - marker_overhang / R
q_end     = C + R * (cos(phi_end), sin(phi_end))

M q_exit(k).x q_exit(k).y
A R R 0 0 1 q_end.x q_end.y
```

Large-arc flag `0` vì adjacent gap <180°; sweep flag luôn `1` cho clockwise trong SVG. Arrowhead overhang hoàn tất 1.2px cuối tới `q_entry(j)` mà không xuyên stroke. Closing connector `N-1`→0 dùng cùng formula.

Circular ring arc của Loop là ngoại lệ type-specific với SKILL.md §6 rule 1, tương tự promotion arc của Medallion. Loop không mix cubic, straight hoặc rounded-orthogonal segment vào ring: visible gap phải đọc như những phần của cùng một circle.

### 2.3 Dashed write-back spoke endpoint

Mỗi spoke chạy từ station edge hướng vào hub, theo radial vector `u_k`:

```text
box_distance(v, half_w, half_h) = min(half_w / abs(v.x), half_h / abs(v.y))
                                        # ignore a term whose denominator is zero

d_station = box_distance(u_k, a, b)
d_hub     = box_distance(u_k, A, B)
marker_gap = 6                         # 4..8px; 6px canonical

spoke_start(k) = P_k - d_station * u_k
hub_edge(k)    = C   + d_hub     * u_k
spoke_end(k)   = C   + (d_hub + marker_gap) * u_k
```

Vì arrow đi từ station về `C`, cộng `marker_gap` để endpoint dừng ngay ngoài hub boundary. Spoke radial là ngoại lệ type-specific với ban on slanted straight connector; phải là true radius, không cắt nhau và chỉ chạm source station + hub.

Label optional nếu station sublabel đã nói write-back. Nếu dùng, follow `arrow-label`, nằm một bên spoke, có opaque `paper` mask và visible gap 6–10px. Chỉ label curated subset.

### 2.4 ViewBox sizing

ViewBox phải bao toàn station rectangle, outer ring curve, arrowhead và ít nhất `margin` breathing room:

```text
left   <= cx - R - station_w/2 - margin
right  >= cx + R + station_w/2 + margin
top    <= cy - R - station_h/2 - margin
bottom >= cy + R + station_h/2 + margin

viewBox_w = right - left
viewBox_h = bottom - top
```

Check cả circle extrema `cx +/- R`, `cy +/- R`, station bound và marker clearance. Không shrink tới mức clip. Canonical six-station: `viewBox="0 0 1040 680"`, `C=(520,340)`, `R=240`, station `160×64`, hub `200×104`.

---

## 3. Visual grammar

| Element | Treatment |
|---|---|
| Station | Standard node: `paper` fill, `ink` stroke, `radius-md`; name `node-name`, sublabel `sublabel` |
| Hub | Dark element duy nhất: `ink` fill, `paper` text; lớn hơn station một chút |
| Focal station | Tối đa một: `accent-tint` fill, `accent` stroke; name có thể `accent` |
| Ring flow | Circular `A R R 0 0 1` arc trên station circle, solid `muted`, default arrowhead tại destination; clockwise only |
| Write-back spoke | Dashed `soft`, `stroke-dasharray="5,4"`, `soft` arrowhead |
| Spoke label | `arrow-label`, `soft`, uppercase, paper mask, cách connector 6–10px |

Drawing order: paper/dot grid → ring arrows → dashed spokes → spoke-label masks/labels → station boxes → hub → text.

Hub không phải process step thứ bảy. Nó là accumulated state: memory, standard, evidence, policy hoặc shared operating record. Copy chỉ một name + một short sublabel.

---

Visual grammar giữ đúng token source: hub dùng `ink`, focal station dùng `accent`, và write-back spoke dùng `soft`.

## 4. Quy tắc connector (bắt buộc)

SKILL.md §6 áp dụng đầy đủ trừ hai Loop primitive: circular ring arc (§2.2) và straight radial spoke (§2.3), thay rule 1:

- Ring arrow là same-radius circular arc, solid, clockwise; mọi path dùng `A R R 0 0 1`; marker destination chạm station edge, không center.
- Spoke dashed và hướng inward. Solid spoke phá distinction giữa operating flow và write-back.
- Label dùng opaque mask + gap 6–10px.
- Không ring connector/spoke nào overlap. Ring ngoài hub; spoke theo radial route riêng.
- Nếu hai spoke phải rời cùng station edge, fan attach point theo §6 với ≥12px. Normal Loop có một spoke/station; spoke thứ hai chỉ khi semantic không merge được.
- Nếu ring route cắt hub, tăng `R` hoặc split. Không thread flow qua shared state hay đổi sang orthogonal route.

---

## 5. Dark variant — token swap

Áp dụng inversion rule của style guide; không tạo palette thứ hai.

| Role | Light | Dark |
|---|---|---|
| Canvas and station fill | `paper` | dark `paper` |
| Primary text and station stroke | `ink` | inverted `ink` |
| Hub fill / hub text | `ink` / `paper` | inverted `ink` / dark `paper` |
| Ring flow | `muted` | dark `muted` |
| Write-back spokes and labels | `soft` | dark `soft` |
| Focal fill / stroke | `accent-tint` / `accent` | dark `accent-tint` / brighter dark `accent` |
| Rule and dot grid | `rule` | inverted `rule` same opacity |

Semantic relation không đổi trong dark mode.

---

## 6. Reproducibility checklist

1. Station count 5–8, hub chính xác một.
2. Station 0 tại `-90deg`; còn lại equal `360/N` clockwise.
3. Mọi solid ring arrow nối adjacent station bằng `A R R 0 0 1`, cùng `R`; last returns first.
4. Mọi ring marker chạm station edge, không center.
5. Mọi dashed spoke bắt đầu inner edge station và dừng `marker_gap` trước hub stroke.
6. Ring connector ở ngoài hub; spoke không cross/overlap.
7. Tối đa một station dùng `accent-tint` + `accent`; chỉ hub dùng dark `ink` fill.
8. Spoke label nếu có dùng `arrow-label`, opaque mask, gap 6–10px.
9. ViewBox chứa station box, stroke, curve, marker, margin không clip.

---

## 7. Anti-pattern

| Anti-pattern | Vì sao fail / cách sửa |
|---|---|
| Hai hub | Hai accumulated state = hai system. Vẽ hai diagram. |
| Solid spoke | Trông như primary flow. Dùng dashed `soft` write-back. |
| Station angle không đều vô lý | Ring mất operating cadence. Dùng equal `360/N` trừ documented phase gap. |
| Mix arc + orthogonal ring segment | Ring thành rounded rectangle. Mọi segment phải same-radius circular arc. |
| Connector cắt hub | Flow lẫn state. Tăng radius/route ngoài. |
| Accent nhiều station | Mất editorial gate. Tối đa một focal station. |
| Hơn 8 station | Label/spoke crowded. Split overview + detail. |
| Cycle không thực sự return | Đó là Flowchart đặt vòng tròn. Dùng Flowchart. |

---

## 8. Ví dụ

- `assets/example-loop.html` — minimal light: six-station self-improving operating loop.
- `assets/example-loop-dark.html` — cùng geometry dưới dark token inversion.
- `assets/example-loop-full.html` — editorial page với flagship loop, 3 summary card và colophon.
