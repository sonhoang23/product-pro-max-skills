# Swimlane

**Phù hợp nhất cho:** quy trình liên chức năng, flow kiểu RACI, vendor handoff, workflow shipping nhiều team.

## Quy ước layout
- Lane ngang (hoặc column dọc) — mỗi actor/team một lane. Gắn label cho từng lane ở margin trái (hoặc phía trên) bằng eyebrow Geist Mono.
- Lane divider: hairline 1px.
- Process step là rectangle nằm trong lane của actor thực hiện; arrow thể hiện flow.
- Handoff (arrow cắt qua lane boundary) là edge quan trọng nhất — có thể dùng coral cho handoff tạo nhiều coupling hoặc latency nhất.
- Không ép mọi lane có cùng số step; lane chỉ có một step vẫn hợp lệ.

## Anti-pattern
- Lane không có label.
- Một step vẽ ngang hai lane (hãy chọn một owner).
- Arrow ngoằn ngoèo qua lại — sắp xếp lại step để flow phần lớn đi thẳng.

## Ví dụ
- `assets/example-swimlane.html` — minimal light
- `assets/example-swimlane-dark.html` — minimal dark
- `assets/example-swimlane-full.html` — full editorial
