# Gantt Chart

**Phù hợp nhất cho:** project plan và roadmap — task có start/end date rõ ràng, nhóm thành phase. Dùng khi cần nhìn nhanh temporal overlap, parallel track và milestone sequence.

## Quy ước layout
- **Left label column:** x=20–200 (180px). Task name Geist sans 11px 600. Phase label là eyebrow Geist Mono 7px phía trên mỗi group.
- **Timeline area:** x=200–960 (760px). Time axis trái→phải.
- **Row height:** 40px mỗi task. Bar cao 24px căn giữa row (top padding 8px).
- **Time axis:** label week/month Geist Mono 8px tại x=200+i×pitch, y=56. Hairline separator tại y=64.
- **Phase grouping:** zone rect nhẹ phía sau row của mỗi phase, dùng pattern architecture zone: fill `rgba(45,49,66,0.02)`, stroke `rgba(45,49,66,0.10)`.
- **Focal task bar:** 1 bar dùng accent fill/stroke (key deliverable hoặc critical path). Còn lại muted fill @ 0.15, muted stroke.
- **Today / milestone marker:** vertical dashed line `muted` tuỳ chọn tại x-position tuần hiện tại.

### Task bar pattern

```svg
<!-- Non-focal task -->
<rect x="X_start" y="ROW_Y+8" width="DURATION_PX" height="24" rx="4"
      fill="rgba(79,93,117,0.15)" stroke="#4f5d75" stroke-width="1"/>
<text x="X_start+8" y="ROW_Y+25" fill="#2d3142" font-size="10" font-weight="600"
      font-family="'Geist', sans-serif">Task name</text>

<!-- Focal task -->
<rect x="X_start" y="ROW_Y+8" width="DURATION_PX" height="24" rx="4"
      fill="rgba(235,108,54,0.12)" stroke="#eb6c36" stroke-width="1"/>
<text x="X_start+8" y="ROW_Y+25" fill="#eb6c36" font-size="10" font-weight="600"
      font-family="'Geist', sans-serif">Key task</text>
```

Duration pixel: `(end_week - start_week) × pitch`. Pitch = timeline_width / total_weeks.

## Anti-pattern
- Hơn 12 task — tách sub-plan hoặc collapse thành phase-level view.
- Hơn 5 parallel track mỗi phase.
- Dependency arrow giữa task ở v1 — chỉ thêm khi thiết yếu; dùng annotation primitive cho label.
- Start/end date nằm trong bar label — đặt ở x-axis hoặc tooltip comment.
- Visual weight bằng nhau cho mọi bar — focal task phải nổi bật.

## Ví dụ
- `assets/example-gantt.html` — minimal light
- `assets/example-gantt-dark.html` — minimal dark
- `assets/example-gantt-full.html` — full editorial
