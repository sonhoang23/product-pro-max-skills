# Flowchart

**Phù hợp nhất cho:** logic quyết định, thuật toán, branching flow hướng tới người dùng (“Tôi có nên…?”), routing onboarding, cây support-triage.

## Quy ước layout
- Shape biểu thị type, không phải màu:
  - **Oval** (`rx=20`) — start / end
  - **Rectangle** (`rx=6`) — step / action
  - **Diamond** — decision (≤3 exit)
  - **Small filled ink dot** (`r=4`) — merge point nơi các branch nhập lại
- Flow chạy từ trên xuống. Từ diamond, exit theo quy ước: Yes sang phải, No xuống dưới — nhưng vẫn phải gắn label cho mọi outgoing arrow.
- Dùng coral cho happy path *hoặc* cho một decision có hệ quả lớn nhất — không dùng cho mọi decision.
- Nếu hai arrow buộc phải cắt nhau, dùng một arc jump nhỏ trên một đường để điểm cắt dễ đọc.

## Anti-pattern
- Dùng fill color để biểu thị node type (shape đã làm việc đó).
- Decision diamond có 4+ exit — refactor thành các diamond lồng nhau.
- Decision branch không có label.

## Ví dụ
- `assets/example-flowchart.html` — minimal light
- `assets/example-flowchart-dark.html` — minimal dark
- `assets/example-flowchart-full.html` — full editorial
