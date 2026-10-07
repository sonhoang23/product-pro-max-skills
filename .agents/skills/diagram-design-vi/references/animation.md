# Animation tùy chọn

Animation giải thích một static diagram đã hoàn chỉnh; nó không bao giờ cung cấp meaning còn thiếu. Chỉ load reference này khi motion được yêu cầu rõ ràng hoặc thực sự làm rõ order, accumulation, evaluation, containment hoặc propagation. Nếu không, dùng mode `none` và ship static HTML.

## Modes

Chọn một mode cho mỗi figure bằng `data-motion-mode="none|reveal|step|loop"`.

| Mode | Hành vi | Controls / implementation | Dùng khi |
|---|---|---|---|
| `none` | Figure ổn định hoàn chỉnh | Không JavaScript | Mặc định, print, screenshot, export, reduced-motion fallback với playback control unavailable |
| `reveal` | Một deterministic autoplay run rồi kết thúc ở trạng thái hoàn chỉnh | CSS-only nếu ≤5s; nếu dài hơn dùng scoped controller | Ordered explanation ngắn; không bao giờ auto-replay |
| `step` | Các semantic state có thể pause | Minimal inline JS cho Play, Pause, Replay, Previous, Next | Teaching, comparison, policy trace |
| `loop` | Một decorative token lặp mà không đổi meaning | CSS-only mặc định | Quiet flow hint; cycle ≥3s |

Chỉ `loop` được lặp. Queue state, typing, field value, policy outcome, containment và audit entry dùng `reveal` hoặc `step` và phải kết thúc hoàn chỉnh.

`reveal` là autoplay mode duy nhất được cho phép: nó được chạy một lần ở initial load khi motion đã được yêu cầu explicit, sau đó giữ complete state. Nó không restart khi viewport re-entry hoặc khi không có explicit Replay action.

## Static-first enhancement contract

1. **Source hoàn chỉnh.** Mọi semantic node, label, connector, status và outcome đều visible trong HTML/SVG trước enhancement. Chỉ selector dưới `.motion-ready` mới được phép hide/transform chúng.
2. **Stable capture.** Initial `data-frame="static"`, `?motion=static`, print, no-JS và standalone SVG export expose complete frame và hide control/decorative token. Không capture sau arbitrary delay.
3. **CSS sở hữu presentation.** Dùng CSS transition/keyframe cho appearance/travel. Minimal inline JavaScript chỉ được dùng để bind explicit control, update step/state attribute, schedule deterministic step và update dedicated live-status region. Không fetch, markup injection, path measurement hoặc mutate semantic diagram label/value.
4. **Một clock.** Dùng `--motion-fast: 160ms`, `--motion-step: 480ms`, `--motion-hold: 720ms`, và `--motion-total` ≤ `8000ms`; derive delay từ integer step. Không randomness, spring hoặc transition-event timing.
5. **Order explicit.** Mark item `data-motion-item data-step="N"` cho integer step 1–8. DOM order theo narrative order. Tối đa hai item enter mỗi step.
6. **End state ổn định.** Completion expose mọi item và set `data-frame="end"`. Replay reset về step 0 trước. Pause clear pending timer và resume tiếp tục từ đúng step đó.
7. **State scoped.** Control chỉ operate nearest `[data-motion-root]`; ID, timer, live region và step state không cross figure boundary.
8. **Startup fail-safe.** JavaScript chỉ add `.motion-ready` sau khi control bind và initial render thành công. Script error trước thời điểm đó để complete source vẫn visible.

## Semantic primitives

Mỗi primitive đều có text, count, symbol, pattern hoặc outline ngoài color.

