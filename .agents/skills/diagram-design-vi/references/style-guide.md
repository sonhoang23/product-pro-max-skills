<!-- diagram-design-profile
name: Oh My Slide Product
slug: oh-my-slide-product
source-url: none
created: 2026-09-27
updated: 2026-09-27
notes: Neutral technical documentation skin until product branding is finalized
-->
# Style Guide

**Semantic contract + fallback skin.** File này định nghĩa ý nghĩa của color/typography/token và là fallback khi project không có shared theme CSS. Nếu `.diagram-design` dùng `theme:`, file CSS được trỏ tới mới là **source of truth cho giá trị visual thực tế**; xem [`project-theme.md`](project-theme.md).

Current skin là **Oh My Slide Product — Neutral Technical**: nền trung tính, tương phản rõ, một accent xanh duy nhất và typography ưu tiên khả năng đọc tài liệu kỹ thuật. Đây là skin tạm thời cho project cho tới khi brand chính thức được chốt.

Để tạo skin riêng từ website URL, xem [`onboarding.md`](onboarding.md).

### Khi project dùng shared theme CSS

Không copy các giá trị hex/font/radius từ bảng dưới vào từng HTML. Map semantic role sang CSS variable:

| Semantic role | Project variable |
|---|---|
| `paper` | `--diagram-paper` |
| `paper-2` | `--diagram-paper-2` |
| `ink` | `--diagram-ink` |
| `muted` | `--diagram-muted` |
| `soft` | `--diagram-soft` |
| `rule` | `--diagram-rule` |
| `rule-solid` | `--diagram-rule-solid` |
| `accent` | `--diagram-accent` |
| `accent-tint` | `--diagram-accent-tint` |
| `link` | `--diagram-link` |

Typography tương ứng dùng `--diagram-font-title`, `--diagram-font-sans`, `--diagram-font-mono`. Các value trong bảng bên dưới chỉ là fallback/reference cho profile mode.

---

## Tokens

### Semantic roles

Mọi token được tham chiếu bằng **semantic role**, không bằng hex value. Type reference (`type-*.md`) và SKILL.md nói `accent`, không nói `#f7591f`.

| Role | Mục đích | Default (light) | Default (dark) |
|---|---|---|---|
| `paper` | Page background, default node fill | `#f7f7f5` | `#111418` |
| `paper-2` | Diagram container bg, secondary fill | `#ffffff` | `#1b1f24` |
| `ink` | Primary text, primary stroke | `#1f2328` | `#f0f3f6` |
| `muted` | Secondary text, default arrow stroke | `#57606a` | `#b1bac4` |
| `soft` | Sublabel, boundary label | `#6e7781` | `#8c959f` |
| `rule` | Hairline border | `#d0d7de` | `rgba(240,243,246,0.20)` |
| `rule-solid` | Stronger border, baseline | `#afb8c1` | `#30363d` |
| `accent` | Focal / tối đa 1–2 mỗi diagram | `#2563eb` | `#60a5fa` |
| `accent-tint` | Fill cho accent-bordered box / title highlight | `rgba(37,99,235,0.12)` | `rgba(96,165,250,0.16)` |
| `link` | HTTP/API call, external arrow | `#0969da` | `#58a6ff` |

> **Nguồn project palette:** neutral technical palette dành cho tài liệu kiến trúc, flow và product documentation. Accent xanh chỉ dùng cho focal node/link; không đại diện cho brand chính thức của sản phẩm.

> **Contrast baseline:** accent tint `0.18` là default cho social. Node/card phải tách được khỏi `paper` bằng `paper-2` hoặc ink tint rõ ràng; border node tối thiểu `1.5px`, focal border `2px`; sublabel cần đọc được dùng `muted`, không dùng `soft` nếu không phải boundary label.

### Social portrait legibility

Áp dụng cho LinkedIn `960×1200`, Story `1080×1920` và mọi ảnh được xem nhỏ trên feed:

- `paper` và `paper-2` phải tạo khác biệt nhìn thấy; không dùng hai màu nền gần như giống nhau cho node và canvas.
- Text phụ, arrow label và mobile link dùng `muted`; `soft` chỉ dành cho eyebrow/boundary label.
- Node thường dùng border tối thiểu `1.5px`, `border-radius: 6–8px`, nền `paper-2`.
- Focal node dùng `accent-tint` + `accent` border `2px`; tối đa 1–2 focal node.
- Mobile zone nên có border `1.5px`; zone kết luận được phép dùng accent tint rất nhẹ (`0.05–0.08`).
- Tiêu đề node tối thiểu `24px` ở social-scale; sublabel tối thiểu `15px`; browser phone lần lượt tối thiểu `17px` và `12px`.
- Nếu diagram còn vùng trắng vô nghĩa, tăng scale/spacing/callout trước khi thêm decoration.
- Luận điểm trung tâm nên có callout riêng, không để chìm trong footer nhỏ.

