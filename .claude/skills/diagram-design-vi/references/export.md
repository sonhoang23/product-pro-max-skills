# Export sang PNG / SVG

Chuyển một file HTML diagram đã tạo thành `.svg` và/hoặc `.png` portable nằm cạnh file đó. **Chỉ chạy thủ công khi được yêu cầu — tuyệt đối không tự chạy.**

## Trigger

Nạp file này khi:

- Người dùng gọi `/diagram-design:export-diagram <html-file>` — slash command của plugin, được định nghĩa ở `commands/export-diagram.md` tại repo root.
- Người dùng yêu cầu bằng ngôn ngữ tự nhiên rằng muốn export, save, rasterize, convert hoặc download diagram dưới dạng `.svg` hoặc `.png`. Các cách nói điển hình:
  - "export this as PNG"
  - "save as SVG"
  - "give me a PNG of that diagram"
  - "rasterize it"
  - "convert to png and svg"

Slash command chỉ là wrapper mỏng ủy quyền cho file này — cả hai đường đều chạy cùng procedure bên dưới.

## Phạm vi

Cả hai format đều là **diagram-only** — chỉ node `<svg>`. Editorial wrapper như header, summary card và footer trong variant `-full` được bỏ có chủ đích: deliverable export là chính diagram, phù hợp cho Figma, slide, social card hoặc hình trong blog.

SVG-only export giữ nguyên `<title>` và `<desc>` của source. ID có prefix riêng cho từng diagram và variant giúp nhiều SVG export có thể inline cùng một page mà figure này không resolve nhầm accessible name sang figure khác.

Nếu người dùng yêu cầu rõ "a screenshot of the whole page including the cards", đó là yêu cầu khác — dùng full-page screenshot thông thường qua OS hoặc browser của người dùng.

## Quy trình export SVG

1. Đọc source HTML file.
2. Extract block `<svg ...>...</svg>` **đầu tiên**. Dùng multiline regex anchor ở `<svg` và `</svg>`. Phần lớn generated diagram chỉ có một SVG; nếu có nhiều thì SVG đầu tiên là diagram, ngoại trừ gallery file — xem *Edge cases*.
3. Làm nó thành standalone SVG:
   - Bảo đảm opening tag có `xmlns="http://www.w3.org/2000/svg"`; nếu thiếu thì thêm.
   - Bảo đảm có `viewBox`. Template của skill luôn có; nếu thiếu thì cảnh báo thay vì đoán.
   - Giữ nguyên chính xác `role="img"`, `aria-labelledby`, cùng first-child `<title>` / `<desc>` như source đã author.
   - Inject Google Fonts `@import` để SVG render đúng typography trong browser. **Phải XML-escape các dấu `&` thành `&amp;`** — standalone `.svg` được parse như XML nghiêm ngặt, trong đó `&` trần bắt đầu entity reference và khiến toàn file parse lỗi. Không copy raw URL trực tiếp từ HTML `<link href>` vì dạng ampersand đó chỉ hợp lệ trong HTML.

     ```svg
     <defs>
       <style>@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Geist:wght@400;500;600&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap');</style>
     </defs>
     ```

     Nếu SVG đã có `<defs>`, **merge** `<style>` vào đó, không thêm `<defs>` thứ hai.
4. Prepend `<?xml version="1.0" encoding="UTF-8"?>\n` để file là XML well-formed.
5. Ghi ra `<basename>.svg` cạnh source, ví dụ `example-architecture.html` → `example-architecture.svg`. Nếu người dùng đưa output path rõ ràng thì phải tôn trọng path đó.

### Caveat cần nói với người dùng

Các tool không fetch remote font khi import — như Illustrator offline, một số đường import của Figma, hoặc SVG viewer cũ — sẽ substitute typography. SVG render đúng trong browser hiện đại. Nếu cần pixel-perfect portability, khuyến nghị PNG export.

## Quy trình export PNG

Render **HTML gốc**, không phải SVG đã extract, rồi screenshot chỉ bounding box của element `<svg>`. Cách này giữ font loading đáng tin cậy vì source HTML đã wire font, đồng thời vẫn đáp ứng quy tắc "diagram only". PNG luôn có **transparent background** (`omit_background=True`) để đặt lên slide/doc màu bất kỳ mà không có quầng trắng.

Với HTML có motion, append `?motion=static`, chờ `document.fonts.ready`, và assert motion root có `data-frame="static"` trước khi capture. Không bao giờ export ở một wall-clock delay tùy ý.

### Detection

Trước khi chạy, xác minh Playwright đã được cài:

```
python -c "import playwright" 2>NUL || python -c "import playwright"
```

Nếu import thất bại, đưa **chính xác** instruction sau cho người dùng và dừng:

