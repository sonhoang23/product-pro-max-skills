# Database Schema

**Phù hợp nhất cho:** *physical* schema — table thực, SQL type thực, constraint thực, index thực và foreign key nối column này với column khác. Đây là DDL được làm cho dễ đọc: migration, review database thực và mọi trường hợp mà column type hoặc hành vi `ON DELETE` là trọng tâm.

**Không dùng cho domain modeling.** [ER / data model](type-er.md) ở cấp entity: relationship line nối *box* và mang cardinality, field chỉ là list; phù hợp cho thảo luận conceptual/domain. Database schema ở cấp column: FK connector neo vào đúng row của column ở cả hai đầu — năng lực ER không có và là lý do type này tồn tại. Nếu đang bàn Order *là gì*, dùng ER. Nếu đang bàn điều gì xảy ra khi row bị delete, dùng type này.

## Quy ước layout

### Table box
- **Header band** — `schema.table` (ví dụ `public.orders`) bằng Geist sans 12px weight 600, cùng type tag chữ nhật (`rx=2`, KHÔNG phải pill) ghi `TABLE`. Hairline ngăn header với body.
- **Column row** — cố định row height 24px để connector neo ổn định. Mỗi row: column name Geist sans 12px bên trái, SQL type Geist Mono 9px `muted` bên phải (`uuid`, `text`, `numeric(12,2)`, `timestamptz`), constraint chip nằm giữa dưới dạng tag nhỏ `rx=2`, Geist Mono 8px: `PK`, `FK`, `UQ`, `NN`. Row chẵn dùng alternate background `ink @ 0.02` để dễ quét.
- **Overflow row** — nếu table có nhiều column hơn budget, row cuối là dòng Geist Mono 9px `muted`: `+ N more columns`. Không bao giờ âm thầm truncate table.
- **Index compartment** — final compartment tuỳ chọn tách bằng hairline, có eyebrow Geist Mono 8px uppercase `INDEXES`, liệt kê index name bằng Geist Mono 9px (`idx_orders_customer_id`, `uq_products_sku`). Chỉ liệt kê index quan trọng với câu chuyện, không phải mọi index.

### Foreign-key connector — rule định nghĩa type

Mỗi FK edge bắt đầu tại **vertical centre của source column row** và kết thúc tại **vertical centre của referenced column row**, route bằng orthogonal rounded elbow (xem SKILL.md §6 và [type-architecture.md](type-architecture.md)). Gắn label Geist Mono 8px theo referential action — `ON DELETE CASCADE`, `ON DELETE RESTRICT`, `ON DELETE SET NULL` — với mask và gap chuẩn 6–10px. Row height cố định 24px đảm bảo ≥12px separation chỉ khi hai FK gắn vào *hai row khác nhau* trên cùng table edge — row spacing tự tạo fan. Khi hai FK trở lên gắn vào *cùng row* trên cùng edge (ví dụ hai child table cùng tham chiếu primary key của parent), không được neo tất cả đúng row centre vì vi phạm SKILL.md §6 rule 4. Offset attach point đối xứng quanh vertical centre của row — ±8px cho hai edge, vẫn nằm trong band 24px và cách neighbor ≥12px — để mỗi connector vẫn đọc là gắn vào row đó nhưng có thể lần theo độc lập.

### Nhóm schema

Table trong non-default schema nằm trong containment rect (`rx=8`, fill `ink @ 0.02`, stroke `ink @ 0.20` dashed `4,4`) với schema label Geist Mono 8px uppercase tracked ở góc trên-trái. Vẽ group rect trước để table paint lên trên.

### Focal rule

2 accent element là: (1) destructive FK duy nhất (`ON DELETE CASCADE`) — edge và label tính chung một element; và (2) table mà FK cascade vào, dùng `accent-tint` trên **header band בלבד**, không trên toàn box. Không thứ gì khác dùng `accent`.

Nếu schema không có destructive FK, không có focal element. Để không accent thay vì tự nâng một table bất kỳ.

## Complexity budget

Tối đa 5 table, 8 column row hiển thị mỗi table, 6 FK edge, 2 accent element. Vượt budget → chỉ thể hiện subsystem, không phải toàn database, và nói rõ trong caption.

## Anti-pattern
- Vẽ mọi column của mọi table — schema diagram là lập luận về subsystem, không phải dump `\d+`.
- FK line nối box-to-box thay vì column-to-column — đó là ER, hãy dùng ER.
- Thiếu SQL type — type là nửa nội dung.
- FK edge không label — hành vi `ON DELETE` là điều reviewer cần thấy.
- Constraint chip trên mọi row đến mức chip thành nhiễu.
- Index compartment liệt kê mọi index thay vì index quan trọng.
- Trộn conceptual entity name với physical table name trong cùng diagram.

## Ví dụ
- `assets/example-db-schema.html` — minimal light
- `assets/example-db-schema-dark.html` — minimal dark
- `assets/example-db-schema-full.html` — full editorial
