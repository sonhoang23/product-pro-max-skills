# Timeline

**Phù hợp nhất cho:** lịch sử release, project milestone, incident timeline, roadmap, trực quan hoá changelog.

## Quy ước layout
- Baseline hairline ngang qua giữa (`stroke-width=1`).
- Tick mark tại boundary thời gian (quarter, month, sprint), date label ở dưới bằng Geist Mono.
- Event: filled circle nhỏ (`r=4`) trên baseline. Label xen kẽ trên/dưới để tránh va chạm, nối với circle bằng hairline drop 1px.
- Major milestone: coral circle (`r=6`) + label Geist bold.
- Time scale phải trung thực: nếu interval không đều, khoảng cách circle cũng phải không đều. Không giả linear spacing chỉ để đẹp. Nếu một vùng quá dày, thể hiện axis break rõ ràng.

## Anti-pattern
- Event cách đều nhau dù thời gian thực không đều.
- Thiếu axis label (“đơn vị này là gì?”).
- Label chen chúc mà không offset theo chiều dọc — không đọc được.

## Ví dụ
- `assets/example-timeline.html` — minimal light
- `assets/example-timeline-dark.html` — minimal dark
- `assets/example-timeline-full.html` — full editorial
