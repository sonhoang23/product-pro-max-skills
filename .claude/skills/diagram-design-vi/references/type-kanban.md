# Kanban Board

**Phù hợp nhất cho:** snapshot work-in-progress theo state — cái gì đang queued, cái gì đang move, cái gì stuck và nơi WIP limit bị breach. Đây là một *state census*, không phải flow: kanban board **không có connector nào**. Chính điều này phân biệt nó với swimlane — lane + flow đi xuyên lane, handoff là load-bearing edge — và process — ordered step với directional handoff. Nếu diagram cần một arrow ở bất kỳ đâu, nó không còn là kanban board — dùng swimlane hoặc process thay thế.

## Quy ước layout

- **Tối đa 5 vertical column bằng nhau — rộng 240px — gutter 32px.** Column background `ink @ 0.02`; không border cho column.
- **Header band mỗi column:** column name Geist sans 12px weight 600, anchor trái. **WIP chip** anchor phải — rectangular tag (`rx=2`, **không bao giờ** pill) chứa `n/limit` bằng Geist Mono 8px — hoặc chỉ `n` ở queue/terminal column vốn không có limit. Mọi in-process column đều phải nêu một limit. Hairline `rule` separator nằm ngay dưới header band, span full column width.
- **Cards:** node-box pattern §6 tại `rx=6`, width = column width trừ padding 16px mỗi bên, cao 56px, vertical gap 12px giữa card. Content: title Geist sans 12px weight 600 và sublabel Geist Mono 9px `muted` cho `TICKET-ID · owner`, ví dụ `AVA-214 · nadia`.
- **Drawing order:** background → column fill → header text + WIP chip → header rule → card — mỗi card: box, sau đó left `accent` bar nếu blocked, title, sublabel — → legend.

## Card states — semantic vocabulary của type

Mỗi card render ở chính xác một trong bốn state. Document và dùng đủ bốn khi board có đủ card để thể hiện:

| State | Fill | Stroke | Extra |
|---|---|---|---|
| `default` | white | `ink` | — |
| `blocked` | `accent @ 0.05` | `accent` full opacity dashed `4,4` | accent bar 4px ở left edge card |
| `waiting / external` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` | — |
| `done` | `ink @ 0.05` | `muted` | — |

Các state map trực tiếp vào bảng node-treatment ở SKILL.md §5 (`security` → blocked, `optional` → waiting/external, `store` → done) — board tái sử dụng semantic fill có sẵn của system thay vì tạo treatment mới.

## Over-limit column

Khi card count `n` của column vượt `limit`, stroke và text của WIP chip chuyển sang `accent`. Cùng với một blocked card, đây là toàn bộ budget 2 accent của diagram — không dùng budget ở chỗ khác.

## Complexity budget

- Max 5 column, max 4 card mỗi column, max 12 card tổng.
- Max 2 accent element — over-limit chip tính một, blocked card tính một.
- Vượt budget ở một column → aggregate backlog thành một count card (`+14 more`) thay vì liệt kê mọi item.

## Anti-pattern

- **Vẽ arrow giữa card.** Board cho state, không cho flow — nếu flow cần visible, dùng swimlane hoặc process.
- **Hơn 4 card trong một column.** Aggregate thành count card; đừng để column scroll ra khỏi canvas.
- **Một card mỗi person.** Đó là org chart mặc kanban skin.
- **In-process column không có WIP limit.** Limit là nửa ý nghĩa của type này — column mà work đi *qua* nhưng không có stated limit thì không thể cho thấy nó over budget. Entry queue và terminal column là ngoại lệ: không có gì bị constrain bởi việc giữ thêm done work, nên chúng hiển thị bare count.
- **Accent mọi blocked card.** Một hoặc hai blocked card đọc như signal; cả column toàn accent là noise và xoá focal rule.
- **Column “Done” tăng vô hạn.** Cap nó và ghi archive point trong sublabel hoặc footnote — Done không giới hạn chỉ trở thành Backlog thứ hai.
- **Pill-shaped WIP tag.** Chip là rectangle `rx=2`, khớp type-tag primitive ở §6 — pill đọc như status badge từ design language khác.

## Ví dụ

- `assets/example-kanban.html` — minimal light. Platform-team board: Backlog (3), In progress (4/3, over limit), Review (2/3), Done (2), một blocked card.
- `assets/example-kanban-dark.html` — minimal dark, cùng data.
- `assets/example-kanban-full.html` — full editorial: container framing + 3 summary card khác width + footer.
