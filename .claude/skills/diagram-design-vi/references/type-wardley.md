# Wardley Map

**Phù hợp nhất cho:** đặt các component của value chain theo mức độ evolved/commoditised để reader thấy cái gì nên build, cái gì nên buy và cái gì sắp dịch chuyển. Đây là strategy artifact, không phải architecture diagram — nó không nói component connect thế nào ở runtime, chỉ nói mỗi component đứng ở đâu trên curve genesis→commodity.

## Quy ước layout

- **Y axis — value chain.** `Visible to the user` ở top, xuống `Invisible` ở bottom. Label axis bằng các `<text>` line riêng xếp chồng ở hai endpoint — **không bao giờ dùng `writing-mode`** để rotate label dọc. Axis line dùng `rule-solid` opacity `0.20`.
- **X axis — evolution.** Bốn band ngăn bởi ba vertical hairline: `Genesis | Custom-built | Product | Commodity`. Band separator dùng `rule` opacity 0.10, dashed `4,4`. Band label nằm dọc bottom axis: Geist Mono 8px, uppercase, tracked, `muted`. Axis line `rule-solid` opacity 0.20.
- **Component** là circle nhỏ `r=6`, fill `paper`, stroke `ink` 1px. Label Geist sans 12px weight 600, đặt 12px phía trên dot, `text-anchor="middle"`. Optional Geist Mono 9px `muted` sublabel có thể nằm dưới dot cho technical qualifier — dùng tiết chế.
- **Dependency link** là line thẳng `muted` 0.8px từ component xuống component mà nó phụ thuộc. **Đây là documented exemption duy nhất của §6 rule 1 — mandatory orthogonal elbow — và chỉ dành cho dependency link.** Vị trí x/y của component trên map *chính là data*; ép nó về axis để tạo elbow sẽ làm sai vị trí. Không arrowhead — bản thân line đã nói dependency.
- **Movement** — component đang evolve có một short right-pointing arrow: `accent`, dashed `5,4`, `marker-end="url(#arrow-accent)"`, chạy từ edge của dot hướng sang band kế. Arrow không cần on-arrow text label: legend swatch "Evolving" — `accent` dot + dashed accent arrow — đã gọi tên meaning của accent + dashes, và vì movement arrow trên map chỉ có thể trỏ sang phải, direction đã nói “toward commodity.” Một bare word như `COMMODITISING` chỉ lặp lại thứ shape và color đã encode — áp remove test §1: nếu bỏ label mà color/shape vẫn truyền đạt đủ thì bỏ label, không phải đổi vị trí của nó.
  On-arrow label chỉ hợp lệ khi nó bổ sung qualifier mà arrow không tự biểu đạt — timeframe như `BY Q3`, driver như `VENDOR LOCK-IN` — không bao giờ chỉ restate direction. Nếu thêm, mask bằng Geist Mono 8px, gap 6–10px khỏi stroke theo §6 rule 2, và trước hết phải xác nhận quanh arrow có runway cho mask. Vùng quanh component dot thường congested nhất vì dependency link cũng fan-out ở đó. Worked example: moving component trong `example-wardley.html` ở `(420,156)`, có link fan tới `(620,220)` và `(680,252)`; tại mandatory gap band phía dưới arrow `y=164–176`, hai line này cắt tại `x=441.7–482.5` và `x=445–482.5`, gần như phủ toàn span của arrow `x=428–504`, không để lại clear pocket đủ rộng cho label. Phía trên dot cũng không tốt hơn vì component name đã chiếm band đó theo rule “12px above dot”. Kiểm tra cả hai band trước khi thêm movement label; nếu không band nào clear thì đừng thêm — legend đã đủ.
- **Focal rule:** 2 accent element của type này là moving component dot — `accent-tint` fill, `accent` stroke — và movement arrow của nó; hoặc hai moving component cùng chia hai accent slot và không còn accent ở nơi khác.
- **Legend:** horizontal strip dưới đáy, hairline separator phía trên, viewBox tăng khoảng 60px — giống mọi type khác.

Axis line dùng `rule-solid` ở opacity `0.20`; band separator dùng `rule` ở opacity `0.10`.

## Complexity budget

| Giới hạn | Quy tắc |
|---|---|
| Max components | 9 |
| Max dependency links | 12 |
| Max movement arrows | 2 |
| Max accent elements | 2 |

## Anti-pattern

- **X axis bị dùng như maturity score.** Evolution là bốn qualitative band — genesis / custom-built / product / commodity — không phải slider 0–10. Không plot component ở “6.5”; đặt nó trong một band.
- **Component không có dependency link.** Nếu không ai phụ thuộc nó và nó cũng không phụ thuộc gì thì nó không thuộc value chain — xoá hoặc wire nó vào.
- **Arrow right-to-left.** Evolution chỉ đi toward commodity. Movement arrow trỏ trái là contradiction, không phải design choice.
- **Dùng map như architecture diagram.** Không request/response direction, không protocol, không runtime topology — đó là architecture type. Type này trả lời “cái gì đáng build vs buy,” không phải “traffic chạy thế nào.”
- **Đánh số y axis.** Value-chain visibility là ordinal — visible hơn hoặc ít visible hơn với user — không phải quantity. Numeric tick ám chỉ measurement không tồn tại.
- **Hơn 2 movement arrow.** Khi đó map không còn tạo một single point mà biến thành forecast không ai hành động được.
- **`writing-mode` vertical axis text.** Xếp word thành các horizontal `<text>` line riêng như Layout conventions ở trên.

## Ví dụ

- `assets/example-wardley.html` — minimal light. AI assistant product, agent orchestration đang commoditising hướng tới Product.
- `assets/example-wardley-dark.html` — minimal dark, cùng map.
- `assets/example-wardley-full.html` — full editorial: framed container + 3 varied-width card — moving component, genesis-stage build và commodity base.