> Playwright isn't installed. To enable PNG export, run:
> ```
> pip install playwright
> playwright install chromium
> ```
> Then ask me to export again.

Không tự cài. Người dùng yêu cầu một tính năng, không yêu cầu thay đổi hệ thống.

### Rasterize

Ghi snippet sau vào file tạm và chạy bằng `python <tmp.py> <src.html> <out.png>`:

```python
from playwright.sync_api import sync_playwright
import sys, pathlib

src, out = sys.argv[1], sys.argv[2]
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 2

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=scale)
    page.goto(f"file://{pathlib.Path(src).resolve()}")
    page.wait_for_load_state("networkidle")
    page.locator("svg").first.screenshot(path=out, omit_background=True)
    browser.close()
```

Mặc định `device_scale_factor=2` để output sắc nét. Chấp nhận `1` cho asset nhỏ gọn hoặc `3` cho print/retina hero; truyền dưới dạng CLI arg thứ ba.

### Tên output

`example-architecture.html` → `example-architecture.png`, ghi cạnh source. Nếu người dùng đưa path rõ ràng thì dùng path đó.

Script thêm capture mode vào tên file để các chế độ không ghi đè nhau:

```text
example-architecture__diagram-only__scale-2.png
example-architecture__full-page__preset-social-portrait__scale-2.png
example-architecture__full-page__viewport-1600x900__scale-2.png
```

Dùng `--diagram-only` để ghi rõ chỉ chụp node `<svg>`; đây cũng là mặc định khi không có `--full-page`. Dùng `--variant NAME` để thêm nhãn tùy chọn, ví dụ `--variant version-2`. Nếu file cùng tên đã tồn tại, script thêm hậu tố số (`-2`, `-3`, ...).

## Kích thước export

Pixel dimensions của PNG bằng `viewBox` của SVG × `device_scale_factor`. Vì vậy quyết định size đã được đưa ra khi vẽ diagram — xem [`output-spec.md` §2](output-spec.md) cho preset. Export chỉ chọn multiplier.

| Destination | Scale | Kết quả với `viewBox` 1280×720 |
|---|---:|---:|
| Docs, README, wiki | 2 | 2560×1440 |
| Slide deck (projected) | 2 | 2560×1440 |
| Print / PDF handout | 3 | 3840×2160 |
| Inline thumbnail, email | 1 | 1280×720 |

### Đạt chính xác pixel size

Khi người dùng cần kích thước cụ thể, chẳng hạn OG card đúng 1200×630 hoặc slide image 1920×1080, tính scale factor thay vì đoán — Playwright chấp nhận giá trị fractional:

```
scale = target_width / viewBox_width
```

Ví dụ `viewBox` rộng 960 với target 1200px → `scale=1.25`.

Hai quy tắc:

- **Không bao giờ scale xuống dưới 1** để đạt target nhỏ — việc đó làm type bị soft-focus. Hãy redraw ở preset nhỏ hơn.
- **Không bao giờ scale vượt quá 4** — sau mức đó bạn đang upscale layout được thiết kế cho canvas nhỏ hơn; hãy redraw ở `slide-16x9` hoặc print preset.

Nếu target aspect ratio không khớp `viewBox`, nói rõ và đề xuất redraw ở preset tương ứng. Padding hoặc crop diagram đã hoàn thiện để ép vào frame **không** phải export operation; nó phá safe margin 40px.

## Edge cases

- **Source là `assets/index.html`** — gallery có nhiều SVG trong một file: từ chối export và hỏi người dùng diagram file cụ thể nào. Không đoán.
- **Không tìm thấy `<svg>`**: source không phải diagram file. Báo cho người dùng; không ghi gì.
- **Surrounding HTML quan trọng với người dùng**: họ muốn card/header nằm trong hình. Nói rõ skill này chỉ export diagram và khuyến nghị browser full-page screenshot hoặc PDF print riêng.
- **Source thiếu font lúc runtime**: Playwright sẽ substitute và screenshot sẽ sai. Kiểm tra source HTML có `<link href="...fonts.googleapis.com...">` trong `<head>`. Nếu thiếu, file không đến từ current template — sửa source thay vì workaround trong export.

## Lệnh này tuyệt đối không làm gì

- Không sửa source HTML.
- Không thêm export button hoặc `<script>` tag. Static diagram vẫn script-free; source có motion có thể giữ scoped controller từ [`animation.md`](animation.md), nhưng export không inject controller khác.
- Không tự sinh `.svg` hoặc `.png` cùng lúc với HTML generation. Mỗi lần đều phải được yêu cầu thủ công.
- Không embed HTML wrapper như card/header vào SVG bằng `foreignObject`; cách đó quá mong manh giữa các renderer.
