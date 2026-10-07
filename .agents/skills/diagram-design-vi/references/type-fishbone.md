# Fishbone / Ishikawa (root-cause)

**Phù hợp nhất cho:** phân tích root-cause có cấu trúc. Một observed effect, cause được group theo category, sub-cause treo trên từng category. Đây là artifact tiêu chuẩn của incident post-mortem — dùng khi người đọc cần thấy *đã điều tra những gì*, không chỉ kết luận.

## Quy ước layout

- **Spine.** Một horizontal line (`ink`, 1.2px) chạy trái→phải tại vertical centre `CY`, kết thúc bằng arrowhead đi vào **effect box** ở đầu phải — node-box pattern từ SKILL.md §6, chứa observed-effect statement.
- **Bones.** Category line là diagonal thẳng ở góc cố định **60°** so với spine, xen kẽ phía trên và dưới, phân bố đều dọc spine. Mỗi bone có category name ở outer end trong tag-style box nhỏ (`rx=4`, không phải pill) — Geist sans 12px weight 600.
- **Sub-causes.** Các horizontal tick ngắn 32px (`soft`) rẽ ra từ mỗi bone tại những vị trí cố định theo chiều dài, mỗi tick có sub-cause label Geist Mono 9px nằm qua phía đầu mở của tick.
- **Diagonal exemption.** SKILL.md §6 rule 1 — mandatory rounded right-angle elbow — không áp dụng cho bone 60° vì đây là grammar định nghĩa type này. Exemption **chỉ** bao phủ bone và sub-cause tick; mọi connector khác trong fishbone diagram, ví dụ callout leader hoặc cross-reference arrow, vẫn dùng rounded right-angle elbow.
- **Focal rule.** Chính xác một bone là confirmed root cause: line của nó dùng `accent`, category tag dùng `accent-tint` fill + `accent` stroke. Effect box dùng cùng treatment (`accent-tint` fill, `accent` stroke) vì đó là headline của diagram. Cặp đó — root-cause bone và effect box — là toàn bộ budget 2 accent; mọi bone, tag và tick khác giữ `ink` / `muted` / `soft`.
- **Drawing order:** background → spine → bones → sub-cause ticks → category tag boxes → effect box → legend. Line trước box để box fill cap line end sạch sẽ.

## Math

Với spine tại `y = CY`, effect box có left edge tại `x = HEAD`, bone `k` (1-indexed, k = 1..6) attach vào spine tại:

```
attach_x(k) = HEAD - 160 - k * 160
```

Bone xen kẽ phía trên (`k` lẻ) và phía dưới (`k` chẵn) spine. Far endpoint của bone — nơi category tag nằm — là offset 60° được round thành integer từ attach point:

```
dx = -96
dy = ∓168        (minus = above, plus = below)
far_x(k) = attach_x(k) + dx
far_y(k) = CY ∓ 168
```

### Pre-computed reference (5-bone layout, HEAD=1200, CY=320)

| Bone `k` | Category slot | Side | `attach_x` | `far_x, far_y` |
|---|---|---|---|---|
| 1 | first | above | 880 | 784, 152 |
| 2 | second | below | 720 | 624, 488 |
| 3 | third | above | 560 | 464, 152 |
| 4 | fourth | below | 400 | 304, 488 |
| 5 | fifth | above | 240 | 144, 152 |

Bone thứ 6 — phía dưới — sẽ attach tại `x=80`, far endpoint `(-16, 488)`, và category tag chạy từ `x=-76` đến `x=44` trong khi viewBox bắt đầu tại `x=-40`. Nó sẽ bị clip. **Năm là ceiling tại `HEAD=1200`**: để vẽ bone thứ 6, tăng `HEAD` *và* viewBox width ít nhất 160 mỗi giá trị, giữ viewBox origin ở `-40`. Cả hai phải dịch cùng nhau — chỉ tăng `HEAD` sẽ đẩy effect box rộng 200px tới `1360..1560`, vượt right edge `1440`, tức đổi một clipped tag bên trái lấy một clipped effect bên phải. Hoặc bỏ một category.

**Sub-cause tick** nằm tại fraction `m/6` dọc bone (`m = 2, 4` cho hai tick; `m = 3` cho một tick), nhờ vậy coordinate giữ trên 4px grid:

```
tick_x(k, m) = attach_x(k) - 16 * m
tick_y(k, m) = CY ∓ 28 * m
```

Tick là horizontal line 32px từ `(tick_x, tick_y)` tới `(tick_x - 32, tick_y)`; label nằm quá đầu mở, `text-anchor="end"` tại `x = tick_x - 36`, `y = tick_y - 4` cho bone phía trên hoặc `tick_y + 12` cho bone phía dưới.

## Complexity budget

| Giới hạn | Quy tắc |
|---|---|
| Max categories (bones) | 5 tại `HEAD=1200`. Bone thứ 6 cần canvas rộng hơn — xem Geometry |
| Max sub-causes per bone | 3 |
| Max sub-causes total | 18 |
| Max accent elements | 2 (root-cause bone+tag, effect box) |

## Anti-pattern

- **Hơn 5 bone trên default canvas.** Tag của bone thứ 6 clip viewBox. Tăng `HEAD` và viewBox width cùng nhau một cách có chủ đích, hoặc split theo subsystem thành hai fishbone.
- **Sub-cause chỉ nhắc lại category.** Bone “Deploy” với sub-cause “deployment issue” thêm node mà không thêm information.
- **Bone không có sub-cause.** Category rỗng là placeholder, không phải finding — xoá bone hoặc chưa vẽ nó cho tới khi có nội dung.
- **Accent hơn một root cause.** Nếu hai category đều confirmed, đó là hai diagram — hoặc một merged cause — không phải hai accent bone. Budget 2 accent là load-bearing cho signal “đây là câu trả lời”.
- **Dùng fishbone cho sequence of failures.** Một chain sự kiện theo thứ tự là timeline hoặc sequence diagram — fishbone dành cho causes của *một* effect, không phải chronology.
- **Dán classic 6M template — Man/Machine/Material/Method/Measurement/Environment — với category rỗng.** Đặt category theo investigation thực tế, không dùng generic checklist chờ điền.
- **Effect box phrased thành solution.** “Add a p99 alert” là fix, không phải observed effect. Box nói cái đã nhìn thấy — symptom, measurement, incident — không bao giờ là remedy.

## Ví dụ

- `assets/example-fishbone.html` — minimal light. Checkout p99 latency incident, 5 category, Data được xác nhận là root cause.
- `assets/example-fishbone-dark.html` — minimal dark, cùng data.
- `assets/example-fishbone-full.html` — full editorial: container framing + 3 summary card khác width + footer.
