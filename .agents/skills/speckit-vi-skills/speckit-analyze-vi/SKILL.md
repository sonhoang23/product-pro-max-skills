---
name: "speckit-analyze-vi"
description: "Thực hiện phân tích nhất quán và chất lượng theo kiểu không phá hủy trên constitution, spec.md, plan/design artifacts, tasks.md và diagram dẫn xuất sau khi đã tạo task."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/analyze.md"
---


## Đầu vào người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi phân tích)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry dưới key `hooks.before_analyze`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có field `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook đó và để việc đánh giá condition cho implementation của HookExecutor.
- Khi dựng command invocation từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau dựa trên cờ `optional`:
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

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục sang phần Mục tiêu. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation thực tế có thể khác với id `{command}` hiển thị ở trên, ví dụ agent chạy ở skills mode có thể gọi dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua âm thầm.

## Mục tiêu

Xác định các điểm không nhất quán, trùng lặp, mơ hồ và chưa được đặc tả đầy đủ giữa các lớp artifact (`spec.md` → `plan.md`/technical artifacts → `tasks.md`) trước khi implementation. Command này **CHỈ ĐƯỢC** chạy sau khi `$speckit-tasks` đã tạo thành công một file `tasks.md` hoàn chỉnh.

## Ràng buộc vận hành

**CHỈ ĐỌC NGHIÊM NGẶT**: **KHÔNG** sửa bất kỳ file nào. Chỉ xuất báo cáo phân tích có cấu trúc. Có thể đề xuất một kế hoạch khắc phục tùy chọn (người dùng phải phê duyệt rõ ràng trước khi bất kỳ command chỉnh sửa tiếp theo nào được gọi thủ công).

**Thẩm quyền của hiến chương**: Hiến chương dự án (`.specify/memory/constitution.md`) là **không thể thương lượng** trong phạm vi phân tích này. Mọi xung đột với hiến chương tự động được xếp mức CRITICAL và phải được xử lý bằng cách điều chỉnh spec, plan hoặc tasks — không được làm nhẹ nguyên tắc, diễn giải lại hoặc âm thầm bỏ qua. Nếu bản thân một nguyên tắc cần thay đổi, việc đó phải được thực hiện trong một lần cập nhật hiến chương riêng biệt và rõ ràng bên ngoài `$speckit-analyze`.

## Các bước thực thi

