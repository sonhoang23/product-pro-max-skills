# Modeling Implementation Phase

## Source of truth

Kết hợp có phân biệt:

- intended: `spec.md`, `plan.md`, `data-model.md`, `contracts/`, `tasks.md`;
- current state: code/config/runtime artifact thực tế của phase vừa implement.

## Mục tiêu

Cho thấy **hệ thống thực tế vừa được triển khai** ở một phase/mốc, đồng thời giữ ranh giới rõ với intended design.

Diagram candidate:

- implemented component/module map;
- runtime flow;
- technical sequence;
- data flow;
- integration path;
- current-state architecture;
- state/lifecycle implementation khi cần kiểm chứng.

## Quy tắc quan trọng

- Chỉ model phase đã hoàn tất implementation và pass test/QA/validation bắt buộc; không model phase đang code dở như implemented truth.
- Sau modeling, chạy **Project Docs Promotion Check**. Chỉ semantics đã tồn tại trong code/config/runtime và được phase verification xác nhận mới được promote vào `docs/` và project-level diagrams.
- Promotion có thể theo từng phase; không cần đợi toàn feature, nhưng project docs tuyệt đối không được đi trước phase tương ứng.
- Code không được tự trở thành nguồn để sửa intended design.
- Nếu implementation lệch plan/spec:
  - current-state diagram được phép thể hiện lệch;
  - ghi rõ drift;
  - nếu drift là thay đổi thiết kế có chủ đích, cập nhật upstream artifact trước rồi mới đồng bộ intended diagram.
- Không regenerate toàn bộ diagram sau mỗi task nhỏ. Lazy gate chạy trên phase đã hoàn tất trước khi phase kế tiếp bắt đầu; nếu Diagram Check âm thì ghi `no-diagram-needed` thay vì tạo file.

## Output

`FEATURE_DIR/implementation-diagram/`

Ưu tiên tên:

```text
phase-01-foundation.html
phase-02-generation-flow.html
phase-03-runtime.html
```

Nếu một diagram hiện có đại diện cùng viewpoint, cập nhật nó thay vì tạo duplicate.
