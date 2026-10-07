# Project theme — living diagram CSS

Project theme mode dùng một file CSS trong repository làm **source of truth cho phần nhìn của mọi diagram HTML**.

## Marker

Ở project root, `.diagram-design` có thể chứa đúng một dòng:

```text
theme: docs/diagrams/theme.css
```

Path phải là repo-relative, dùng dấu `/`, kết thúc bằng `.css`, không được là URL, absolute path, chứa `..`, `~` hoặc backslash.

Nếu marker `theme:` hợp lệ:

1. Resolve path từ project root và yêu cầu file tồn tại.
2. Theme CSS là nguồn sự thật cho **giá trị visual token**.
3. `references/style-guide.md` vẫn là semantic contract: role nào dùng ở đâu, typography role, focal rule, density rule, v.v.
4. Bỏ qua first-run profile gate. Không cần profile trong `~/.diagram-design/profiles/`.
5. Mọi HTML diagram phải link tới theme bằng relative path từ chính file HTML.
6. CSS riêng của từng diagram chỉ chứa geometry/layout/type-specific rule; không copy lại project token value vào HTML.

Nếu theme marker sai hoặc file không tồn tại, dừng và báo lỗi. Không silent fallback sang profile/style guide vì như vậy project có thể render khác nhau trên mỗi máy.

## CSS variable contract

Project theme phải khai báo tối thiểu:

```css
:root {
  --diagram-paper: ...;
  --diagram-paper-2: ...;
  --diagram-ink: ...;
  --diagram-muted: ...;
  --diagram-soft: ...;
  --diagram-rule: ...;
  --diagram-rule-solid: ...;
  --diagram-accent: ...;
  --diagram-accent-tint: ...;
  --diagram-link: ...;

  --diagram-font-title: ...;
  --diagram-font-sans: ...;
  --diagram-font-mono: ...;

  --diagram-radius-sm: ...;
  --diagram-radius-md: ...;
  --diagram-radius-lg: ...;
}
```

Type-specific CSS phải tham chiếu `var(--diagram-...)`; không hardcode lại màu/font/radius đã có token.

## HTML contract

Ví dụ diagram nằm cùng thư mục với theme:

```html
<link rel="stylesheet" href="./theme.css">
<style>
  /* Chỉ layout/geometry riêng của diagram */
  .architecture-zone { ... }
</style>
```

Nếu diagram nằm ở thư mục khác, tính relative path chính xác tới theme. Không dùng absolute filesystem path.

SVG presentation attribute được phép dùng CSS variable:

```html
<rect fill="var(--diagram-paper-2)" stroke="var(--diagram-ink)" />
```

Ưu tiên class semantic trong theme cho primitive phổ biến; dùng variable trực tiếp khi rule thuộc layout/type riêng.

## Living-document behavior

Khi sửa `theme.css`, tất cả diagram HTML đang link file này sẽ nhận style mới ở lần mở/reload tiếp theo. Không cần regenerate diagram nếu chỉ đổi:

- palette;
- font stack;
- border/radius;
- stroke token;
- primitive semantic style đã đặt trong theme.

Vẫn cần sửa/regenerate diagram khi thay đổi geometry, nội dung, node/edge, semantic meaning hoặc layout-specific CSS.

## Standalone export

Project HTML mặc định **không standalone** vì phụ thuộc theme CSS local. Khi cần gửi một file HTML duy nhất, chạy `python3 scripts/inline_theme.py path/to/diagram.html` từ thư mục skill (hoặc gọi script bằng full path) để tạo `*-standalone.html` với theme đã inline. Bản standalone là artifact để chia sẻ, không phải source document; không chỉnh trực tiếp rồi kỳ vọng nó tiếp tục nhận update từ theme.

PNG/SVG export có thể render từ project HTML bình thường miễn theme path resolve được.
