# Sequence

**Phù hợp nhất cho:** request/response flow, protocol exchange, tương tác nhiều actor theo thời gian, API call trace, incident reconstruction, auth/token refresh path có branch.

## Quy ước layout
- Actor là box trong horizontal row phía trên.
- **Lifeline:** dashed vertical line từ actor xuống bottom.
- Message: horizontal arrow giữa lifeline; thời gian chạy top→down.
- **Activation bar:** narrow rectangle (`w=8`, muted fill, stroke hairline 0.8) trên lifeline trong khoảng actor giữ control. Stack cho nested call.
- Self-message: U-shaped loop ngắn quay lại cùng lifeline; label bên phải loop.
- Return message: stroke **dashed** + marker **filled** (không open). Ưu tiên muted; có thể match originating call color khi pairing multi-hop stack. Headline success có thể solid coral.
- Coral cho primary success response hoặc headline message — một, tối đa hai. Actor focal stroke không tính vào coral message budget.
- Khi flow **branch** (valid/invalid token, retry, optional step), dùng **combined fragment** frame — không tạo if/else arrow cluster thả nổi.

## Message kind

| Kind | Stroke | Marker | Khi dùng |
|---|---|---|---|
| Call (sync) | solid muted hoặc link-blue | filled | Request chờ reply |
| Return | **dashed** muted (hoặc match call color) | filled | Reply cho sync call — không solid |
| Async / fire-and-forget | dashed muted | **open** arrowhead | Beacon, event, one-way notify |
| Headline success | solid accent (≤1–2 message) | accent filled | Primary happy-path response בלבד |

### Open arrowhead (async)

Định nghĩa một lần trong `<defs>` và chỉ dùng fire-and-forget:

```svg
<marker id="arrow-open" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polyline points="0 0, 8 3, 0 6" fill="none" stroke="#4f5d75" stroke-width="1.2"/>
</marker>
```

Dark mode: stroke `#bfc0c0`. Không fill open marker — hollow head là async signal. Return message vẫn giữ **filled** marker dù dashed.

## Combined fragment (`alt` / `opt` / `loop`)

Dùng rectangular **frame** chỉ span lifeline tham gia branch. Operator label Geist Mono uppercase trong tab nhỏ top-left. Thời gian vẫn top→down trong frame.

### Frame primitive

```svg
<!-- Frame: light ink wash + hairline. Label tab top-left. -->
<rect x="X" y="Y" width="W" height="H" rx="4"
      fill="rgba(45,49,66,0.02)" stroke="rgba(45,49,66,0.22)" stroke-width="1"/>
<!-- Operator tab -->
<rect x="X" y="Y" width="40" height="16" rx="2"
      fill="#f5f5f5" stroke="rgba(45,49,66,0.22)" stroke-width="1"/>
<text x="X+20" y="Y+12" fill="#4f5d75" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle"
      letter-spacing="0.12em">ALT</text>
```

Dark mode: fill của frame `rgba(245,245,245,0.04)`, stroke `rgba(245,245,245,0.22)`, tab fill = `paper` dark (`#2d3142`), tab text = `muted` dark (`#bfc0c0`).

### Operator

| Operator | Region | Divider | Guard label |
|---|---|---|---|
| `opt` | 1 | none | `[if condition]` dưới tab, Geist Mono 8px |
| `alt` | **2 max** | dashed horizontal hairline qua frame | `[guard]` region 1; `[else]` hoặc second guard region 2 |
| `loop` | 1 | none | `[for each item]` hoặc `[retry ≤ 3]` dưới tab |

### Guard + divider primitive

```svg
<!-- Guard: left-aligned inside the frame, mono -->
<text x="X+12" y="GUARD_Y" fill="#4f5d75" font-size="8"
      font-family="'Geist Mono', monospace" letter-spacing="0.04em">[token valid]</text>

<!-- alt region divider -->
<line x1="X+8" y1="DIV_Y" x2="X+W-8" y2="DIV_Y"
      stroke="rgba(45,49,66,0.20)" stroke-width="1" stroke-dasharray="4,3"/>
```

### Quy tắc fragment layout
- Frame left/right inset ≥12px từ center lifeline ngoài cùng tham gia.
- ≥24px giữa consecutive message y-level trong region.
- Guard nằm ~20px đầu dưới tab; first message ≥24px dưới guard baseline.
- Divider y trên 4px grid; clear ≥16px khỏi message trên/dưới.
- Nested fragment: **max 1 level**. Ưu tiên hai diagram thay deep nesting.
- Mặc định **một** fragment mỗi diagram. Fragment thứ hai chỉ khi cả hai vẫn trong budget.
- Coral chỉ trên **một** headline success message toàn diagram. Không coral cả hai `alt` branch.

### Ngoài phạm vi — không tự bịa
- `par`, `critical`, `break`, `ref` và UML operator khác.
- Participant create/destroy, found/lost message, duration timing bar.

Combined-fragment budget giữ operator `alt` tối đa hai region.

## Complexity budget riêng Sequence
- Max lifeline: 5.
- Max message arrow: 12.
- Max combined fragment: 1 mặc định; 2 chỉ nếu mỗi cái là single-region `opt`/`loop`.
- Max `alt` region: 2.
- Max fragment nesting depth: 1.
- Max coral element: 2 (ưu tiên 1 với fragment diagram).

Vượt → split happy-path overview + failure/refresh detail.

## Lifeline primitive
```svg
<line x1="CX" y1="TOP" x2="CX" y2="BOTTOM"
      stroke="rgba(45,49,66,0.20)" stroke-width="1" stroke-dasharray="3,3"/>
```

## Activation bar primitive
```svg
<rect x="CX-4" y="TOP" width="8" height="H"
      fill="rgba(45,49,66,0.06)" stroke="#4f5d75" stroke-width="0.8"/>
```

## Anti-pattern
- Message arrow chỉ lên trên (đảo ngược thời gian).
- Activation bar không đóng.
- Label nằm trên lifeline khác.
- Dùng swimlane-style lane thay lifeline.
- Vẽ `if/else` bằng arrow cluster không fragment frame.
- Nested `alt` trong `alt`.
- Fragment operator dùng Geist sans — phải mono `ALT` / `OPT` / `LOOP`.
- Coral trên cả hai `alt` branch.
- Frame bao actor không có message trong fragment.
- Filled arrowhead trên async fire-and-forget.
- Open arrowhead trên return message.

## Ví dụ
- `assets/example-sequence.html` — minimal light (cold-cache happy path)
- `assets/example-sequence-dark.html` — minimal dark
- `assets/example-sequence-full.html` — full editorial
- `assets/example-sequence-oauth.html` — bearer call + `alt` refresh (light)
- `assets/example-sequence-oauth-dark.html` — same special, dark
- `assets/example-sequence-oauth-full.html` — same special, full editorial
