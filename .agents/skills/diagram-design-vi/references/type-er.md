# ER / Data Model

**Phù hợp nhất cho:** conceptual và logical data model, relationship giữa API resource, domain model — mọi trường hợp mà câu chuyện chính là *entity và cardinality*.

**Không dùng cho physical schema.** ER ở cấp entity: relationship line nối *box* và mang cardinality ở mỗi đầu. Khi điểm chính là table thực với SQL type, constraint chip, index và foreign key neo **column với column**, hãy dùng [`type-db-schema.md`](type-db-schema.md) thay thế.

## Quy ước layout
- Mỗi entity là box hai phần:
  - **Header**: type tag (`ENTITY`) + entity name bằng Geist.
  - **Body**: field list bằng Geist Mono, mỗi field một dòng. PK có prefix `#`, FK có prefix `→`.
- Relationship: line giữa entity với cardinality ở mỗi đầu:
  - `1`, `N`, `0..1`, `1..*` bằng Geist Mono, 8px, đặt cách entity edge 10–12px.
  - Relationship label tuỳ chọn (“has”, “belongs to”) căn giữa line.
- Nhóm entity liên quan gần nhau; bố trí để phần lớn relationship là line thẳng, không rối.
- Coral trên aggregate root hoặc central entity của model.

## Anti-pattern
- Vẽ arrow cho mọi FK trong model có hàng chục FK — thay vào đó bố trí theo cluster.
- Cardinality notation không nhất quán giữa hai đầu cùng một relationship.
- Padding field để mọi box bằng height — height tự nhiên theo content là hợp lệ.

## Ví dụ
- `assets/example-er.html` — minimal light
- `assets/example-er-dark.html` — minimal dark
- `assets/example-er-full.html` — full editorial
