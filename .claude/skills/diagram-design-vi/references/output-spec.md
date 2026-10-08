# Output spec cho import draw.io — format × size × detail × audience

Bốn "dial" quyết định một diagram được import sẽ trở thành gì. Hãy đặt chúng **trước khi vẽ lại** — chúng thay đổi deliverable, layout, type ramp, số node và cách dùng từ, nên cố lắp chúng vào sau khi đã vẽ đồng nghĩa với phải vẽ lại.

| Dial | Câu hỏi mà nó trả lời | Mặc định |
|---|---|---|
| **Format** | File này sẽ đi tới đâu? | `html` |
| **Size** | Canvas lớn đến mức nào, và người đọc ở xa bao nhiêu? | `doc-inline` |
| **Detail level** | Giữ lại mọi element hay nén bớt? | `balanced` |
| **Audience** | Cách diễn đạt nên kỹ thuật đến mức nào? | `mixed` |

Hãy suy ra những lựa chọn đã rõ từ yêu cầu, ví dụ "for my deck" ngụ ý một slide preset. Với những ambiguity có ảnh hưởng đáng kể còn lại, hỏi một câu ngắn gọn. Nếu người dùng không quan tâm, dùng các default ở trên và nói rõ bạn đã dùng lựa chọn nào.

---

## 1. Format

| Format | Deliverable | Giữ lại | Bỏ đi |
|---|---|---|---|
| `html` | `.html` tự chứa (mặc định) | header, diagram, summary cards, footer, live fonts | không gì cả |
| `svg` | `.svg` cạnh source | node `<svg>`, vector text | editorial wrapper; font có thể bị substitute trong tool offline |
| `png` | `.png` ở `device_scale_factor` | pixel đúng như browser render | khả năng edit vector |
| `html+png` | cả hai | — | — |

Luôn tạo HTML trước — `svg` và `png` được sinh **từ HTML** qua [`export.md`](export.md). Không bao giờ hand-author SVG file trực tiếp; HTML là source of truth và là artifact duy nhất mà taste gate trong SKILL.md §9 được viết để kiểm tra.

Chọn theo destination:

| Destination | Format | Size preset |
|---|---|---|
| Blog post, README, docs site | `html` (embed) hoặc `png` | `doc-inline` |
| Keynote / PowerPoint / Google Slides | `png` @2 | `slide-16x9` |
| Figma / Illustrator / chỉnh sửa tiếp | `svg` | `fit` |
| X / LinkedIn / OG link card | `png` @2 | `social-og` |
| Printed handout, PDF deck | `png` @3 | `print-a4-landscape` |
| Confluence / Notion / internal wiki | `png` @2 | `doc-wide` |

---

## 2. Size

Preset đặt SVG `viewBox`. Mọi giá trị dưới đây đều chia hết cho 4, nên grid rule trong SKILL.md §7 vẫn được giữ.

| Preset | viewBox | Aspect | PNG @2 | Type ramp | Dùng cho |
|---|---|---|---|---|---|
| `doc-inline` (mặc định) | `0 0 960 600` | 8:5 | 1920×1200 | standard | Diagram ở body-width trong post hoặc README |
| `doc-wide` | `0 0 1280 720` | 16:9 | 2560×1440 | standard | Full-width docs, wiki page |
| `slide-16x9` | `0 0 1280 720` | 16:9 | 2560×1440 | presentation | Deck slide, projected |
| `slide-4x3` | `0 0 1024 768` | 4:3 | 2048×1536 | presentation | Legacy deck template |
| `social-og` | `0 0 1200 632` | ~1.9:1 | 2400×1264 | presentation | Link preview card |
| `social-square` | `0 0 1080 1080` | 1:1 | 2160×2160 | presentation | Feed post, carousel |
| `print-a4-landscape` | `0 0 1120 792` | ~1.41:1 | @3 → 3360×2376 | print | A4 landscape, margin ~10mm ở 96dpi |
| `print-letter-landscape` | `0 0 1056 816` | ~1.29:1 | @3 → 3168×2448 | print | US Letter landscape |
| `video-landscape` | `0 0 1920 1080` | 16:9 | 3840x2160 | presentation | Blog cover, video cover |
| `fit` | suy ra từ content | bất kỳ | @2 | standard | Vector hand-off; không có frame cố định |

### LinkedIn portrait preset

`social-portrait` dùng canvas cố định `960×1200`, tỷ lệ 4:5. PNG ở scale 2 là `1920×2400`.
HTML phải giữ toàn bộ content trong canvas này; khi xem trên mobile, canvas được co theo width
viewport nhưng không được làm tràn title, diagram, label hoặc footer.

### Suy ra `fit`

