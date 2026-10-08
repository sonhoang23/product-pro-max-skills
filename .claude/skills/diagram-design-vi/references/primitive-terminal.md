# Terminal Window (biến thể CLI-chrome)

Skin full-page tùy chọn bọc bất kỳ diagram nào trong một cửa sổ terminal giả — titlebar có ba chấm, một dòng prompt `$`, toàn bộ dùng type monospace. Dùng cho post giới thiệu dev-tool, CLI product và technical social card khi screenshot cần đọc như "terminal", không phải "editorial doc".

Đây là **skin cố định thứ hai** — xem [style-guide.md § Terminal skin](style-guide.md#terminal-skin-opt-in-alternate) để biết token table. Nó không kế thừa brand token từ `onboarding.md` và không thuộc light/dark inversion rule; mọi terminal example đều dùng cùng chín token bất kể brand của host site.

## Grammar

```html
<div class="terminal">
  <div class="titlebar">
    <div class="dot accent"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="titlebar-name">loop.sh — self-improving-loop</div>
  </div>
  <main class="frame">
    <p class="prompt">
      <span class="sign">$</span> diagram-design render --type loop
    </p>
    <h1># The self-improving loop</h1>
    <svg>...</svg>
  </main>
</div>
```

```css
body {
  background: var(--terminal-page);
}
.terminal {
  background: var(--terminal-paper);
  border: 1px solid var(--terminal-border);
  border-radius: 12px;
}
.titlebar {
  background: var(--terminal-bar);
  border-bottom: 1px solid var(--terminal-border);
}
.dot {
  background: var(--terminal-soft);
}
.dot.accent {
  background: var(--terminal-accent);
}
```

Bên trong SVG, thay 1:1 các token mặc định light/dark bằng token `terminal-*`: `paper` → `terminal-paper`, `ink` → `terminal-ink`, `muted`/`soft` → `terminal-muted`/`terminal-soft`, `accent`/`accent-tint` → `terminal-accent`/`terminal-accent-tint`. Pattern hub/focal-node — fill đảo ngược cho một element được highlight — vẫn được áp dụng.

## Typography

**Mọi thứ đều là monospace** — đây là biến thể duy nhất nơi điều đó là đúng. Bỏ hoàn toàn Instrument Serif và Geist sans; page title dùng mono, bold và có prefix `# ` để đọc như comment line. Eyebrow trở thành shell prompt: `$ ` dùng `terminal-accent`, command dùng `terminal-muted`.

Tăng mọi text role khoảng **1–2px so với** default type scale trong `style-guide.md`, ví dụ `node-name` 12px → 14px, `sublabel`/`arrow-label` 8–9px → 9–10px, hub label 16px → 18px. Monospace ở kích thước mặc định trông nhỏ khi đặt cạnh hỗn hợp sans/serif mà nó thay thế; hơn nữa những card này thường được xem ở social-feed scale chứ không phải full-bleed.

## Titlebar dots

Ba circle 10px theo phong cách macOS. **Quy tắc 1 accent vẫn giới hạn việc dùng màu ở đây**: một dot là `terminal-accent`, hai dot còn lại là `terminal-soft`. Không dùng traffic-light triad đỏ/vàng/xanh — đó sẽ là hue thứ hai và thứ ba, trái với palette.

## Quy tắc quan trọng

- Không dùng pure black (`#000000`) — dùng `terminal-page` (`#0a0a0a`) / `terminal-paper` (`#141414`). Cùng quy tắc như default skin, cùng lý do: true black bị clip trên OLED và khi in.
- Chỉ một accent. Nếu diagram cần focal element thứ hai, dùng `terminal-ink` (trắng) để nhấn bằng weight/size, không thêm màu thứ hai.
- Background dot-grid pattern, nếu dùng, giữ ở `rgba(255,255,255,0.06–0.08)` — chỉ là texture rất nhẹ, không cạnh tranh với titlebar chrome.

## Khi nào dùng

- Post giới thiệu dev-tool / CLI product như npm package, CLI flag hoặc terminal-based workflow.
- Technical social card nơi thông điệp "đây là công cụ cho engineer" là một phần của nội dung.
- Screenshot cần nổi bật trong feed thiên dark mode như X, Discord hoặc dev blog.

## Khi nào không dùng

- Editorial / long-form post — thay vào đó ghép với default light hoặc full-editorial variant.
- Output đã brand-match từ `onboarding.md` — terminal là fixed skin, không brand-tokenized. Không cố hòa hai hệ này.
- Bất kỳ diagram nào có audience không được developer-code để hiểu `$` / `#` / titlebar dots là chrome thay vì content.