### 1. Khởi tạo ngữ cảnh phân tích

Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec -RequireTasks -IncludeTasks` một lần từ thư mục gốc repo và parse JSON để lấy FEATURE_DIR cùng AVAILABLE_DOCS. Từ đó suy ra các đường dẫn tuyệt đối:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Dừng với thông báo lỗi nếu thiếu bất kỳ file bắt buộc nào (hướng dẫn người dùng chạy command prerequisite còn thiếu).
Với dấu nháy đơn trong tham số như "I'm Groot", dùng cú pháp escape, ví dụ: 'I'\''m Groot' (hoặc dùng dấu nháy kép nếu có thể: "I'm Groot").

### 2. Nạp artifact theo nguyên tắc Progressive Disclosure

Chỉ nạp lượng ngữ cảnh tối thiểu cần thiết từ từng artifact:

**Từ spec.md:**

- Overview/Context
- Functional Requirements
- Success Criteria (kết quả có thể đo lường — ví dụ: hiệu năng, bảo mật, tính sẵn sàng, thành công của người dùng, tác động kinh doanh)
- User Stories
- Edge Cases (nếu có)

**Từ diagram dẫn xuất (khi cần xác minh visual drift):**

- `spec-diagram/`, `plan-diagram/`, `tasks-diagram/` nếu tồn tại.
- Diagram chỉ dùng để xác minh mô hình trực quan có còn đồng bộ với source artifact; không làm source of truth.

**Từ plan.md:**

- Lựa chọn kiến trúc/stack
- Tham chiếu Data Model
- Các phase
- Ràng buộc kỹ thuật

**Từ tasks.md:**

- Task ID
- Mô tả
- Nhóm theo phase
- Marker song song [P]
- Đường dẫn file được tham chiếu
- Section `Runtime Risk Coverage` và mapping Risk ID → Task ID / lý do N/A

**Từ runtime-verification:**

- Nạp `.agents/skills/runtime-verification/SKILL.md` ở mode `audit`.
- Đọc requirement/AC/edge-case refs trong spec, `Runtime Risk Design` trong plan và `Runtime Risk Coverage` trong tasks.
- Tự xác định lại applicability từ spec/plan/technical artifacts; không tin mù quáng bảng coverage trong `tasks.md`.
- Đọc `lifecycle-profile.md` + `catalog-index.md`, sau đó chỉ nạp Risk ID/category liên quan.

**Từ hiến chương:**

- Nạp `.specify/memory/constitution.md` để kiểm tra nguyên tắc

### 3. Xây dựng mô hình ngữ nghĩa

Tạo các biểu diễn nội bộ (không đưa raw artifact vào output):

- **Danh mục requirement**: Với mỗi Functional Requirement (FR-###) và Success Criterion (SC-###), ghi lại một key ổn định. Dùng identifier FR-/SC- tường minh làm key chính khi có, đồng thời có thể suy ra thêm slug dạng cụm động từ mệnh lệnh để dễ đọc (ví dụ: "User can upload file" → `user-can-upload-file`). Chỉ đưa vào những Success Criteria đòi hỏi công việc có thể triển khai (ví dụ: hạ tầng load-testing, tooling audit bảo mật), và loại các outcome metric sau khi ra mắt cùng business KPI (ví dụ: "Reduce support tickets by 50%").
- **Danh mục user story/action**: Các hành động riêng biệt của người dùng kèm acceptance criteria
- **Ánh xạ độ bao phủ của task**: Map mỗi task tới một hoặc nhiều requirement hoặc story (suy luận bằng từ khóa / pattern tham chiếu tường minh như ID hoặc cụm từ khóa)
- **Runtime Risk Inventory**: Tập risk độc lập được `runtime-verification` xác định là `APPLIES | NOT_APPLICABLE | NEEDS_UPSTREAM`, kèm evidence từ architecture/integration.
- **Runtime Trace Map**: Map `Risk ID → Requirement/AC/Edge-case refs (khi applicable) → plan prevention design → Task IDs → required/actual evidence`.
- **Runtime Risk Coverage Map**: Map mỗi risk `APPLIES` tới task cụ thể; giữ riêng lý do N/A và upstream gap để phát hiện false-N/A hoặc risk bị bỏ sót.
- **Bộ quy tắc hiến chương**: Trích xuất tên nguyên tắc và các phát biểu chuẩn tắc MUST/SHOULD

### 4. Các lượt phát hiện theo hướng tiết kiệm token

Tập trung vào các phát hiện có tín hiệu cao. Giới hạn tổng cộng 50 phát hiện; phần còn lại được gom vào bản tóm tắt overflow.

#### A. Phát hiện trùng lặp

- Xác định các requirement gần như trùng nhau
- Đánh dấu cách diễn đạt chất lượng thấp hơn để hợp nhất

#### B. Phát hiện mơ hồ

- Đánh dấu các tính từ mơ hồ (fast, scalable, secure, intuitive, robust) nhưng thiếu tiêu chí đo lường
- Đánh dấu placeholder chưa được xử lý (TODO, TKTK, ???, `<placeholder>`, v.v.)

#### C. Thiếu đặc tả

- Requirement có động từ nhưng thiếu đối tượng hoặc kết quả có thể đo lường
- User story thiếu sự liên kết với acceptance criteria
- Task tham chiếu file hoặc component không được định nghĩa trong spec/plan

#### D. Tuân thủ hiến chương

- Bất kỳ requirement hoặc phần tử plan nào xung đột với nguyên tắc MUST
- Thiếu section hoặc quality gate bắt buộc theo hiến chương

#### E. Khoảng trống bao phủ

- Requirement không có task nào liên quan
- Task không map được tới requirement/story nào
- Success Criteria đòi hỏi công việc có thể triển khai (hiệu năng, bảo mật, tính sẵn sàng) nhưng không được phản ánh trong task

#### F. Không nhất quán

- Thuật ngữ bị trôi nghĩa (cùng một khái niệm nhưng được gọi khác nhau giữa các file)
- Data entity được nhắc trong plan nhưng không có trong spec (hoặc ngược lại)
- Mâu thuẫn về thứ tự task (ví dụ: task integration đứng trước task nền tảng mà không có ghi chú dependency)
- Requirement xung đột nhau (ví dụ: một yêu cầu Next.js trong khi yêu cầu khác chỉ định Vue)

#### G. Drift giữa source artifact và diagram/downstream

Kiểm tra thêm khi có diagram:

- `spec-diagram/` chứa actor/flow/domain/state không còn đúng với `spec.md`.
- `plan-diagram/` chứa architecture/data-flow/component relation không còn đúng với plan/data-model/contracts.
- `tasks.md` hoặc implementation dựa trên behavior/technical decision không tồn tại trong source artifact có thẩm quyền.
- Diagram chứa semantics chỉ tồn tại trong hình.

#### H. Runtime Risk Coverage

- Risk mà `runtime-verification` xác định `APPLIES` nhưng không map tới task nào.
- Risk bị đánh `NOT_APPLICABLE` trong `tasks.md` nhưng architecture/contract cho thấy điều kiện áp dụng thực sự tồn tại.
- Risk `NEEDS_UPSTREAM` chưa được xử lý nhưng `tasks.md` vẫn tuyên bố hoàn tất.
- Task runtime chỉ ghi chung chung kiểu "smoke test toàn hệ thống" mà không chỉ rõ failure mode, expected runtime behavior hoặc evidence cần chứng minh.
- Runtime task bị dồn mặc định vào phase cuối thay vì nằm ở phase/story nơi route/auth/integration/env/worker/browser boundary được tạo ra.
- Unit/integration/E2E coverage được dùng làm lý do bỏ qua một risk runtime dù failure pattern yêu cầu proof ở boundary chạy thật.
- Risk có user/domain behavior implication nhưng không trace tới requirement/acceptance/edge-case có thẩm quyền.
- Plan có risk `APPLIES` nhưng thiếu prevention design hoặc verification strategy.
- Task/evidence triển khai behavior khác prevention design mà spec/plan chưa được cập nhật.
- Feature mới có plan theo contract 1.10+ nhưng thiếu Runtime Risk Design; `legacy-bootstrap` chỉ hợp lệ cho artifact legacy và phải có provenance.

### 5. Gán mức độ nghiêm trọng

Dùng heuristic sau để ưu tiên các phát hiện:

- **CRITICAL**: Vi phạm nguyên tắc MUST của hiến chương, thiếu artifact spec cốt lõi, requirement không có độ bao phủ nào và điều đó chặn chức năng nền tảng, hoặc runtime risk bị bỏ sót làm core P1 entry/auth/integration path không thể sử dụng.
- **HIGH**: Requirement trùng lặp hoặc xung đột, thuộc tính bảo mật/hiệu năng mơ hồ, acceptance criterion không thể kiểm thử, drift giữa spec ↔ plan ↔ tasks/diagram làm thay đổi core business behavior, hoặc runtime risk `APPLIES` chưa có task coverage nhưng chưa chặn toàn bộ P1.
- **MEDIUM**: Thuật ngữ bị trôi nghĩa, thiếu độ bao phủ task phi chức năng, edge case chưa được đặc tả đầy đủ
- **LOW**: Cải thiện phong cách/câu chữ, dư thừa nhỏ không ảnh hưởng thứ tự thực thi

### 6. Tạo báo cáo phân tích cô đọng

Xuất báo cáo Markdown (không ghi file) theo cấu trúc sau:

## Báo cáo phân tích đặc tả

| ID | Danh mục | Mức độ | Vị trí | Tóm tắt | Khuyến nghị |
|----|----------|--------|--------|---------|-------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Hai requirement tương tự nhau ... | Hợp nhất cách diễn đạt; giữ phiên bản rõ ràng hơn |

**Bảng tóm tắt độ bao phủ:**

| Requirement Key | Có Task? | Task IDs | Ghi chú |
|-----------------|----------|----------|---------|

**Vấn đề tuân thủ hiến chương:** (nếu có)

**Task chưa được ánh xạ:** (nếu có)

**Runtime Risk Coverage:**

| Risk ID | Trạng thái suy ra | Task IDs | Đánh giá |
|---------|-------------------|----------|----------|

**Model/diagram consistency:** (nếu có diagram; tóm tắt drift giữa source artifact và visual/downstream)

**Chỉ số:**

- Tổng số Requirement
- Tổng số Task
- Coverage % (requirement có >=1 task)
- Runtime Risk Coverage % (risk `APPLIES` có >=1 task hợp lệ)
- Số runtime risk `NEEDS_UPSTREAM`
- Số false-N/A runtime risk
- Số điểm mơ hồ
- Số điểm trùng lặp
- Số vấn đề Critical
- Số finding liên quan model/diagram drift (nếu có)

### 7. Đưa ra hành động tiếp theo

Ở cuối báo cáo, xuất một block Hành động tiếp theo ngắn gọn:

- Nếu có vấn đề CRITICAL: Khuyến nghị xử lý trước `$speckit-implement`
- Nếu chỉ có LOW/MEDIUM: Người dùng có thể tiếp tục, nhưng đưa ra các gợi ý cải thiện
- Đưa ra gợi ý command rõ ràng, ví dụ: "Chạy $speckit-specify để tinh chỉnh", "Chạy $speckit-plan để điều chỉnh kiến trúc", "Chỉnh thủ công tasks.md để bổ sung độ bao phủ cho 'performance-metrics'"

### 8. Đề nghị khắc phục

Hỏi người dùng: "Bạn có muốn tôi đề xuất các chỉnh sửa khắc phục cụ thể cho N vấn đề ưu tiên cao nhất không?" (**KHÔNG** tự động áp dụng chúng.)

### 9. Kiểm tra extension hook

Sau khi báo cáo, kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry dưới key `hooks.after_analyze`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có field `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook đó và để việc đánh giá condition cho implementation của HookExecutor.
- Khi dựng command invocation từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau dựa trên cờ `optional`:
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation thực tế có thể khác với id `{command}` hiển thị ở trên, ví dụ agent chạy ở skills mode có thể gọi dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua âm thầm.