Làm tròn content bounding box **lên** multiple of 4 tiếp theo, sau đó thêm fixed chrome: outer margin 40px ở mọi phía, cộng 60px phía dưới cho legend strip. Không bao giờ để content chạm mép `viewBox`.

### Type ramp theo size class

Khi canvas lớn hơn, node name trông sẽ nhỏ tương đối — đừng để điều đó xảy ra. Scale ramp theo preset để slide chiếu vẫn đọc được từ hàng ghế cuối.

| Role | standard | presentation | print |
|---|---|---|---|
| Title (Instrument Serif) | 28 | 40 | 32 |
| Node name (Geist 600) | 12 | 16 | 12 |
| Sublabel (Geist Mono) | 9 | 12 | 9 |
| Arrow label (Geist Mono) | 8 | 12 | 8 |
| Eyebrow / tag (Geist Mono) | 8 | 8 | 8 |
| Node box min height | 48 | 64 | 48 |
| Min gap between nodes | 24 | 40 | 24 |

Presentation ramp ngụ ý ít node hơn — node name 16px trong box 64px chiếm canvas nhanh hơn. Nếu layout `slide-16x9` không fit, chính size dial đang cho biết detail dial đặt quá cao; hãy giảm một detail level thay vì thu nhỏ type.

### Safe area

- **Mọi preset:** outer margin 40px; legend strip là 60px dưới cùng và không có content khác ở đó.
- **`social-og`:** giữ 64px ngoài cùng ở mọi phía trống — link-card crop khác nhau khó đoán giữa các platform.
- **`slide-*`:** chừa 80px phía dưới nếu deck template có footer bar; hỏi nếu chưa chắc.

---

## 3. Detail level

Bao nhiêu phần của source được giữ lại. Đây là *count dial* — nó điều khiển số element đi qua, không điều khiển cách chúng được diễn đạt; phần đó thuộc §4.

| Level | Nodes | Edges | Sublabels | Những gì được giữ |
|---|---|---|---|---|
| `faithful` (詳細) | ≤24, có zone | ≤32 | mọi port, protocol, version | Mọi component riêng biệt trong source. Chỉ merge exact duplicate. |
| `balanced` (mặc định) | ≤12 | ≤16 | technical sublabel trên ≤4 node | Các component mang story; leaf cluster được collapse thành một node. |
| `simplified` (簡略) | ≤7 | ≤9 | không có | Capability và thứ tự của chúng. Infrastructure biến mất. |

`balanced` và `simplified` nằm trong complexity budget tiêu chuẩn của SKILL.md §7. **`faithful` chủ động vượt budget đó** — đây là trade-off, và đi kèm các điều kiện:

1. **Bắt buộc zoning.** Trên 9 node, mọi node phải thuộc một labeled zone (2–4 zone, hairline border, `paper-2` fill, mono uppercase zone label ở top-left). Diagram 20 node không zone là wiring diagram chứ không phải schematic.
2. **Connector rule không được nới.** SKILL.md §6 rule 1–5 vẫn áp dụng ở 24 node. Nếu không route được mà không overlap, bạn đã vượt real ceiling — hãy split.
3. **Trên 24 node, phải split.** Tạo overview (zone như node, grammar `balanced`) cộng một detail diagram cho mỗi zone. Đặt tên `<base>-overview.html`, `<base>-<zone>.html`. Không bao giờ ship một canvas 40 node.
4. **Accent vẫn là 2.** Nhiều node hơn không cho phép có thêm focal element.

### Degrade ladder

Khi source có nhiều element hơn level cho phép, cắt theo đúng thứ tự này và dừng ngay khi xuống dưới budget. Không cắt ad hoc.

1. **Decorative cells** — sticky note, free-floating text, title block, watermark, legend của source. Note đáng giữ được chuyển thành annotation callout — tối đa 2, xem [primitive-annotation.md](primitive-annotation.md).
2. **Exact duplicates** — N worker/replica/shard giống hệt thành một node `Worker ×N`.
3. **Leaf clusters** — container có children đều là leaf collapse thành container: `Core Services` thay ba box con. Extractor liệt kê chúng dưới *collapsible groups*.
4. **Degree-1 sinks không đổi story** — monitoring hook, log bucket, archive tier.
5. **Cross-cutting infrastructure** — logging, metrics, secrets, CI. Ở `simplified` bỏ mà không cần hỏi; ở `balanced` giữ tối đa một, và chỉ nếu diagram nói về nó.
6. **Vẫn quá?** Split overview + detail. Split luôn tốt hơn shrink.

Mọi thứ bị cắt ở bước 2–6 phải xuất hiện trong fidelity ledger (§5). Bước 1 không cần report.

---

## 4. Audience level

Độc lập với detail dial: cùng 12 node sẽ được gọi tên khác nhau cho platform team và steering committee. Detail quyết định *bao nhiêu*; audience quyết định *gọi chúng là gì*.