> **Lưu ý:** các example HTML pre-baked trong `assets/` được xây dưới skin cũ hơn. Regenerate chúng theo current `style-guide.md` là task v5.1. Diagram mới do skill tạo sẽ dùng token ở trên.

### Inversion rule (light → dark)

Mọi `rgba(24,23,20, X)` ở light trở thành `rgba(247,243,235, X)` ở dark. Giữ nguyên opacity, đảo RGB. Accent dịch sang `#ff7849` trên dark paper.

### Series palette — chỉ multi-series chart type

Một tập nhỏ color desaturated theo editorial tone dành cho chart type thực sự cần phân biệt nhiều entity chồng lên nhau — hiện tại là **radar**. Quy tắc “1 focal” vẫn giữ — `accent` dành riêng cho focal series; palette dưới đây cover phần còn lại.

| Token | Light | Dark | Ghi chú |
|---|---|---|---|
| `series-1` | `#7c8f6f` (sage) | `#9caf8f` | Non-focal series |
| `series-2` | `#5e7a9b` (dusty-blue) | `#82a0c0` | Non-focal series |
| `series-3` | `#b8915a` (mustard) | `#d3ad7a` | Non-focal series |
| `series-4` | `#9c6b50` (rust-brown) | `#b88670` | Non-focal series |
| `series-5` | `#6e6479` (slate) | `#8d8298` | Non-focal series |

Fill ở opacity `0.18` light, `0.22` dark; stroke dùng full color. **Không backfill các token này sang non-chart type** — architecture, swimlane v.v. tiếp tục dùng muted-ink variant. Series palette là opt-in cho diagram nơi overlapping shape cần distinguishable color, không phải giấy phép để thêm màu ở chỗ khác.

### Terminal skin — opt-in alternate

Palette self-contained cho terminal-window primitive — xem [primitive-terminal.md](primitive-terminal.md) — một CLI-chrome register cho dev-tool post và technical social card. Nó không thay default skin ở trên, không bị onboarding tác động; đây là fixed skin thứ hai được opt-in theo từng diagram.

| Token | Hex | Mục đích |
|---|---|---|
| `terminal-page` | `#0a0a0a` | Page background phía sau window |
| `terminal-paper` | `#141414` | Window body, node fill |
| `terminal-bar` | `#1b1b1b` | Titlebar strip |
| `terminal-border` | `#2b2b2b` | Window border, hairline |
| `terminal-ink` | `#f5f5f5` | Primary text/stroke, cùng white-smoke với default `ink` |
| `terminal-muted` | `#9a9a9a` | Secondary text, sublabel, ring stroke |
| `terminal-soft` | `#5c5c5c` | Tertiary — inactive dot, spoke |
| `terminal-accent` | `#ff5a36` | Accent duy nhất — focal station, prompt sign, active dot |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | Fill cho accent-bordered box |

**Quy tắc 1 accent vẫn áp dụng.** Mọi thứ không phải `terminal-ink` hoặc `terminal-muted`/`terminal-soft` nên dùng `terminal-accent` — không bao giờ đưa vào hue thứ hai.

---

## Typography

