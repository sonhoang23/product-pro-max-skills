# Annotation Callout (italic-serif aside)

Dùng cho các ghi chú editorial bên lề — “italic pointer” đánh dấu một chi tiết mà không cạnh tranh với grammar chính của diagram. Hãy nghĩ đến marginalia như: *“structure IS the index”*, *“no imports, no configuration”*.

## Grammar

```svg
<!-- 1. Italic Instrument Serif text -->
<text x="904" y="36" fill="#2d3142" font-size="14" font-style="italic"
      font-family="'Instrument Serif', serif" text-anchor="end">no imports, no configuration</text>
<!-- 2. Dashed Bézier leader -->
<path d="M 820 44 Q 700 84 520 216" fill="none"
      stroke="rgba(45,49,66,0.40)" stroke-width="1" stroke-dasharray="4,3"/>
<!-- 3. Landing dot -->
<circle cx="520" cy="216" r="2" fill="#2d3142"/>
```

## Quy tắc
- Italic + serif kết hợp để biểu thị “editorial voice”, đối lập với phần thân sans/mono của diagram. Không thay bằng italic sans hoặc italic mono — sự kết hợp này mang ý nghĩa thiết kế quan trọng.
- Dashed path (`stroke-dasharray="4,3"`) phân biệt callout leader với arrow chính (solid).
- Đặt callout ở margin (góc trên-phải, dưới-trái). Không bao giờ đặt trong vùng diagram đang hoạt động.
- Tối đa 2 callout mỗi diagram. Nhiều hơn sẽ trở thành lời bình, không còn là tín hiệu nhấn mạnh.

## Màu

| Mục đích | Text | Leader |
|---|---|---|
| Ghi chú trung tính | ink `#2d3142` | `rgba(45,49,66,0.40)` |
| Focal / accent | coral `#eb6c36` | `rgba(235,108,54,0.50)` |
| Tertiary (muted) | muted `#4f5d75` | `rgba(45,49,66,0.30)` |

## Anti-pattern
- Solid arrow leader (dễ bị đọc như flow arrow).
- Italic sans hoặc italic mono — serif là thành phần mang ý nghĩa thiết kế quan trọng.
- Callout cắt qua primary arrow / lifeline — dịch sang một margin trống.
- Dùng callout để gắn nhãn cho thứ mà diagram nên gắn nhãn trực tiếp — hãy đặt label lên element đó.