| Primitive | Mechanism | Static / reduced-motion result | Limit |
|---|---|---|---|
| **Path draw** | Decorative duplicate path có `pathLength="1"` và animated dash offset | Base labeled connector vẫn visible | ≤2 path; một active |
| **Staggered reveal** — stage reveal | `data-motion-item` + opacity/translate ≤8px | Mọi stage visible | ≤8 step, 12 item |
| **Queue counter** — queue accumulation | Stable slot; item reveal + visible numeric count | Final queue và count visible | ≤5 item; không reorder |
| **Typing / field population** | Full accessible string; clipped decorative overlay hoặc labeled row reveal | Complete text/field visible một lần | ≤32 typed char hoặc 6 field |
| **Policy evaluation** — rule evaluation | Ordered rule row có text status + current-row outline | Mọi state và outcome visible | 3–6 rule; 2 trace |
| **Flow token** | `aria-hidden` token trên fixed path | Token hidden; connector vẫn còn | Một token; loop ≥3s |
| **Containment** | Reveal child rồi persistent labeled boundary | Child và boundary visible | Một boundary transition |
| **Audit append** | Chronological row reveal; timestamp/sequence ổn định | Complete ordered log visible | ≤5 appended row |

Không animate layout coordinate, connector route, `viewBox`, node dimension hoặc semantic text. Tránh zoom, parallax, bounce, shake, glow, particle và indefinite blink.

```css
:root {
  --motion-fast: 160ms;
  --motion-step: 480ms;
  --motion-hold: 720ms;
  --motion-total: 3600ms; /* five steps × hold; set this per diagram */
  --motion-ease: cubic-bezier(.2,.8,.2,1);
}
.motion-ready [data-motion-item] {
  opacity: .12;
  transform: translateY(8px);
  transition: opacity var(--motion-step) var(--motion-ease),
              transform var(--motion-step) var(--motion-ease);
}
.motion-ready [data-motion-item].is-visible,
.motion-ready[data-frame="end"] [data-motion-item] {
  opacity: 1;
  transform: none;
}
[data-motion-controls][hidden] { display: none !important; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
  [data-motion-item] { opacity: 1 !important; transform: none !important; }
  [data-motion-decorative] { display: none !important; }
  [data-motion-controls] { display: none !important; }
}
@media print {
  [data-motion-controls], [data-motion-decorative] { display: none !important; }
  [data-motion-item] { opacity: 1 !important; transform: none !important; }
}
```

## Interactive controls và keyboard

Mọi interactive `step` figure cung cấp native button cho **Play, Pause, Replay, Previous, Next**, nằm ngoài SVG. Dùng `data-motion-action="play|pause|replay|prev|next"`, target ≥44×44px, visible focus, disabled state cho unavailable action, và `aria-pressed` cho play/pause state.

Khi focus nằm trong motion root: `ArrowRight` tiến, `ArrowLeft` lùi, `Home` reset, `End` complete, `Space` toggle play/pause khi focus không nằm trên native control, và `R` không modifier để replay. Không intercept `R` nếu Control, Command hoặc Alt đang giữ. Không capture key từ input, link hoặc unrelated region. Không move focus khi frame đổi.

Cung cấp visible instruction cùng scoped `role="status" aria-live="polite" aria-atomic="true"`. Giữ live region trong motion root nhưng ngoài `[data-motion-controls]`, để việc hide control ở reduced/static state không hide announcement. Announce user action như “Step 3 of 5: first divergence”; không announce mọi autoplay frame. Control chỉ operate nearest `[data-motion-root]`.

Dùng [`assets/template-motion.html`](../assets/template-motion.html) thay vì invent controller khác. Inline controller của nó là executable implementation contract: copy script body **verbatim**. Skin linter reject controller bị sửa hoặc controller bổ sung, kể cả khi chúng mang `data-diagram-controls`. Thay diagram content và slug-prefixed ID, nhưng giữ controller cùng state/control attribute.

## Reduced motion, color và accessibility

