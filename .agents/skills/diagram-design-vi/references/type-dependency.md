# Dependency Graph

**Phù hợp nhất cho:** thể hiện cái gì phụ thuộc vào cái gì giữa các package, module hoặc service — đặc biệt để cho thấy hai cấu trúc mà **tree** không thể biểu đạt về mặt hình học: (a) một node có **nhiều hơn một parent** — dependency dùng chung mà nhiều thứ cùng hội tụ vào — và (b) một **cycle**. Nếu data không có cả hai điều này — mọi node đều có đúng một parent và không có gì trỏ ngược — hãy dùng [Tree](type-tree.md) thay thế; nói rõ điều đó thay vì cố ép data dạng tree vào graph layout.

## Quy ước layout

- **Ranked layers.** Node nằm thành các hàng rank ngang theo dependency depth: rank 0 — entry point mà không thứ gì phụ thuộc vào — ở trên cùng, rank sâu hơn ở phía dưới. Forward edge trỏ xuống qua các rank, hoặc chạy ngang trong cùng một rank khi dependency được nén về cùng độ sâu với dependent — ví dụ shallow sibling dependency — tuyệt đối không trỏ lên ngoại trừ đúng một cycle được đánh dấu. Các rank row cách nhau 120px.
- Node dùng node-box pattern tiêu chuẩn (§6): `rx=6`, rộng 160px, cao 56px.
- **Fan-in badge.** Mỗi node có một badge Geist Mono 8px ở góc trên-phải, nằm trong box nhỏ `rx=2`, cho biết bao nhiêu node phụ thuộc vào nó (`4 in`). Một mask nằm hoàn toàn bên trong node là badge chip, không phải label — hợp lệ theo §6 rule 6. Node có fan-in cao nhất là câu chuyện cấu trúc của diagram; đừng làm thứ gì khác lớn đến mức cạnh tranh với nó.
- **Node treatment** (§5 Node type → treatment):
  - Package/service nội bộ → fill trắng + stroke `ink`.
  - External / third-party → fill `ink @ 0.03` + stroke `ink @ 0.30` — treatment External/Cloud.
  - Leaf không có outgoing edge → fill `ink @ 0.05` + stroke `muted`.
- **Cycle.** Tối đa một back-edge trỏ ngược lên chống lại rank order. Đây là editorial point của diagram: stroke `accent`, dashed `5,4`, `marker-end="url(#arrow-accent)"`, route **vòng bên ngoài** node stack — không đi thẳng xuyên giữa, không chạy sau một node mà nó không kết nối — với label Geist Mono 8px `CYCLE` có mask ở đầu nhìn thấy. Hai node mà cycle chạm tới vẫn giữ treatment node bình thường (§5) — không accent stroke/fill lên chính node, nếu không budget 2 accent bị tiêu sai chỗ.
- **Focal rule:** 2 accent element được phép trong diagram là back-edge và label `CYCLE` của nó. Không thứ gì khác trong dependency graph dùng accent.
- Toàn bộ sáu Mandatory connector rule ở §6 áp dụng đầy đủ, không ngoại lệ: rounded right-angle elbow (`r=8`) giữa các node lệch trục, label-margin 6–10px, không connector overlap — dùng bridge/hop tại crossing — fan attach point cách nhau ≥12px khi nhiều edge cùng dùng một box edge, không connector chạy sau non-endpoint box, không label mask bị node vẽ sau clip mất.

## Complexity budget

| Giới hạn | Quy tắc |
|---|---|
| Max nodes | 9 |
| Max edges | 14 |
| Max rank layers | 4 |
| Max highlighted cycles | 1 |
| Max accent elements | 2 |

Vượt budget: collapse một leaf cluster thành một aggregate node có label ghi count, ví dụ `+6 leaves`, và nói rõ trong caption — không âm thầm bỏ node.

## Anti-pattern

- Vẽ dependency graph khi data thực chất là tree — mỗi node chỉ một parent, không cycle — dùng Tree thay thế.
- Forward edge trỏ lên mà không phải cycle duy nhất được đánh dấu.
- Hairball layout không rank ordering — luôn rank trước; ranking là thứ làm graph đọc được, không phải polishing step tuỳ chọn.
- Một node cho mỗi file thay vì mỗi package/module/service — graph nói về dependency structure, không phải filesystem.
- External dependency không label — version hoặc registry phải nằm trong Geist Mono sublabel (`v3.23 · npm`), không được để implicit.
- Highlight hơn một cycle trong cùng diagram — chọn cycle quan trọng về mặt editorial; cycle thứ hai cạnh tranh với cycle đầu và cả hai đều khó đọc.
- Bỏ fan-in badge — nếu không có badge, người đọc không thể nhìn nhanh ra nơi dependency tập trung, chính là lý do dùng type này thay vì tree thường.

## Ví dụ

- `assets/example-dependency.html` — minimal light
- `assets/example-dependency-dark.html` — minimal dark
- `assets/example-dependency-full.html` — full editorial
