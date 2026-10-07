# Modeling Plan

## Source of truth

Đọc theo nhu cầu:

- `spec.md`;
- `plan.md`;
- `research.md`;
- `data-model.md`;
- `contracts/`;
- constitution.

Spec giữ business/product requirement. Plan và technical artifacts giữ intended technical design.

## Mục tiêu

Trực quan hóa technical design đã được plan quyết định khi `tasks` chạy `ensure-model(plan)` hoặc khi người dùng gọi modeling thủ công; modeling không quyết định kiến trúc thay plan.

Diagram candidate:

- architecture/component responsibility;
- data flow;
- technical sequence;
- integration boundary;
- data model/ER khi relation khó đọc;
- deployment/runtime topology khi plan đã quyết định;
- security/trust boundary khi có giá trị.

## Quy tắc

- Không thêm component/service/database chỉ để diagram đẹp.
- Nếu diagram cần một quyết định chưa có trong plan, đánh `[OPEN]` và quay lại plan.
- Technical diagram phải trace được về plan/data-model/contracts.
- Không biến conceptual entity trong spec thành physical table nếu plan chưa quyết định.

## Output

`FEATURE_DIR/plan-diagram/`

Ví dụ:

```text
plan-diagram/
  architecture.html
  data-flow.html
  data-model.html
  deployment.html
```
