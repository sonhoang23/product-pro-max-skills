# Modeling Converge

## Source of truth

- `spec.md`;
- `plan.md` và technical artifacts;
- `tasks.md` gồm các convergence task mới;
- code/current implemented state;
- constitution.

## Mục tiêu

Final converge gate luôn chạy Diagram Check trước khi command tuyên bố hoàn tất; chỉ trực quan hóa khoảng cách giữa intended state và current implemented state khi visual có giá trị để người đọc thấy:

- phần nào đã hoàn tất;
- phần nào mới một phần;
- phần nào còn thiếu;
- dependency của remaining work;
- convergence task nào xử lý gap nào.

Diagram candidate:

- intended vs current map;
- gap map;
- remaining dependency graph;
- current-state system map.

## Quy tắc

- Không biến diagram thành nguồn task mới độc lập.
- Gap phải trace về requirement/plan/task.
- Nếu converge không tìm thấy gap và mental model không đổi, không tạo diagram mới chỉ để báo “clean”.

## Output

`FEATURE_DIR/converge-diagram/`

Ví dụ:

- `current-state.html`;
- `gap-map.html`.