| Audience | Node names | Sublabels | Edge labels | Tuyệt đối không |
|---|---|---|---|---|
| `engineer` | tên service/component chính xác | protocol, port, version, image tag | `POST /v2/orders`, `SQL`, `gRPC` | động từ mơ hồ như "connects to" |
| `mixed` (mặc định) | component names, acronym được mở rộng | technology chỉ khi làm thay đổi decision | động từ thường — `verifies`, `writes`, `notifies` | port, version, internal codename |
| `executive` | capability và outcome | không có | business verbs — `approves`, `pays out` | vendor name, infrastructure, protocol |

Ví dụ cùng một node qua ba audience:

| Audience | Node name | Sublabel |
|---|---|---|
| `engineer` | `Auth Service` | `JWT · RS256 · :8443` |
| `mixed` | `Auth Service` | `token check` |
| `executive` | `Sign-in` | — |

Hai quy tắc áp dụng cho mọi audience:

- **Không invent detail để lấp slot.** Nếu source chỉ nói `svc-04`, output `executive` chỉ được gọi tên theo chức năng nếu có thể xác định từ context — nếu không, hỏi thay vì đoán business name.
- **Giữ vocabulary của source cho proper noun.** Đổi `Kafka` thành `Message Bus` ở `executive` là chấp nhận được; đổi thành `Event Grid` — một product khác — là factual error.

### Non-Latin labels

Geist không có coverage CJK. Khi label chứa Japanese, Chinese hoặc Korean text, mở rộng family trên **chính các `<text>` đó** — không đổi toàn bộ skin:

```svg
<text font-family="'Geist', 'Hiragino Sans', 'Noto Sans JP', 'Yu Gothic', sans-serif">認証サービス</text>
<text font-family="'Geist', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif">인증 서비스</text>
```

Hiragino/Yu Gothic stack không có Hangul glyph, vì vậy Korean label cần Korean stack — không tái dùng Japanese stack. Noto Sans KR được ship trong font link của skin nên đứng đầu stack đó, local family theo sau; register, floor và title rule dành riêng cho Korean nằm trong [`style-guide.md`](style-guide.md#korean-labels). Với mono sublabel dùng `'Geist Mono', 'Noto Sans Mono CJK JP', monospace` cho Japanese hoặc `'Geist Mono', 'Noto Sans Mono CJK KR', monospace` cho Korean.

Budget **1em cho mỗi full-width CJK glyph**, không dùng một tỷ lệ nhỏ cộng vào average Latin glyph; `verify-treemap.py` dùng contract bảo thủ đó cho Unicode wide/full-width character và coi combining mark là không advance. Ưu tiên name 12px thay vì sublabel 8px cho CJK vì dưới 10px trở nên bệt. Width thực tế vẫn thay đổi theo fallback font, nên chạy geometry verifier liên quan sau khi dịch label.

---

## 5. Fidelity ledger

Bất cứ khi nào output nhỏ hơn input — mọi run `balanced` và `simplified`, và phần lớn run `faithful` — hãy report những gì bị cắt trong chat sau file path. Ngắn và cụ thể:

```
Detail: balanced · 18 source nodes → 9 drawn
Merged:  worker-01..06 → "Ingest Worker ×6"
Collapsed: "Observability" group (Grafana, Loki, Tempo) → one node
Dropped: 2 sticky notes, CI pipeline (cross-cutting)
Kept in full: the request path (Client → Gateway → Orders → Postgres)
```

Người đọc diagram không nhìn thấy thứ bị thiếu. Người yêu cầu diagram thì cần biết.

---

## 6. Checklist

Chạy song song với taste gate ở SKILL.md §9.

- [ ] Cả bốn dial đã được đặt — do user yêu cầu, suy ra từ destination, hoặc dùng default và đã nói rõ?
- [ ] `viewBox` khớp chính xác size preset, các giá trị chia hết cho 4?
- [ ] Type ramp đúng size class — không dùng standard ramp trên slide?
- [ ] Outer margin 40px được giữ (64px cho `social-og`)?
- [ ] Node count nằm trong ceiling của detail level?
- [ ] `faithful` trên 9 node → có zone, và split trên 24?
- [ ] Node name, sublabel và edge label đều ở cùng audience level?
- [ ] CJK label có font fallback?
- [ ] Fidelity ledger đã report mọi thứ bị cắt?
- [ ] Diagram `<svg>` có `role="img"`, `aria-labelledby` resolve đúng, first-child `<title>` không rỗng, `<desc>` không rỗng, và ID có prefix theo diagram/variant?
- [ ] Non-HTML format được sinh qua [`export.md`](export.md), không hand-author?