## Nguyên tắc vận hành

### Hiệu quả ngữ cảnh

- **Token tối thiểu, tín hiệu cao**: Tập trung vào các phát hiện có thể hành động, không viết tài liệu dài dòng
- **Progressive disclosure**: Nạp artifact dần theo nhu cầu; không đổ toàn bộ nội dung vào phân tích
- **Output tiết kiệm token**: Giới hạn bảng phát hiện ở 50 dòng; tóm tắt phần overflow
- **Kết quả xác định**: Chạy lại khi không có thay đổi phải cho ra ID và số lượng nhất quán

### Hướng dẫn phân tích

- **KHÔNG BAO GIỜ sửa file** (đây là phân tích chỉ đọc)
- **KHÔNG BAO GIỜ bịa section bị thiếu** (nếu không có, báo đúng là không có)
- **Ưu tiên vi phạm hiến chương** (luôn ở mức CRITICAL)
- **Ưu tiên ví dụ thay vì quy tắc exhaustive** (trích dẫn trường hợp cụ thể, không nêu pattern chung chung)
- **Báo cáo trường hợp không có vấn đề một cách rõ ràng** (xuất báo cáo thành công kèm thống kê độ bao phủ)

## Ngữ cảnh

$ARGUMENTS

## Optional companion skill — audit stack-specific coverage

Đọc protocol tại `../companion-skills.md`.

Nếu repo có companion phù hợp, `speckit-analyze-vi` MUST dùng nó trong phân tích read-only để:
- audit plan/tasks có bỏ sót stack-specific prevention/evidence obligation không;
- phát hiện rule companion bị materialize sai authority layer;
- phát hiện generated artifact/toolchain/test-harness/browser debt bị coi nhầm đã cover;
- đối chiếu generic Risk ID với implementation obligation cụ thể theo template;
- phân biệt finding của companion với business/spec inconsistency.

Analyze không sửa code/artifact và không re-invent rule đã thuộc canonical `runtime-verification`.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-analyze`
- Tên gốc: `speckit-analyze`
- Chính sách: `faithful`
- Commit nguồn: `566943554c617128f73e2e4864aeb713bacd0478`
