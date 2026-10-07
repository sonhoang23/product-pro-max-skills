---
name: "speckit-tasks-vi"
description: "Tạo file tasks.md có thể thực thi ngay, được sắp xếp theo thứ tự phụ thuộc cho feature dựa trên các tài liệu thiết kế hiện có."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/tasks.md"
---


## Dữ liệu đầu vào của người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét dữ liệu đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi tạo tasks)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của project hay không.
- Nếu có, đọc file và tìm các mục trong key `hooks.before_tasks`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: hãy báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser), đồng thời cho biết không có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại bỏ các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có field `enabled` được coi là bật theo mặc định.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa một `condition` không rỗng, bỏ qua hook đó và để việc đánh giá condition cho implementation của HookExecutor.
- Khi tạo lệnh gọi từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ, `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo flag `optional`:
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục. Hãy chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách gọi thực tế có thể khác với id `{command}` hiển thị ở trên; ví dụ agent ở skills mode có thể chạy dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không chạy hook thì chưa được tính là đã thực thi.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Quy trình

1. **Thiết lập**: Chạy `.specify/scripts/powershell/setup-tasks.ps1 -Json` từ thư mục gốc của repo và parse `FEATURE_DIR`, `TASKS_TEMPLATE_CONTENT`, `TASKS_TEMPLATE` cùng danh sách `AVAILABLE_DOCS`. Khi có giá trị, `FEATURE_DIR` và `TASKS_TEMPLATE` phải là đường dẫn tuyệt đối. `AVAILABLE_DOCS` là danh sách tên tài liệu/đường dẫn tương đối có trong `FEATURE_DIR` (ví dụ `research.md` hoặc `contracts/`). Với dấu nháy đơn trong tham số như "I'm Groot", dùng cú pháp escape, ví dụ: 'I'\''m Groot' (hoặc dùng dấu nháy kép nếu có thể: "I'm Groot").

2. **Lazy Modeling Gate — plan**:
   - Sau khi resolve `FEATURE_DIR`, chạy `ensure-model(plan)` theo contract trong `speckit-system-modeling-vi`.
   - Nếu gate `plan` pass + fresh thì tiếp tục ngay.
   - Nếu thiếu/stale/output mất/state legacy, tự invoke `$speckit-system-modeling-vi` ở mode `plan`, chờ hoàn tất rồi kiểm tra lại.
   - Không yêu cầu người dùng gọi modeling thủ công giữa `$speckit-plan` và `$speckit-tasks`.
   - Nếu gate bị `blocked`, không tạo tasks cho tới khi upstream plan/design artifact được sửa.

3. **Nạp tài liệu thiết kế**: Đọc từ `FEATURE_DIR`:
   - **Bắt buộc**: `plan.md` (tech stack, thư viện, cấu trúc), `spec.md` (user story cùng mức ưu tiên).
   - **NẾU CÓ `spec-diagram/` hoặc `plan-diagram/`**: chỉ dùng như visual aid khi cần hiểu boundary/flow/architecture; không dùng diagram làm nguồn requirement hay technical decision độc lập.
   - **Tùy chọn**: `data-model.md` (entity), `contracts/` (interface contract), `research.md` (quyết định), `quickstart.md` (test scenario).
   - **NẾU TỒN TẠI**: Nạp `.specify/memory/constitution.md` để lấy các nguyên tắc của project và ràng buộc governance.
   - **NẾU CÓ**: Nạp `Project Docs Impact` từ `spec.md` và `Project Docs Promotion Plan` từ `plan.md`; chỉ đọc các project-level docs được chỉ định khi cần tạo **promotion task** cụ thể.
   - **BẮT BUỘC**: Nạp `.agents/skills/runtime-verification/SKILL.md` ở mode `tasks`. Ưu tiên `Runtime Risk Design` trong `plan.md` như inventory design authoritative, rồi đọc `lifecycle-profile.md` + catalog router để refresh đúng Risk ID/category liên quan; không đổ toàn bộ catalog vào context.
   - **Legacy compatibility**: nếu plan cũ chưa có `Runtime Risk Design`, MAY bootstrap design evaluation read-only và đánh dấu `legacy-bootstrap`; không giả vờ rằng plan legacy đã có traceability mới.
   - Lưu ý: Không phải project nào cũng có đầy đủ các tài liệu trên. Hãy tạo task dựa trên những gì hiện có.

4. **Thực thi workflow tạo task**:
   - Nạp `plan.md` và trích xuất tech stack, thư viện, cấu trúc project.
   - Nạp `spec.md` và trích xuất user story cùng mức ưu tiên (P1, P2, P3, v.v.).
   - Nếu có `data-model.md`: Trích xuất entity và ánh xạ chúng vào user story.
   - Nếu có `contracts/`: Ánh xạ interface contract vào user story.
   - Nếu có `research.md`: Trích xuất các quyết định dùng cho task thiết lập.
   - **Runtime Risk Check — BẮT BUỘC trước khi chốt task**:
     - Bắt đầu từ `Runtime Risk Design` của plan; refresh catalog chỉ để bắt architecture drift, false-N/A hoặc pattern mới liên quan, không thiết kế lại từ đầu.
     - Với mỗi risk `APPLIES`, giữ trace `Risk ID → Requirement refs (nếu có) → Prevention design → Task IDs → Required evidence`.
     - Tạo ít nhất một task phòng ngừa hoặc verification cụ thể và đặt task vào **đúng phase/user story nơi risk được tạo ra**. Không gom mặc định thành một task "runtime test cuối dự án".
     - Task runtime-risk là nghĩa vụ delivery bắt buộc khi risk áp dụng, kể cả khi feature không bật TDD hoặc không yêu cầu test tổng quát.
     - Nếu cùng một task đã bao phủ risk, tái sử dụng task đó và ghi traceability tới Risk ID; không tạo task trùng.
     - Nếu refresh phát hiện `NEEDS_UPSTREAM` hoặc prevention design thiếu/contradict spec, **không đoán**. Báo upstream gap và chưa coi `tasks.md` là hoàn tất cho tới khi artifact có thẩm quyền được sửa.
     - Với legacy-bootstrap, ghi provenance trong Runtime Risk Coverage để Analyze biết inventory không originate từ plan 1.10+.
   - Tạo task được tổ chức theo user story (xem Quy tắc tạo task bên dưới).
   - Tạo dependency graph thể hiện thứ tự hoàn thành các user story.
   - Tạo ví dụ thực thi song song cho từng user story.
   - Kiểm tra tính đầy đủ của task (mỗi user story có đủ task cần thiết và có thể được kiểm thử độc lập).
   - Nếu feature tác động mental model chung, tạo promotion task cho từng project-level doc/diagram bị ảnh hưởng và **gắn task đó vào đúng implementation phase tạo ra capability tương ứng**. Promotion task phải đứng sau implementation + test/QA của phase và chỉ được chạy sau gate `implementation:phase-XX` fresh; task phải có đường dẫn file cụ thể và mô tả semantics implemented cần promote.

5. **Tạo `tasks.md`**: Dùng `TASKS_TEMPLATE_CONTENT` (từ JSON output ở trên) làm cấu trúc. Để tương thích với các setup script cũ không trả về `TASKS_TEMPLATE_CONTENT`, hãy đọc `TASKS_TEMPLATE` thay thế. Điền:
   - Tên feature chính xác từ `plan.md`.
   - Thêm section `## Runtime Risk Coverage` trước các phase, với bảng tối thiểu: `Risk ID | Trạng thái | Requirement refs | Prevention design | Task IDs / lý do N/A | Required evidence`. Mọi risk `APPLIES` phải map tới ít nhất một Task ID; `NOT_APPLICABLE` phải có lý do ngắn; không ghi `PASS` ở giai đoạn tạo task vì chưa có runtime evidence.
   - Phase 1: Task thiết lập (khởi tạo project).
   - Phase 2: Task nền tảng (điều kiện tiên quyết chặn tất cả user story).
   - Phase 3+: Mỗi user story là một phase riêng (theo thứ tự ưu tiên trong `spec.md`).
   - Mỗi phase gồm: mục tiêu story, tiêu chí kiểm thử độc lập, test (nếu được yêu cầu), task implementation.
   - Phase cuối: Hoàn thiện và các vấn đề xuyên suốt.
   - Không gom promotion mặc định vào phase cuối. Với mỗi phase có thay đổi project mental model, thêm nhóm **Project Docs Promotion** ở cuối chính phase đó, sau validation/modeling. Phase cuối chỉ giữ convergence/polish còn lại. Không tạo task docs chung chung nếu feature không tác động mental model xuyên repo.
   - Tất cả task phải tuân thủ nghiêm ngặt checklist format (xem Quy tắc tạo task bên dưới).
   - Đường dẫn file rõ ràng cho từng task.
   - Phần dependencies thể hiện thứ tự hoàn thành story.
   - Ví dụ thực thi song song cho từng story.
   - Phần chiến lược implementation (MVP trước, bàn giao tăng dần).

