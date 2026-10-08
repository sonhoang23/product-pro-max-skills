# State Machine

**Phù hợp nhất cho:** finite state logic — trạng thái order, auth state, vòng đời connection, form wizard, trạng thái job queue.

## Quy ước layout
- State là rounded rectangle (`rx=8`), label bằng Geist.
- **Start**: filled ink dot (`r=6`). **End**: ringed dot (outer `r=8` outline, inner filled `r=5`).
- Transition: curved arrow có label Geist Mono theo dạng `event [guard] / action` (bỏ phần không cần).
- Self-loop cong phía trên state.
- Định hướng theo dominant flow (trái→phải hoặc trên→dưới); sắp xếp lại trước khi để transition cắt nhau.
- Dùng coral cho state người đọc cần chú ý — thường là error state hoặc “happy completion”.

## Anti-pattern
- Số transition lớn hơn số state × 2 → nhiều khả năng nên là hai state machine.
- Transition “From any state” được vẽ từ mọi state — thay bằng một annotation duy nhất (`* → Error on timeout`).
- Transition không có label (điểm cốt lõi là *điều gì kích hoạt transition*).

## Ví dụ
- `assets/example-state.html` — minimal light
- `assets/example-state-dark.html` — minimal dark
- `assets/example-state-full.html` — full editorial
