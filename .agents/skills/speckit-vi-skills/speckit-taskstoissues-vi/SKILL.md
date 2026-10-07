---
name: "speckit-taskstoissues-vi"
description: "Chuyển các task hiện có thành GitHub issue có thể hành động, được sắp xếp theo dependency cho feature dựa trên các design artifact hiện có."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/taskstoissues.md"
---


## Đầu vào của người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi chuyển task thành issue)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.before_taskstoissues`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có trường `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có trường `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để phần đánh giá điều kiện cho implementation của HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo cờ `optional`:
  - **Hook tùy chọn** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Hook bắt buộc** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Quy trình

1. Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` từ thư mục gốc repo và parse FEATURE_DIR cùng danh sách AVAILABLE_DOCS. Tất cả đường dẫn phải là đường dẫn tuyệt đối. Với dấu nháy đơn trong tham số như `"I'm Groot"`, dùng cú pháp escape, ví dụ: `'I'\''m Groot'` (hoặc dùng dấu nháy kép nếu có thể: `"I'm Groot"`).
1. **NẾU TỒN TẠI**: Đọc `.specify/memory/constitution.md` để lấy các nguyên tắc của dự án và ràng buộc quản trị.
1. Từ script đã chạy, lấy đường dẫn đến **tasks**.
1. Lấy Git remote bằng cách chạy:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> CHỈ TIẾP TỤC CÁC BƯỚC SAU NẾU REMOTE LÀ MỘT GITHUB URL

1. **Lấy các issue hiện có để chống trùng lặp**: Trước khi tạo bất cứ thứ gì, xây tập hợp task ID sắp xử lý từ `tasks.md` (mỗi ID là chữ `T` theo sau bởi **ít nhất** ba chữ số, ví dụ `T001` — `$speckit-converge` gán ID mới theo `T{M+1:03d}`, trong đó ba chữ số là mức tối thiểu chứ không phải giới hạn tối đa, vì vậy khi file có hơn 999 task thì ID sẽ có bốn chữ số trở lên). Sau đó dùng tool `list_issues` của GitHub MCP server để tìm các issue đã bao phủ những ID đó. Không truyền giá trị `state`, vì khi bỏ qua tham số này tool sẽ trả về cả issue đang mở và đã đóng. Yêu cầu `perPage: 100` để giảm số lần gọi, và vì tool dùng phân trang theo cursor, hãy yêu cầu các trang tiếp theo bằng tham số `after` (dùng `endCursor` từ response trước). Với title của từng issue, đối chiếu theo mẫu task ID `\bT\d{3,}\b` (`{3,}` chấp nhận ID có bốn chữ số trở lên — nếu dùng `\d{3}` thì title chứa `T1000` sẽ hoàn toàn không match, vì `\b` ở cuối không thể nằm giữa hai chữ số, khiến task đó âm thầm vừa không được nhận diện là trùng vừa không được tạo; word boundary vẫn ngăn token như `ST001` match, đồng thời buộc toàn bộ dãy chữ số phải được tiêu thụ để `T100` không thể match bên trong `T1000`; cách này cũng nhận diện các title dạng `T001 ...`, `T001: ...` hoặc `[T001] ...`). Khi match một task ID trong tập hợp của bạn, đánh dấu ID đó là đã có issue. Dừng phân trang ngay khi mọi task ID đã được match hoặc khi không còn trang nào nữa, để không tiếp tục tải toàn bộ lịch sử issue của repo sau khi đã xác định đủ task ID. Cách này giới hạn số lần gọi trên các repo có lịch sử issue lớn, đồng thời vẫn ngăn trùng lặp khi command được chạy lại sau khi `tasks.md` được tạo lại hoặc skill được gọi lại.
1. Với từng task trong danh sách, dùng GitHub MCP server để tạo issue mới trong đúng repository tương ứng với Git remote. Command này **không chạy lại runtime-verification/catalog**; nếu task có trace như `runtime:UI-007`, Risk ID hoặc required-evidence note thì bảo toàn phần traceability đó khi normalize task thành issue. Các dòng task trong `tasks.md` bắt đầu bằng checkbox Markdown, vì vậy trước tiên hãy bỏ phần `- [ ]` ở đầu dòng (cùng các marker `[P]` / `[US#]` nếu có) để lấy task ID và mô tả. Tạo issue với một title chuẩn duy nhất theo dạng `T001: <description>`, trong đó ID chỉ xuất hiện một lần rồi đến mô tả task (ví dụ, dòng `- [ ] T001 Create project structure` sẽ trở thành title `T001: Create project structure`).
   - **Bỏ qua** mọi task có ID đã xuất hiện trong tập hợp issue hiện có ở bước trước và báo lại việc đó (ví dụ: `T001 already has an issue, skipping`).
   - Chỉ tạo issue cho các task chưa có issue tương ứng.

> [!CAUTION]
> TUYỆT ĐỐI KHÔNG ĐƯỢC TẠO ISSUE TRONG REPOSITORY KHÔNG KHỚP VỚI REMOTE URL

## Kiểm tra sau khi thực thi

**Kiểm tra extension hook (sau khi chuyển task thành issue)**:
Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.after_taskstoissues`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có trường `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có trường `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để phần đánh giá điều kiện cho implementation của HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo cờ `optional`:
  - **Hook tùy chọn** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Hook bắt buộc** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Optional companion skill

Đọc protocol tại `../companion-skills.md`.

Command này **không re-evaluate companion guardrails**:
- chỉ bảo toàn companion traceability, Risk ID, required evidence, DEFERRED/BLOCKED note đã có trong `tasks.md`;
- không tự mở thêm rule stack-specific khi chuyển task thành issue;
- nếu task thiếu thông tin cần thiết, giữ nội dung trung thành với task và báo thiếu thay vì suy từ companion.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-taskstoissues`
- Tên gốc: `speckit-taskstoissues`
- Chính sách: `faithful`
- Commit nguồn: `566943554c617128f73e2e4864aeb713bacd0478`