| Role | Family | Size | Weight | Dùng cho |
|---|---|---|---|---|
| `title` | Noto Serif (Vietnamese-safe) | 1.75rem | 400 | Page H1 |
| `node-name` | Inter (sans) | 12px | 600 | Human-readable label |
| `sublabel` | Geist Mono | 9px | 400 | Port, protocol, URL, field type |
| `eyebrow` | Geist Mono | 8–13px | 600, tracked 0.08em, uppercase | Type tag, axis label; tăng ở social |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | Arrow annotation |
| `callout` | Noto Serif *italic* | 14px | 400 | Chỉ editorial aside |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Noto+Serif:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
```

### Korean labels

Noto Serif trong cấu hình Latin/Vietnamese không được coi là bảo đảm có Hangul. Một Korean `<text>` tự mở rộng family — không bao giờ đổi skin:

```svg
<text font-family="'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif">결제 서비스</text>
```

Diagram tiếng Việt dùng Noto Serif cho title/callout theo mặc định. Label Hangul cần face Hangul riêng được user cung cấp và phê duyệt.

Google `css2` endpoint slice Korean theo unicode-range, nên diagram chỉ có vài Korean label chỉ download những slice được dùng. Bốn template chứa cả hai face vì diagram mới có thể chứa Hangul; shipped example chỉ Latin giữ link ngắn hơn vì file không Hangul không có gì cần resolve.

**Width budget.** Đo theo từng character, không theo script: **mọi Unicode wide/full-width character tốn 1em, mọi character khác tốn Latin advance của face** — 0.60em sans, 0.62em mono — và nonspacing/enclosing mark không tốn width. Cộng trên toàn string rồi nhân font size để ra text width, sau đó thêm padding và round box **lên** multiple of 4 kế tiếp. `verify-treemap.py` enforce chính xác text-width contract này cho treemap cell label; padding/rounding là authoring convention, các type khác không có automatic check nên bạn phải tự giữ budget.

Đếm theo script là cái bẫy. `주문 v2.1` có hai full-width syllable và năm narrow character; công thức chỉ đếm Hangul/Latin letter/space sẽ bỏ `2`, `.`, `1` và size box như thể string chỉ có bốn trên bảy character. Mỗi rendered character đều tốn gì đó — đo theo character, không theo script.

Ba quy tắc từ Hangul metrics:

- **Sublabel giữ Latin.** Port, protocol, field type và URL vốn là Latin — giữ `Geist Mono`. Hangul trong mono sublabel 9px không đọc được và không có mono face fallback phù hợp.
- **Floor 12px.** Hangul bị bệt dưới 12px. Nếu Korean name không fit ở 12px, cắt name — không shrink type.
- **Arrow label, eyebrow và legend text đổi register.** Các slot này bình thường là Geist Mono 7–8px, uppercase và tracked, nhưng Hangul không có face/legibility tương ứng. Korean label trong các slot đó dùng sans 12px weight 500, không tracking, không uppercase transform; mask rect tăng lên 16px cao, width theo budget trên và vẫn round multiple of 4. Latin label trong cùng diagram giữ mono treatment.

**Load-bearing rule:** Mono dành cho *technical* content như port, command, URL, field type. Name dùng Inter sans. Page title và annotation callout dùng Noto Serif. **Không bao giờ dùng JetBrains Mono** như blanket "dev" font.

---

## Stroke, radius, spacing

| Token | Value | Dùng cho |
|---|---|---|
| `stroke-thin` | `0.8` | Tag-box outline, leaf node |
| `stroke-default` | `1` | Phần lớn stroke |
| `stroke-strong` | `1.2` | Emphasis stroke |
| `radius-sm` | `4` | Small tag |
| `radius-md` | `6` | Node box |
| `radius-lg` | `8` | Container, ring |
| `grid` | `4` | Mọi coord, size và gap chia hết cho 4 — hard rule |

---

## Node type → treatment

Các tổ hợp semantic role; type spec tham chiếu chúng bằng tên.

| Type | Fill | Stroke |
|---|---|---|
| `focal` (tối đa 1–2) | `accent-tint` | `accent` |
| `backend` | `paper-2` | `ink @ 0.72`, 1.2px |
| `store` | `ink @ 0.08` | `ink @ 0.62`, 1.2px |
| `external` | `ink @ 0.06` | `ink @ 0.48`, 1.2px |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## Tùy biến skin

Bốn lựa chọn:

1. **Chạy onboarding** — xem [`onboarding.md`](onboarding.md). Nếu project dùng marker `theme:`, skill update shared theme CSS; nếu không mới rewrite file này/profile.
2. **Edit thủ công** — đổi hex value trong table trên. Chạy pre-output taste gate sau đó để verify accent vẫn đọc như "focal" trên paper color mới.
3. **Brand handoff** — paste design-token JSON hiện có vào section mới ở đây và map token sang semantic role trên.
4. **Client profiles** — save/switch named skin hoặc bind skin vào project bằng [`profiles.md`](profiles.md).

### Constraint — không được phá

- **Contrast:** `ink` phải đạt WCAG AA trên `paper`. `muted` phải đạt AA trên `paper` cho text 11px+.
- **Một accent:** chọn một color cho `accent`. Hai accent xóa focal signal.
- **Không rainbow palette:** nếu brand ship 8 color, chọn 3 — paper, ink, accent. Phần còn lại trở thành `muted` variant.
- **Title + sans + mono:** tối đa ba family. Title/callout dùng `--diagram-font-title`; body/node dùng `--diagram-font-sans`; technical label dùng `--diagram-font-mono`. Không hardcode một family cụ thể vào type reference.
- **Paper là warm-neutral, không pure white:** pure white làm design sterile. Chọn cream, bone hoặc light grey có chút warmth.
- **Dot pattern là optional, không default:** 22×22 dot pattern là opt-in "dotted paper" variant, phù hợp long-form editorial hero. Default background là clean `paper` fill, không pattern. Khi enable, pattern khoảng 10% opacity của `ink` trên `paper` — nhìn thấy nhưng yên.
- **Container mặc định clean:** diagram nằm trực tiếp trên page paper, không secondary container background/border. Framed variant — `paper-2` bg + `rule` border + radius 8 + padding — là opt-in cho card-heavy layout; không dùng mặc định vì chrome thêm sẽ cạnh tranh với figure.
