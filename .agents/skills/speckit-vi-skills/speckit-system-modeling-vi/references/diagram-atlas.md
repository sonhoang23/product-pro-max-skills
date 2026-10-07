# Diagram Atlas & Feature Ledger

## Mục tiêu

Diagram trong repo tạo thành một **navigation graph có phân cấp**, không phải tập file HTML rời rạc.

Mô hình:

```text
Repo Diagram Atlas
   ↓
Feature / Spec Diagram Ledger
   ↓
Diagram
   ↕
Parent / Children / Related diagrams
```

Tree dùng để điều hướng từ tổng quan xuống chi tiết; graph `related` dùng để đi ngang giữa các mental model liên quan.

## Canonical locations

- Repo Atlas: `docs/diagrams/index.html`
- Graph registry: `docs/diagrams/diagram-index.json`
- Feature ledger: `FEATURE_DIR/diagrams.html`
- Feature diagrams: `FEATURE_DIR/<phase>-diagram/*.html`
- Project diagrams: `docs/diagrams/<topic>/*.html`

Không di chuyển diagram chỉ để gom vật lý vào một folder. Atlas/ledger giải quyết discoverability.

## Registry

Mọi living diagram MUST có một entry duy nhất trong `docs/diagrams/diagram-index.json`.

Conceptual entry:

```json
{
  "id": "feature-001-core-flow",
  "title": "One-AI Presentation Generation Flow",
  "scope": "feature",
  "truth": "planned",
  "phase": "spec",
  "topic": "feature",
  "feature": "001-presentation-foundation",
  "path": "specs/001-presentation-foundation/spec-diagram/core-flow.html",
  "source": "specs/001-presentation-foundation/spec.md",
  "parent": "feature-001-ledger",
  "children": ["feature-001-ai-job-claim"],
  "related": ["lifecycle", "ai-bridge"]
}
```

### Truth metadata

Mỗi entry MUST phân biệt:

- `scope`: `feature` hoặc `project`;
- `truth`: `planned` hoặc `implemented`;
- `phase`: `spec`, `plan`, `tasks`, `implementation`, `converge` hoặc `project`.

Quy tắc:
- `spec/plan/tasks` feature diagrams luôn có `truth=planned`;
- `implementation` feature diagram chỉ có `truth=implemented` khi phase đã hoàn tất và verification pass;
- mọi project diagram trong `docs/diagrams/` phải có `truth=implemented`;
- Atlas MAY hiển thị cả planned và implemented diagram nhưng phải làm khác trạng thái rõ ràng; không được khiến planned feature diagram trông như current project architecture.

### Stable ID

- ID MUST ổn định và duy nhất trong repo.
- Rename file không mặc định rename ID nếu mental model vẫn là cùng một model.
- Feature diagram SHOULD prefix bằng feature id để tránh collision.

## Relations

### parent

Một navigation parent duy nhất:

- `repo-atlas`;
- feature ledger pseudo-id như `feature-001-ledger`;
- hoặc ID của một diagram khác.

Parent biểu diễn drill-down hierarchy, không nhất thiết là source authority.

### children

Diagram chi tiết hơn mà reader có thể drill-down tới.

Nếu child có parent là một diagram khác, parent SHOULD liệt kê child trong `children`.

### related

Quan hệ ngang. Không yêu cầu reciprocal tuyệt đối, nhưng SHOULD thêm backlink khi nó giúp khám phá hai chiều.

### source

Canonical textual artifact mà diagram derive từ đó.

## Feature ledger

Mỗi feature có diagram MUST có `FEATURE_DIR/diagrams.html`.

Ledger MUST:

- link lên Repo Atlas;
- link về source artifacts của feature;
- liệt kê toàn bộ diagram feature-level;
- liệt kê project diagrams liên quan quan trọng;
- hiển thị modeling status/freshness khi có thể;
- không tạo requirement/decision mới.

Nếu feature hiện không có diagram, không bắt buộc tạo ledger rỗng.

## Navigation chrome trong diagram

Mỗi living diagram MUST có navigation chrome ngoài SVG gồm tối thiểu:

- Repo Atlas;
- Feature Ledger nếu là feature diagram;
- Parent nếu có;
- current diagram title;
- canonical Source **dưới dạng metadata path**;
- Children và Related quan trọng.

### HTML-only navigation

Atlas được thiết kế để đọc trực tiếp bằng browser/file://. Vì vậy:

- mọi clickable navigation link trong Repo Atlas, Feature Ledger và diagram navigation chrome MUST trỏ tới một file `.html` hoặc HTML anchor;
- `.md`, `.json`, source code và modeling-state path MUST hiển thị dưới dạng metadata/text, không phải navigation destination;
- registry vẫn giữ raw `source`, `modeling_state` và technical path cho traceability;
- nếu sau này cần đọc source trong browser, tạo một HTML view/wrapper riêng thay vì đổi navigation pill sang raw file.

Navigation chrome không được làm thay đổi SVG semantics và không được tính vào complexity budget của diagram.

## Update transaction

Sau mỗi modeling run tạo/xóa/rename/thay relation của diagram:

1. tạo/cập nhật diagram;
2. cập nhật `diagram-index.json`;
3. cập nhật/regenerate feature ledger liên quan;
4. cập nhật Repo Atlas nếu feature/category/top-level inventory thay đổi;
5. cập nhật navigation chrome/backlinks của diagram liên quan;
6. chạy Atlas validation;
7. chỉ sau đó ghi modeling gate là pass.

Không để state `modeled` nếu output diagram tồn tại nhưng registry/ledger bị stale.

## Validation

Khi có checkout local, chạy:

```bash
python scripts/verify-diagram-atlas.py\npython scripts/verify-diagram-layout.py
```

Validator kiểm tra tối thiểu:

- duplicate ID;
- diagram/source/feature ledger path không tồn tại;
- reference tới parent/child/related ID không hợp lệ;
- project/feature diagram HTML tồn tại nhưng chưa đăng ký;
- project diagram có `truth != implemented`;
- spec/plan/tasks feature diagram có `truth != planned`;
- feature diagram không có feature entry;
- diagram thiếu Atlas navigation chrome;
- navigation chrome chứa clickable link tới non-HTML file;
- parent/child relation không nhất quán khi parent là diagram.\n\nLayout/language validator kiểm tra thêm nhãn UI chưa Việt hóa, text có nguy cơ tràn, rect vượt viewBox và connector thẳng đi xuyên node không phải endpoint.

## Authority

Atlas, ledger, registry và navigation chrome đều là **derived navigation artifacts**.

Chúng không đứng trong authority chain và không được tạo semantics mới. Canonical decisions vẫn theo:

```text
constitution > spec > plan > tasks > implementation
```
