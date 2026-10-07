# Modeling Spec

## Source of truth

Bắt buộc đọc:

1. `.specify/memory/constitution.md` nếu có;
2. `FEATURE_DIR/spec.md`;
3. research/product direction chỉ khi spec cần truy nguồn.

Không dùng code boilerplate để mở rộng requirement.

## Mục tiêu

Giúp người đọc nhìn được WHAT/WHY của hệ thống khi gate `spec` được kiểm tra trước technical planning hoặc khi người dùng gọi modeling thủ công.

Diagram candidate:

- system context / boundary;
- actor-role-capability map;
- core user flow;
- use-case overview;
- conceptual domain model;
- lifecycle/state;
- journey khi phù hợp.

Không tạo:

- component/service/module architecture;
- API contract;
- database physical schema;
- deployment/infrastructure diagram.

Các phần đó thuộc plan.

## Ambiguity gate

Nếu modeling phát hiện ambiguity ảnh hưởng:

- boundary;
- actor/role;
- core flow;
- domain invariant;
- lifecycle;
- acceptance behavior;

thì dừng và quay lại `$speckit-clarify` hoặc cập nhật `spec.md`.

Không tạo `analysis/*.md` để vá ambiguity.

## Output

`FEATURE_DIR/spec-diagram/`

Ví dụ:

```text
spec-diagram/
  system-context.html
  core-flow.html
  domain-model.html
  lifecycle.html
```

Không bắt buộc tạo đủ bốn file. Diagram Check quyết định.

Nếu clarify làm thay đổi mental model, gate `spec` trở nên stale; lần `ensure-model(spec)` kế tiếp chỉ update diagram khi thay đổi đó thực sự ảnh hưởng visual semantics.
