# Deployment

**Phù hợp nhất cho:** phần mềm thực sự *chạy ở đâu* — host, VM, pod và managed service đặt bên trong các zone môi trường hoặc network-boundary, kèm replica count và versioned artifact. Architecture trả lời “cái gì nói chuyện với cái gì”; deployment trả lời “cái gì được cài trên host nào, ở environment nào, sau network boundary nào, với bao nhiêu replica.” Nếu diagram không có quyết định physical placement nào để thể hiện — không zone boundary, không replica count, không version quan trọng — hãy dùng `type-architecture.md` thay thế; vẽ lại logical architecture rồi gắn hostname vào là deployment anti-pattern phổ biến nhất.

## Quy ước layout

Ba level nesting, từ ngoài vào trong — tái sử dụng containment grammar từ `type-nested.md`, chuyên biệt cho infrastructure:

1. **Zone** — environment hoặc network boundary (`edge`, `prod / eu-west-1`, `data`). Một rect lớn, `rx=8`, fill `ink @ 0.02`, stroke `ink @ 0.20` dashed `4,4`. Label eyebrow uppercase tracked bằng Geist Mono 8px — hoặc 7px cho layout chật — nằm bên trong góc trên-trái, trên paper-colored mask phủ qua border. Zone được vẽ **đầu tiên** — trước arrow và node — để label và box được paint phía trên chúng; z-order: bg → zones → arrows → labels → nodes.
2. **Infrastructure node** — host, VM, pod hoặc managed service bên trong zone. Dùng node-box pattern §6 trong SKILL.md tại `rx=6`, với rectangular type tag `rx=2` — **không** phải pill — mang `POD` / `VM` / `MANAGED` / `CDN` ở góc trên-trái.
3. **Artifact chip** — thứ được deploy lên node đó. Một rect nhỏ cao 24px, `rx=4`, fill `ink @ 0.05`, stroke `muted`, chứa image hoặc service name bằng Geist sans 12px left-aligned cùng version tag Geist Mono 9px right-aligned, ví dụ `v2.4.1`. Một node có thể chứa nhiều chip — stack với gap 8px — khi nhiều artifact co-located, ví dụ sidecar.

**Replica badge.** Node chạy N copy có badge Geist Mono 8px right-aligned (`x3`) trong box `rx=2` riêng ở góc trên-phải của node. Mask nằm hoàn toàn bên trong node là badge chip và là ngoại lệ hợp lệ cho rule “mask không được overlap node vẽ sau” — SKILL.md §6 rule 6 — vì nó là một phần của cùng node đó.

**Network path.** Orthogonal elbow giữa các node — SKILL.md §6, elbow formula và port-selection rule trong `type-architecture.md` — được label protocol và port bằng Geist Mono 8px (`HTTPS:443`, `TLS:5432`). Path đi qua zone boundary dùng `link`-blue; path ở trong cùng một zone dùng `muted`. Async hoặc replication path dashed `5,4`.

**Focal rule.** 2 accent element là single-point-of-failure hoặc thành phần mới được đưa vào — không bao giờ hơn 2. Trong canonical example: RDS primary — accent-tint fill, accent stroke — và replication path sang standby — accent, dashed.

## Complexity budget

| Giới hạn | Quy tắc |
|---|---|
| Max zones | 3 |
| Max infrastructure nodes | 6 |
| Max artifact chips | 9 |
| Max network paths | 8 |
| Max accent elements | 2 |

Vượt budget → tách thành một deployment diagram cho mỗi environment.

## Anti-pattern

- Vẽ lại logical architecture rồi gắn hostname. Nếu không có placement decision nhìn thấy được — host nào, zone nào, bao nhiêu replica — dùng `type-architecture.md` thay thế.
- Zone chỉ để group trực quan mà không có boundary meaning — zone phải là environment/network boundary thật, không phải layout convenience.
- Artifact chip không có version tag. Version chính là lý do diagram tồn tại; chip không version là một box lãng phí.
- Vẽ một node cho mỗi replica thay vì một node với replica badge.
- Cloud-vendor icon soup thay cho named node — hãy đặt tên host/service, đừng chỉ trang trí.
- Network path không label. Protocol và port là content của deployment diagram, không phải decoration.
- Trộn hai environment trong một diagram, ví dụ staging và production nằm cạnh nhau mà không có zone boundary thực sự phân tách chúng.

## Ví dụ

- `assets/example-deployment.html` — minimal light
- `assets/example-deployment-dark.html` — minimal dark
- `assets/example-deployment-full.html` — full editorial
