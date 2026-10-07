# Sketchy Filter (biến thể vẽ tay)

Displacement filter tuỳ chọn làm mọi stroke và edge rung nhẹ — biến bất kỳ minimal variant nào thành phong cách “editorial” vẽ tay mà không thay đổi layout. Dùng khi diagram đi cùng essay thay vì tài liệu kỹ thuật.

## Grammar

```svg
<defs>
  <filter id="sketchy" x="-2%" y="-2%" width="104%" height="104%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="4"/>
    <feDisplacementMap in="SourceGraphic" scale="1.5"/>
  </filter>
</defs>

<!-- Apply to a group wrapping shapes — NOT text -->
<g filter="url(#sketchy)">
  <!-- rects, paths, circles, lines go here -->
</g>

<!-- Text sits OUTSIDE the filtered group — legibility stays crisp -->
<text ...>Labels go here</text>
```

## Tinh chỉnh

| Parameter | Khoảng | Hiệu ứng |
|---|---|---|
| `baseFrequency` | 0.01–0.04 | Thấp = line lượn chậm; cao = rung nhiều. Mặc định 0.02. |
| `numOctaves` | 1–3 | Cao hơn = nhiều chi tiết noise hơn. 2 là đủ. |
| `scale` | 1–6 | 1 gần như không thấy, 1.5 mặc định, 2 thấy rõ, 4+ thành kiểu hoạt hình. |
| `seed` | integer | Đổi để có random pattern khác. |

## Quy tắc quan trọng
Filter shape, **không filter text**. Text qua displacement mapping sẽ khó đọc. Hãy cấu trúc SVG để text nằm trong sibling group bên ngoài filtered group.

## Khi nên dùng
- Essay / blog post / newsletter khi diagram là hero của trang kể chuyện.
- Phong cách “working sketch” — cho thấy ý tưởng còn đang hình thành, chưa phải architecture cuối cùng.

## Khi không nên dùng
- Tài liệu kỹ thuật (cần độ chính xác).
- Diagram có label dày hoặc alignment sát (filter sẽ thành nhiễu).
- Dark variant — độ rung dễ trông như artifact trên nền tối. Hãy test trước.
