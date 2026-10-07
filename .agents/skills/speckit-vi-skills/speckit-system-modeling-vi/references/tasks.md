# Modeling Tasks

## Source of truth

- `tasks.md`;
- `plan.md`;
- `spec.md`;
- technical artifacts liên quan.

## Mục tiêu

Chỉ trực quan hóa execution structure khi `implement` chạy `ensure-model(tasks)` hoặc khi modeling được gọi thủ công, và task list khó quan sát bằng text.

Diagram candidate:

- dependency graph;
- critical path;
- phase flow;
- parallelization map;
- handoff giữa workstream.

Không mặc định tạo timeline/Gantt nếu task không có time semantics.

## Gate

Nếu task list ngắn hoặc dependency đã rõ bằng text/bảng, Diagram Check âm tính và không tạo file.

## Output

`FEATURE_DIR/tasks-diagram/`

Ví dụ: `dependency.html`.
