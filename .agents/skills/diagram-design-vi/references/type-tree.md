# Tree / Hierarchy

**Phù hợp nhất cho:** org chart, dependency tree, taxonomy, file tree, decision breakdown, skill tree.

## Quy ước layout
- Root ở trên, child xoè xuống dưới (hoặc root bên trái, child sang phải).
- Node là labeled rectangle nhỏ (`rx=6`), name Geist 12px 600 + sublabel Geist Mono 9px tuỳ chọn. Width 120–180px, height 40–52px.
- **Connector phải orthogonal (kiểu elbow), không bao giờ diagonal.** Parent thả một line dọc ngắn, sau đó horizontal bus nối sibling, rồi mỗi child có một vertical drop ngắn vào top edge. Stroke muted 1px.
- Leaf indicator: stroke mảnh hơn (0.8) hoặc fill khác — HOẶC để terminal position tự truyền đạt.
- Max depth: 4 (root + 3 tier). Max breadth mỗi level: 5.
- Coral trên **một** node: root HOẶC critical leaf. Không dùng cả hai.
- Vẽ connector trước node.

## Anti-pattern
- Tree sâu 5+ level trên một page (khó đọc — tách ra).
- Node có width chênh lệch quá lớn — tối đa 2 width.
- Diagonal connector line.
- Bỏ qua level (parent nối thẳng grandchild mà không có middle).
- Coral trên cả root VÀ leaf.

## Ví dụ
- `assets/example-tree.html` — minimal light
- `assets/example-tree-dark.html` — minimal dark
- `assets/example-tree-full.html` — full editorial