- `prefers-reduced-motion: reduce` khởi tạo ở complete static frame, disable và hide mọi playback control, hide decorative movement, expose `data-motion-state="reduced"` cộng status text playback unavailable. Nó không bao giờ đặt partial-step announcement cạnh complete frame.
- `<title>` và `<desc>` của SVG mô tả complete meaning, không mô tả animation. Interaction instruction vẫn là visible HTML text.
- Decorative overlay có `aria-hidden="true" focusable="false"`. Semantic text tồn tại đúng một lần trong accessibility tree.
- State không bao giờ color-only: policy dùng symbol + `PASS/FAIL/SKIPPED/NOT REACHED`; queue show count; active stage dùng number/label/outline.
- Không gì flash hoặc đổi luminance quá ba lần mỗi giây.

## Complexity và deterministic timing

Motion không tăng static diagram budget: ≤8 semantic step — target 3–6 — ≤12 marked item, ≤2 simultaneous reveal, ≤2 drawn path, một flow-token loop, transition 160–600ms, hold 400–1200ms, translation ≤24px và total autoplay 3–8s.

Declare `data-step-count`; không infer step từ transition event. Set `--motion-total` = step count × `--motion-hold`, giữ trong budget 8 giây. Dùng một `setTimeout` chain cho mỗi root, derive hold từ `--motion-hold`, clear khi Pause/Replay/page hide và ngay sau final step; không bao giờ dùng `setInterval` cho semantic playback. Pause khi `document.visibilityState` thành hidden và không catch-up sau đó.

`?motion=step&step=N` có thể expose exact zero-duration frame cho visual regression **chỉ** khi `N` là non-negative base-10 integer từ 0 tới `data-step-count`; missing, fractional, negative hoặc over-budget value để normal playback nguyên trạng.

Final-state capture contract là synchronous: `?motion=static`, `<html data-motion="static">` hoặc mode `none` expose mọi semantic item, hide control/decorative overlay và set `data-frame="static"`. Chờ `document.fonts.ready` trước capture. Hai capture từ cùng URL, viewport, font và device scale phải pixel-identical; random delay, generated ID, clock và runtime path measurement đều bị cấm.

## Export và verification

PNG/SVG export là static final-state artifact trừ khi user explicit yêu cầu named step. Trước capture, mở `?motion=static`, await `document.fonts.ready`, assert `data-frame="static"`. SVG extraction bỏ HTML control/script; source-visible semantic markup vẫn làm result hoàn chỉnh.

Chạy:

```bash
python3 scripts/verify-motion.py path/to/animated-diagram.html
python3 scripts/test-verify-motion.py
python3 scripts/lint-skin.py path/to/animated-diagram.html
```

Verifier kiểm tra mode/state declaration, contiguous step, motion budget, complete SVG naming, no-JS source visibility, decorative accessibility, full control set, live status, reduced-motion/print CSS, keyboard handling, page-hide pause, bounded static/test override, immediate final-step stop và exact canonical-controller identity. Adversarial test của nó mutate canonical template để chứng minh mỗi failure đều bị reject.

Sau đó verify trong browser:

1. Disable JavaScript: complete diagram vẫn visible và meaningful.
2. Emulate `prefers-reduced-motion: reduce`: final state complete, playback control hidden/disabled, DOM status nói playback unavailable.
3. Chỉ dùng keyboard: Tab tới từng native control; Enter/Space operate; Left/Right/Home/End step mà không move focus.
4. Pause, resume và replay hai lần: ordering và final state identical.
5. Capture `?motion=static` hai lần sau `document.fonts.ready`: pixel stable.
6. Print preview + PNG/SVG export: control/decorative token absent, mọi semantic label/relationship vẫn còn.

## Anti-patterns

- Unrequested autoplay, autoplay ngoài single sanctioned `reveal` run, viewport re-entry hoặc endless semantic loop.
- Blank/partial no-JS hoặc reduced-motion frame.
- Motion dùng để cứu over-dense hoặc unlabeled static diagram.
- Pass/fail, queue fullness hoặc outcome encode chỉ bằng hue.
- Remote script, general application logic, runtime geometry hoặc duplicated semantic text.
- Capture theo wall-clock delay thay vì explicit static override.
