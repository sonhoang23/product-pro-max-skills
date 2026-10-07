# User Story Map

**Phù hợp nhất cho:** Jeff Patton user story map — trả lời “whole story là gì, và chúng ta cắt first release ở đâu?” Narrative order chạy trái sang phải; priority chạy trên xuống dưới. **Release cut** là editorial point của diagram: map không có cut chỉ là backlog đặt trên grid.

Đây không phải **Kanban** cũng không phải **User journey**, và sự phân biệt này là load-bearing:

- **Kanban** cho *state* — column là Todo/Doing/Done, không có narrative order và không có gì để slice.
- **User journey** cho *cảm xúc của một persona* qua các stage bằng sentiment curve.
- **Story map** không có state cũng không có sentiment. Column là **narrative order**, row là **release slice**. Nếu không slice release, dùng một trong hai type trên.

## Quy ước layout

Vertical stack từ trên xuống:

1. **Backbone** — tối đa 5 activity theo narrative order trái→phải, dạng header card rộng 200px (`rx=6`, fill `ink @ 0.05`, stroke `muted`). Mỗi card: activity name bằng Geist sans 12px weight 600, phía trên là eyebrow Geist Mono 8px uppercase tracked (`ACTIVITY 1` … `ACTIVITY 5`). Gutter 24px giữa card.
2. **Walking skeleton row** — ngay dưới mỗi activity, các user *step* của nó dưới dạng card nhỏ hơn (`rx=4`, cao 32px, fill trắng, stroke `ink`), Geist sans 12px. Một hoặc hai step mỗi activity; reserve chỗ cho hai để bottom của mọi activity row vẫn align dù activity chỉ có một step.
3. **Release slices** — horizontal band dưới skeleton row, mỗi band là full-width lane có label Geist Mono 8px uppercase tracked (`MVP`, `RELEASE 2`, `LATER`) nằm trong left margin 96px. Band background xen kẽ `ink @ 0.02` / none. Bên trong mỗi band, story card (`rx=4`, cao 48px) nằm trong column activity tương ứng: story title Geist sans 12px weight 600, cộng estimate/ticket sublabel Geist Mono 9px, ví dụ `RPT-114 · 3pt`. Khi bất kỳ slice nào có gap — activity không có card ở row đó — thêm column separator hairline `rule` (0.8px, dashed `4,4`, opacity 0.10) chạy từ ngay dưới backbone xuống bottom của slice cuối, vẽ trước card — nếu không, gappy grid trông như card rải rác thay vì map theo activity.
4. **Release cut line** — full-width horizontal rule `accent` 1.5px ngay dưới MVP band, có masked label Geist Mono 8px `RELEASE CUT` ở right end. Đây là accent element thứ nhất.
5. **Legend** — horizontal strip ở dưới cùng theo global rule — hairline separator phía trên — gồm một swatch cho default story card, một cho highest-risk treatment và một cho release-cut line.

## Focal rule

Chính xác 2 accent element: release cut line cùng label `RELEASE CUT` của nó — tính là một — và story card rủi ro nhất duy nhất — vẽ với fill `accent @ 0.05`, stroke `accent` dashed `4,4`, kèm rectangular tag nhỏ `RISK` (`rx=2`, khớp type-tag primitive) — tính là element còn lại. Không thứ gì khác trên map dùng `accent`.

## Complexity budget

- Max 5 activity, max 3 release slice, max 12 story card tổng, max 4 card mỗi slice.
- Max 2 accent element — release cut tính một, riskiest card tính một.
- Vượt budget trên một activity hoặc slice → split thành một map mỗi activity, hoặc collapse slice thành count card thay vì list mọi item.

## Anti-pattern

- **Không release cut.** Map không có cut line là backlog trên grid, không phải map — cut chính là điểm cốt lõi.
- **Column order theo priority thay vì narrative sequence.** Backbone là story, trái→phải theo thứ tự user trải nghiệm — không phải ranked list.
- **Story card là feature, không phải user-visible outcome.** “Add a chart” là story; “Refactor the charting service” không phải — nó thuộc backlog ticket, không phải map.
- **Slice đặt theo date thay vì outcome.** `MVP` / `RELEASE 2` / `LATER` mô tả scope; `Q3` / `Q4` mô tả calendar và drift ngay khi schedule trượt.
- **Hơn 3 slice.** Sau MVP, next và later, không ai còn tin thứ tự — collapse tail thành “Later.”
- **Trộn hai persona trong một map.** Một map mỗi persona, giống user journey.
- **Thêm state column.** Nó biến thành kanban board — type này không có state.
- **Thêm sentiment curve.** Nó biến thành user journey — type này không có feelings axis.

## Ví dụ

- `assets/example-story-map.html` — minimal light. *Reporting, first release*: bốn activity (`Find the data`, `Build the report`, `Share it`, `Trust it`), slice MVP/Release 2/Later, release cut dưới MVP, `Row-level permissions` được flag là riskiest story.
- `assets/example-story-map-dark.html` — minimal dark, cùng data.
- `assets/example-story-map-full.html` — full editorial: container framing + 3 summary card khác width + footer.