## Hook bắt buộc sau khi thực thi

**Bạn BẮT BUỘC phải hoàn thành phần này trước khi báo cáo hoàn tất cho người dùng.**

Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của project hay không.
- Nếu không tồn tại, hoặc không có hook nào đăng ký trong `hooks.after_tasks`, chuyển đến Báo cáo hoàn tất.
- Nếu có, đọc file và tìm các mục trong key `hooks.after_tasks`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: hãy báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser), đồng thời cho biết không có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó chuyển đến Báo cáo hoàn tất.
- Loại bỏ các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có field `enabled` được coi là bật theo mặc định.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa một `condition` không rỗng, bỏ qua hook đó và để việc đánh giá condition cho implementation của HookExecutor.
- Khi tạo lệnh gọi từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ, `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo flag `optional`:
  - **Hook bắt buộc** (`optional: false`) — bạn **BẮT BUỘC** phải xuất `EXECUTE_COMMAND:` cho từng hook bắt buộc:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục. Hãy chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách gọi thực tế có thể khác với id `{command}` hiển thị ở trên; ví dụ agent ở skills mode có thể chạy dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không chạy hook thì chưa được tính là đã thực thi.
  - **Hook tùy chọn** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Báo cáo hoàn tất

Xuất đường dẫn đến file `tasks.md` đã tạo cùng phần tóm tắt:
- Tổng số task.
- Số task cho từng user story.
- Số Runtime Risk `APPLIES`, `NOT_APPLICABLE`, `NEEDS_UPSTREAM` và các Task ID đang cover risk áp dụng.
- Các cơ hội thực thi song song đã xác định.
- Tiêu chí kiểm thử độc lập cho từng story.
- Phạm vi MVP được đề xuất (thường chỉ gồm User Story 1).
- Kiểm tra format: Xác nhận TẤT CẢ task đều tuân thủ checklist format (checkbox, ID, label, đường dẫn file).

Ngữ cảnh tạo task: $ARGUMENTS

File `tasks.md` phải có thể được thực thi ngay — mỗi task phải đủ cụ thể để một LLM hoàn thành mà không cần thêm ngữ cảnh.

Không bắt buộc chạy modeling `tasks` ngay tại cuối command. `$speckit-implement` sẽ tự chạy `ensure-model(tasks)` trước khi bắt đầu implementation. Người dùng MAY gọi `$speckit-system-modeling-vi` thủ công nếu muốn xem dependency/critical-path diagram sớm.

## Quy tắc tạo task

**NGHIÊM TRỌNG**: Task **BẮT BUỘC** phải được tổ chức theo user story để cho phép implementation và kiểm thử độc lập.

**Test là TÙY CHỌN**: Chỉ tạo task test thông thường nếu feature specification yêu cầu rõ ràng hoặc người dùng yêu cầu cách tiếp cận TDD. Quy tắc này **KHÔNG** miễn các task phòng ngừa/verification bắt buộc do Runtime Risk Check xác định.

### Checklist format (BẮT BUỘC)

Mọi task **BẮT BUỘC** phải tuân thủ nghiêm ngặt format sau:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Các thành phần của format**:

1. **Checkbox**: LUÔN bắt đầu bằng `- [ ]` (markdown checkbox).
2. **Task ID**: Số thứ tự liên tiếp (T001, T002, T003...) theo thứ tự thực thi.
3. **Dấu [P]**: CHỈ thêm khi task có thể chạy song song (khác file, không phụ thuộc vào task chưa hoàn thành).
4. **Label [Story]**: BẮT BUỘC chỉ với task thuộc phase user story.
   - Format: [US1], [US2], [US3], v.v. (ánh xạ tới user story trong `spec.md`).
   - Phase Setup: KHÔNG có label story.
   - Phase Foundational: KHÔNG có label story.
   - Phase User Story: BẮT BUỘC có label story.
   - Phase Polish: KHÔNG có label story.
5. **Description**: Hành động rõ ràng kèm đường dẫn file chính xác.

**Ví dụ**:

- ✅ ĐÚNG: `- [ ] T001 Create project structure per implementation plan`
- ✅ ĐÚNG: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ ĐÚNG: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ ĐÚNG: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ SAI: `- [ ] Create User model` (thiếu ID và label Story).
- ❌ SAI: `T001 [US1] Create model` (thiếu checkbox).
- ❌ SAI: `- [ ] [US1] Create User model` (thiếu Task ID).
- ❌ SAI: `- [ ] T001 [US1] Create model` (thiếu đường dẫn file).

### Cách tổ chức task

1. **Từ User Story (`spec.md`)** - CÁCH TỔ CHỨC CHÍNH:
   - Mỗi user story (P1, P2, P3...) có phase riêng.
   - Ánh xạ tất cả thành phần liên quan vào story tương ứng:
     - Model cần cho story đó.
     - Service cần cho story đó.
     - Interface/UI cần cho story đó.
     - Nếu có yêu cầu test: Test dành riêng cho story đó.
   - Đánh dấu dependency giữa các story (đa số story nên độc lập).

2. **Từ Contract**:
   - Ánh xạ từng interface contract → user story mà nó phục vụ.
   - Nếu có yêu cầu test: Mỗi interface contract → một task contract test [P] trước implementation trong phase của story đó.

3. **Từ Data Model**:
   - Ánh xạ từng entity vào user story cần entity đó.
   - Nếu entity phục vụ nhiều story: Đặt ở story sớm nhất hoặc phase Setup.
   - Relationship → task service layer trong phase story phù hợp.
   - Với mỗi field có constraint trong `data-model.md` (độ dài tối đa, nullable/required, giá trị enum, quy tắc validation), trích nguyên văn constraint vào mô tả task để không phải quyết định lại trong lúc implementation.

4. **Từ Setup/Infrastructure**:
   - Hạ tầng dùng chung → phase Setup (Phase 1).
   - Task nền tảng/chặn tiến độ → phase Foundational (Phase 2).
   - Thiết lập riêng cho từng story → nằm trong phase của story đó.

### Cấu trúc phase

- **Phase 1**: Setup (khởi tạo project).
- **Phase 2**: Foundational (điều kiện tiên quyết chặn tiến độ - BẮT BUỘC hoàn thành trước các user story).
- **Phase 3+**: User Story theo thứ tự ưu tiên (P1, P2, P3...).
  - Trong mỗi story: Test (nếu được yêu cầu) → Model → Service → Endpoint → Integration.
  - Mỗi phase phải là một increment hoàn chỉnh, có thể kiểm thử độc lập.
- **Phase cuối**: Polish & Cross-Cutting Concerns.

## Hoàn tất khi

- [ ] Lazy Modeling Gate `plan` đã pass + fresh trước khi tạo tasks.
- [ ] Đã tạo `tasks.md` với đầy đủ phase, task ID và đường dẫn file.
- [ ] Đã có `Runtime Risk Coverage`; mọi risk `APPLIES` đều map tới task cụ thể ở đúng phase/story, mọi `NOT_APPLICABLE` đều có lý do, và không còn risk `NEEDS_UPSTREAM` chưa xử lý.
- [ ] Khi feature tác động project-level docs, `tasks.md` đã có promotion task cụ thể gắn với đúng implementation phase và không task nào cho phép project docs đi trước verified implementation.
- [ ] Extension hook đã được chạy hoặc bỏ qua theo đúng quy tắc trong phần Hook bắt buộc sau khi thực thi ở trên.
- [ ] Đã báo cáo hoàn tất cho người dùng với tổng số task, phân bổ theo story và phạm vi MVP.

## Optional companion skill — BẮT BUỘC khi repo cài companion

Đọc protocol tại `../companion-skills.md`.

Trước khi hoàn tất `tasks.md`:
1. discover/load companion phù hợp;
2. đọc các reference liên quan đến boundary đã được plan chọn;
3. với mỗi guardrail áp dụng, map thành task cụ thể tại phase/story tạo boundary;
4. tái sử dụng Risk ID từ `runtime-verification` khi có; không tạo catalog local cạnh tranh;
5. task phải ghi **required evidence** đủ để implementation biết khi nào được `[x]`;
6. browser/runtime/generated-artifact obligation không được bỏ chỉ vì test “optional”;
7. không dồn mặc định mọi companion obligation thành QA cuối nếu failure có thể được phòng sớm hơn.

Nếu browser QA được chủ động defer, task bắt buộc browser evidence vẫn phải giữ trạng thái chưa hoàn tất cho tới khi proof thật sự chạy.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-tasks`
- Tên gốc: `speckit-tasks`
- Chính sách: `faithful`
- Commit nguồn: `566943554c617128f73e2e4864aeb713bacd0478`
