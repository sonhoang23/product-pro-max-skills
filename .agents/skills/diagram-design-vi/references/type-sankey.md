# Sankey / Flow-Quantity

**Phù hợp nhất cho:** thể hiện một *quantity* đi đâu khi tách và nhập qua một số ít stage — CI compute budget, volume flow gần funnel, phân bổ cost/headcount. Đây là type duy nhất mà **thickness của band mang data**; nếu người đọc không cần so magnitude, dùng process hoặc pyramid.

## Quy ước layout

- **Chính xác 3 stage column**, trái → phải. Không hơn, không kém — trên 3 stage thì tách thành hai diagram liên kết.
- **Node là vertical bar**, `width=12`, fill `ink` solid, không stroke. Height tỷ lệ với quantity đi qua, làm tròn tới 4px gần nhất để nằm trên grid — rounding chỉ là rendering step, không thay đổi data; true value vẫn in trong quantity sublabel.
- **Flow là filled ribbon**, không phải stroked line: mỗi flow là một closed `<path>`. Top edge là cubic Bézier từ source top-offset tới target top-offset; bottom edge là cùng curve chạy ngược từ target-bottom về source-bottom. **Cả hai** control point nằm tại horizontal midpoint giữa hai column, mỗi điểm ở y của endpoint tương ứng: `C midX,y0 midX,y1 targetX,y1`. Điều này làm band rời/đến bar **theo phương ngang**, cắm vuông vào bar. Đặt control thứ hai tại target x (`C midX,y0 targetX,y1 targetX,y1`) làm tangent tới endpoint suy biến và ribbon gặp bar ở góc xiên — trông như không gắn vào bar.
- **Không bao giờ dùng arrowhead.** Direction được ngầm hiểu từ column trái→phải. Đây là ngoại lệ rõ ràng với rule orthogonal-elbow-and-arrowhead ở SKILL.md §6: ribbon là area encoding, không phải connector.
- **Ribbon fill:** ordinary flow dùng `muted` opacity `0.18`. Một editorial focal path dùng `accent` opacity `0.28`. Một focal path có thể gồm nhiều ribbon segment; `accent` tất cả segment thuộc path đó vẫn tính là **một** focal element. Không rainbow color theo flow.
- **Node ordering giảm crossing.** Sắp node trong từng column để flow converging/diverging giữ thứ tự top-to-bottom nhất quán. Nếu hai ribbon vẫn cắt nhau hơn một lần, reorder node.
- **Label:** node name Geist sans 12px 600, quantity ngay dưới bằng Geist Mono 9px `muted`. Column 1 ở ngoài bar `text-anchor="end"`; column 2 ở gutter phía trên bar `text-anchor="middle"`, **center theo chiều dọc trong gutter**; column 3 ở ngoài `text-anchor="start"`.

  Center column-2 label trong gutter giúp nó nằm trên clean paper và không cần mask. Không dùng mask rect ở đây — trên filled band nó trông như lỗ thủng. Nếu label thật sự không có vùng trống, column đã over budget: bỏ node hoặc split diagram.
- **Column header:** Geist Mono 8px uppercase tracked, centered phía trên mỗi column — kiểu eyebrow “CI COMPUTE BUDGET / TEST STAGE / OUTCOME”, không phải full sentence.
- **Drawing order:** background → column headers → ordinary ribbons → ribbon của accent path (paint cuối trong ribbons) → node bars → node labels → legend.
- **Legend:** horizontal strip bottom theo global rule, tăng viewBox ~60–100px vì Sankey thường cần bottom clearance hơn. Swatch là rectangle 16×8 theo ribbon treatment, có thể thêm italic aside cho editorial read.

## Quy tắc scale

Chọn **một px-per-unit constant `k`** cho toàn diagram và áp dụng cho mọi node/ribbon thickness — không scale khác nhau theo column. Làm tròn thickness về 4px gần nhất và reconcile rounding ở node level, không flow level, để outgoing ribbon vẫn cộng chính xác bằng rounded node height.

**Khi kiểm soát được số liệu, chọn số rơi đúng grid.** Với `k`, step 4px là `4/k` unit; chọn quantity là whole multiple của nó thì drawn area khớp số in. Rounding chỉ là fallback cho real data. Không bao giờ để rounding vượt một step 4px và không round flow tới mức ribbon không còn sum bằng bar.

**Minimum rendered ribbon thickness: 4px.** Giá trị round xuống dưới mức này phải fold vào band `other`, không vẽ hairline vô hình.

### Worked reference (`k = 0.02` px/unit, budget = 12,000 CI minutes)

| Node | Quantity | Height (px) |
|---|---|---|
| CI minutes (col 1) | 12,000 | 240 |
| Unit tests | 5,200 | 104 |
| E2E | 4,000 | 80 |
| Build | 2,000 | 40 |
| Lint | 800 | 16 |
| Passed | 9,400 | 188 |
| Failed | 1,600 | 32 |
| Flaked | 1,000 | 20 |

Tổng node height của mỗi column đều là 240px — invariant total-in = total-out giúp diagram đáng tin. Nếu column không cùng total, data bị leak hoặc layout có bug.

## Complexity budget

| Giới hạn | Quy tắc |
|---|---|
| Max stage columns | 3 |
| Max nodes | 8 |
| Max flows (ribbons) | 12 |
| Max accent elements | 2 (ribbon của một focal path tính là một dù trải qua bao nhiêu segment) |

Over budget → split thành hai Sankey liên kết thay vì nhồi fourth column hoặc ninth node.

## Anti-pattern

- **Ribbon gặp bar ở góc xiên.** Đây là lỗi control-point: cả hai control nằm ở midpoint x.
- **Opaque mask rect sau column-2 label.** Nó trông như lỗ thủng; center label trong gutter.
- **Column-2 label dính top gutter.** Center theo chiều dọc.
- **Bar height không khớp số in bên cạnh.** Tuân scale rule.
- **Ribbon cắt nhau hơn một lần.** Reorder node.
- **Ribbon mỏng hơn 4px.** Merge vào `other`.
- **Rainbow color theo flow.** Ordinary dùng một `muted` treatment, focal dùng accent.
- **Dùng Sankey cho funnel đơn giản.** Dùng pyramid/funnel.
- **Dùng Sankey cho step sequence không split/merge/thickness variation.** Dùng process.
- **Hai flow stack cùng node-edge offset.** Mỗi flow có offset range riêng theo thứ tự top-to-bottom.
- **Quantity/percentage không sum về source total.** Mỗi node incoming/outgoing phải sum bằng node height.

## Ví dụ

- `assets/example-sankey.html` — minimal light.
- `assets/example-sankey-dark.html` — minimal dark, cùng data.
- `assets/example-sankey-full.html` — full editorial.
