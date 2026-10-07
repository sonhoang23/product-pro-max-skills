# Org Chart / Responsibility Map

**Phù hợp nhất cho:** human team, agent team, support escalation map, role ownership, routing map và hierarchy nơi người đọc cần biết *ai sở hữu việc gì* thay vì chỉ parent → child.

Dùng **Org Chart** thay **Tree** khi node là người, agent, team, role hoặc accountable owner. Tree thể hiện generic hierarchy; org chart thể hiện responsibility, invocation path và coverage gap.

## Quy ước layout
- Root owner/front door ở top center. Dùng một coral focal node cho người/team/agent nhận ambiguous work.
- Tier 1 node là department, pod, queue hoặc primary routing bucket, căn ngang.
- Tier 2 là responsible owner/specialist. Hơn 8 specialist thì nhóm dưới pod node.
- Orthogonal connector: vertical drop → horizontal bus → vertical drop. Không diagonal.
- Mỗi node nên trả lời ba câu khi có chỗ: **Name** bằng Geist sans; **How to invoke** (Slack handle, queue, issue prefix, trigger) bằng Geist Mono; **Scope** gồm 2–4 ownership word ngắn.
- Owner non-Slack/chưa live dùng dashed optional styling, không ẩn.
- Escalation/approval rule nằm trong side callout/footer strip, không thành org node thêm.

## Node treatment
- **Front door / command center:** focal (`accent-tint` + `accent`).
- **Team / pod / department:** backend (white + `ink`).
- **Individual agent / owner:** store hoặc external theo active state.
- **Gap / needs setup:** optional dashed.
- **Approval gate:** security, tách khỏi reporting hierarchy.

## Complexity budget
- Max 12 visible org node; hơn thì overview + detail theo pod.
- Max depth 4 tier.
- Max direct report dưới một parent: 5; hơn thì thêm grouping node.
- Max coral node: 1.
- Max side callout: 2.

## Anti-pattern
- Dùng swimlane khi câu hỏi thực là “ai làm gì?”.
- Mọi người/agent là box giống nhau.
- Nhồi full job description vào node.
- Hiển thị agent chưa wired như owner active bình thường.
- Lặp Slack handle trong body paragraph khi sublabel có thể mang invocation path.
- Legend nổi trong org area.

## Ví dụ
- `assets/example-org-chart.html` — minimal light
- `assets/example-org-chart-dark.html` — minimal dark
- `assets/example-org-chart-full.html` — full editorial
