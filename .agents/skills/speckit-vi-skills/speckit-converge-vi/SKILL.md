---
name: "speckit-converge-vi"
description: "Đối chiếu codebase hiện tại với spec, plan và tasks của feature, sau đó bổ sung phần công việc chưa được triển khai thành các task mới ở cuối tasks.md để implement có thể hoàn tất."
compatibility: "Yêu cầu cấu trúc project spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/converge.md"
---


## Dữ liệu người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét dữ liệu người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi converge)**:

- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở root của project hay không.
- Nếu có, đọc file và tìm các entry bên dưới key `hooks.before_converge`.
- Nếu YAML không thể parse hoặc không hợp lệ, không được âm thầm bỏ qua: thông báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm mọi hook bắt buộc (`optional: false`) đã đăng ký trong đó, sau đó tiếp tục như bình thường.
- Lọc bỏ các hook có `enabled` được đặt rõ ràng là `false`. Hook không có field `enabled` mặc định được coi là đã bật.
- Với từng hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook và để việc đánh giá condition cho triển khai HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau dựa trên cờ `optional`:
  - **Hook tùy chọn** (`optional: true`):

    ```text
    ## Hook mở rộng

    **Pre-Hook tùy chọn**: {extension}
    Command: `/{command}`
    Mô tả: {description}

    Prompt: {prompt}
    Để thực thi: `/{command}`
    ```

  - **Hook bắt buộc** (`optional: false`):

    ```text
    ## Hook mở rộng

    **Pre-Hook tự động**: {extension}
    Đang thực thi: `/{command}`
    EXECUTE_COMMAND: {command}

    Hãy chờ kết quả của hook command trước khi tiếp tục sang Mục tiêu.
    ```

    Sau khi phát block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook hoàn tất trước khi tiếp tục. Chạy hook theo đúng cách bạn tự chạy command trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị ở trên; ví dụ agent ở chế độ skills chạy dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ phát block mà không chạy hook thì chưa được tính là đã thực thi.

- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua mà không cần thông báo.

## Mục tiêu

Thu hẹp khoảng cách giữa intent đã được chốt của feature và codebase hiện đang triển khai. Dùng authority chain `constitution > spec.md > plan/design artifacts > tasks.md > implementation state`: spec giữ requirement, plan giữ intended technical design, tasks giữ decomposition, code/runtime phản ánh current state. Đánh giá trạng thái hiện tại của code, xác định requirement, acceptance criteria, core behavior/domain/lifecycle, quyết định trong plan và task hiện có nào chưa được đáp ứng, chưa hoàn chỉnh hoặc mới chỉ được đáp ứng một phần, rồi **append từng phần công việc còn lại thành một task mới có thể truy vết** ở cuối `tasks.md` để `$speckit-implement` có thể hoàn tất. Command này **BẮT BUỘC** chỉ được chạy sau khi `$speckit-implement` đã chạy trên `tasks.md` hiện tại và sau khi `$speckit-tasks` đã tạo ra một `tasks.md` hoàn chỉnh.

Đây **không phải** công cụ diff và **không** theo dõi thay đổi. Nó đánh giá trạng thái hiện tại của code so với các artifact của feature — không dùng git, không so sánh branch, không dùng history.

## Ràng buộc vận hành

**CHỈ APPEND, KHÔNG BAO GIỜ REWRITE**: Đối với artifact có thẩm quyền của feature, phần ghi **duy nhất** mà converge được phép thực hiện là append một section mới `## Phase N: Convergence` vào `tasks.md`. Lazy Modeling Gate/Mandatory final modeling MAY cập nhật derived artifact `.modeling-state.json` và diagram tương ứng. Command **KHÔNG ĐƯỢC**:

- sửa `spec.md`, `plan.md` hoặc technical design artifact dưới bất kỳ hình thức nào;
- rewrite, renumber, reorder hoặc xóa bất kỳ task hiện có nào (bao gồm task từ một phase Convergence trước đó);
- sửa, tạo hoặc xóa application code — việc hoàn thành các task mới append là nhiệm vụ của `$speckit-implement`.

Khi codebase đã đáp ứng mọi thứ, command **BẮT BUỘC** giữ `tasks.md` **không thay đổi từng byte** (không thêm header Convergence rỗng) và báo kết quả sạch.

**Thẩm quyền của Constitution**: Constitution của project (`.specify/memory/constitution.md`) là **không thể thương lượng**. Code vi phạm một nguyên tắc MUST là finding có mức độ nghiêm trọng cao nhất và phải tạo task khắc phục tương ứng. Nếu constitution vẫn là template chưa được điền, bỏ qua kiểm tra constitution một cách bình thường thay vì fail.

## Các bước thực thi

### 1. Khởi tạo ngữ cảnh Convergence

Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec -RequireTasks -IncludeTasks` một lần từ root của repo và parse JSON để lấy FEATURE_DIR và AVAILABLE_DOCS. Suy ra các đường dẫn tuyệt đối:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md
- CONSTITUTION = `.specify/memory/constitution.md` (nếu tồn tại)

Nếu thiếu `spec.md`, `plan.md` hoặc `tasks.md`, **DỪNG** với thông báo rõ ràng, có thể hành động được và nêu đúng command prerequisite cần chạy (`$speckit-specify` nếu thiếu spec, `$speckit-plan` nếu thiếu plan, `$speckit-tasks` nếu thiếu tasks). Không tạo output một phần.

Với argument chứa dấu nháy đơn như "I'm Groot", dùng cú pháp escape: ví dụ `'I'\''m Groot'` (hoặc dùng nháy kép nếu có thể: `"I'm Groot"`).

### 2. Lazy Modeling Gate — latest implementation phase

Trước khi đánh giá convergence:

1. resolve phase implementation hoàn tất gần nhất từ `tasks.md` và current implementation state;
2. chạy `ensure-model(implementation:phase-XX)` cho phase đó;
3. nếu gate pass + fresh → tiếp tục;
4. nếu thiếu/stale/output mất/state legacy → tự invoke `$speckit-system-modeling-vi` ở mode `implementation` với scope phase đó, chờ hoàn tất rồi kiểm tra lại;
5. nếu gate `blocked`, dừng convergence analysis cho tới khi conflict/upstream issue được xử lý.

Người dùng không cần gọi modeling thủ công sau `$speckit-implement`.

### 3. Nạp artifact theo Progressive Disclosure

Chỉ nạp lượng context tối thiểu cần thiết từ mỗi artifact:

**Từ spec.md:**

- Functional Requirements (FR-###)
- Success Criteria (SC-###) — chỉ bao gồm các mục đòi hỏi công việc có thể triển khai; loại trừ outcome metric sau launch và business KPI
- User Stories và Acceptance Scenarios tương ứng
- Edge Cases (nếu có)

**Từ diagram dẫn xuất (nếu cần):**

- `spec-diagram/`, `plan-diagram/`, `implementation-diagram/` chỉ dùng như visual aid/current-state map.
- Không dùng diagram làm nguồn intent độc lập.

**Từ plan.md:**

- Lựa chọn architecture/stack và các quyết định kỹ thuật
- Tham chiếu Data Model
- Các phase và touch-point được nêu tên (file/component mà plan nói sẽ được tạo hoặc chỉnh sửa)
- Ràng buộc kỹ thuật

**Từ tasks.md:**

- Task ID (để tính ID tiếp theo và số phase tiếp theo)
- Mô tả, nhóm phase và các file path được tham chiếu
- `Runtime Risk Coverage`, mapping Risk ID → Task ID / lý do N/A và trạng thái/evidence nếu đã được ghi nhận

**Từ runtime-verification:**

- Nạp `.agents/skills/runtime-verification/SKILL.md`.
- Đọc `references/catalog-index.md`, sau đó chỉ nạp category file liên quan tới runtime surface/current architecture.
- Dùng catalog để kiểm tra lại applicability từ current code/config/runtime; catalog không thay thế spec/plan làm nguồn intent.

**Từ constitution (nếu không phải template chưa được điền):**

- Tên nguyên tắc và các statement chuẩn tắc MUST/SHOULD

**Từ project-level docs bị tác động (nếu spec/plan/tasks đã chỉ định):**

- Chỉ đọc các file trong `docs/` được `Project Docs Impact`, `Project Docs Promotion Plan` hoặc task promotion tham chiếu.
- Đối chiếu mental model tổng thể với feature đã implement; không dùng project-level docs stale để phủ định active spec.

### 4. Xây dựng Intent Inventory

Tạo một mô hình nội bộ (không lặp lại nguyên văn các artifact):

- **Requirements inventory**: một key ổn định cho mỗi FR-### / SC-### / acceptance scenario của user story (ví dụ `US1/AC2`), cùng với các quyết định trong plan và nguyên tắc constitution tạo ra nghĩa vụ có thể triển khai.
- **System-semantics map**: suy trực tiếp từ `spec.md` và intended technical design khi cần để kiểm tra implementation không làm mất hoặc bóp méo core behavior/lifecycle.
- **Code-scope map**: từ các file path được nêu trong `plan.md` và `tasks.md`, cộng với tìm kiếm theo từ khóa cho các khái niệm mà từng requirement mô tả, suy ra tập source file và component thuộc phạm vi đánh giá. Giới hạn đánh giá trong phạm vi này — **không** suy diễn scope vượt quá những gì artifact đã định nghĩa.
- **Project-docs promotion map**: ánh xạ từng thay đổi **đã implement + verify** tới project-level doc/diagram phải phản ánh trạng thái hiện hành; planned change chưa implement không được yêu cầu promote.
- **Runtime-risk trace map**: từ catalog + current architecture xác định `Risk → Requirement refs → Prevention design → Task → Evidence`; risk nào thực sự áp dụng, đoạn trace nào missing/contradict, false-N/A và evidence nào vẫn BLOCKED/STALE/CONTAMINATED.
- Với plan `legacy-bootstrap`, phân biệt thiếu traceability do artifact cũ với regression mới; không tự rewrite lịch sử plan chỉ để đạt format 1.10+.
- **Runtime lesson candidates**: failure quan sát được trong implementation/runtime nhưng chưa có pattern tương ứng trong catalog; chỉ giữ candidate nếu có thể mô tả điều kiện kích hoạt, symptom, root cause, vì sao verification cũ bỏ sót và task-generation rule có thể tái sử dụng qua project khác.

### 5. Đánh giá codebase và phân loại finding

Đưa mọi task hiện có vào intent inventory, bất kể trạng thái checkbox hay phase Convergence: tuyên bố hoàn thành không phải là bằng chứng. Xác minh hành vi hiện tại dựa trên constitution, spec, plan/design artifacts và tasks; với chuỗi task khắc phục, đánh giá hành vi kết quả chứ không đánh giá chi tiết triển khai đã bị thay thế. Kiểm tra cả nghĩa vụ chưa được đáp ứng lẫn phần triển khai mâu thuẫn, vượt quá hoặc nằm ngoài ý định đã nêu.

Với mỗi item trong intent inventory, kiểm tra code hiện tại trong scope và chỉ tạo một `Finding` khi có khoảng trống. **Thiếu promotion vào project-level docs cho capability đã implement + verify là một finding có thể hành động**, ngay cả khi code đã đúng. Phân loại từng finding theo **gap type**:

- **`missing`**: công việc bắt buộc hoàn toàn chưa có trong code.
- **`partial`**: công việc đã có nhưng chưa đáp ứng đầy đủ requirement / acceptance criterion / quyết định trong plan.
- **`contradicts`**: code thực hiện điều gì đó xung đột với ý định đã nêu hoặc một nguyên tắc MUST của constitution.
- **`unrequested`**: code chứa phần việc không được yêu cầu/biện minh bởi spec, plan/design artifacts hoặc tasks (đưa ra để nhận biết — converge **không** xóa code, chỉ append một task để review/justify hoặc remove phần đó).

Runtime-specific:
- Risk catalog xác định `APPLIES` nhưng requirement/design/task/evidence bắt buộc bị thiếu → finding `missing` hoặc `partial` với source-ref `runtime:<Risk ID>`.
- Risk được ghi `NOT_APPLICABLE` nhưng current architecture chứng minh ngược lại → finding `contradicts`.
- Runtime validation bắt buộc còn `BLOCKED`/unavailable thì capability chưa được coi là verified.
- Failure mới có tính tổng quát nhưng chưa có trong catalog → ghi một **Runtime Lesson Candidate** trong report; do converge có ràng buộc append-only đối với feature artifact, **không tự sửa failure catalog** trong command này.

Mỗi `Finding` ghi lại: một id ổn định, `source-ref` mà finding truy vết tới, `gap-type`, severity và mô tả ngắn, dễ hiểu kèm bằng chứng (file/khu vực đã quan sát).

**Edge case:**

- **Có rất ít hoặc chưa có code**: coi toàn bộ scope được chỉ định là phần công việc `missing` còn lại thay vì fail.
- **Không còn gì phải làm**: tạo zero finding và đi theo nhánh converged ở Bước 8.

### 6. Gán mức độ nghiêm trọng

- **CRITICAL**: vi phạm một nguyên tắc MUST của constitution, khoảng trống `missing`/`contradicts` làm chặn chức năng nền tảng của một user story P1, hoặc runtime-risk gap khiến core P1 entry/auth/integration flow không thể dùng.
- **HIGH**: khoảng trống `missing` hoặc `partial` trên một functional requirement cốt lõi/acceptance criterion, hoặc runtime risk `APPLIES` chưa được cover/verify đầy đủ nhưng chưa chặn toàn bộ P1.
- **MEDIUM**: khoảng trống `partial` trên requirement thứ cấp, hoặc phần bổ sung `unrequested` chưa rõ lý do.
- **LOW**: khoảng trống partial nhỏ, phần polish hoặc phần bổ sung `unrequested` có rủi ro thấp.

### 7. Trình bày tóm tắt finding trong session

Trước khi append bất cứ thứ gì, xuất một bản tóm tắt gọn, phân theo severity (chưa ghi file ở bước này):

## Phát hiện Convergence

| ID | Gap Type | Severity | Nguồn | Bằng chứng | Công việc còn lại |
|----|----------|----------|-------|-----------|-------------------|
| F1 | missing  | HIGH     | FR-008 | Ví dụ: không phát hiện guard append-only trong path/to/module.py khi ghi tasks.md | Bổ sung cơ chế đảm bảo append-only |

**Các chỉ số tóm tắt:**

- Số requirement / acceptance criterion đã kiểm tra
- Số quyết định trong plan đã kiểm tra
- Số nguyên tắc constitution đã kiểm tra (hoặc "bỏ qua — template")
- Số finding theo gap type (missing / partial / contradicts / unrequested)
- Số finding theo severity
- Số Runtime Risk `APPLIES`, số risk chưa cover/verify và số false-N/A
- Số Runtime Lesson Candidate mới (nếu có)

### 8. Append task Convergence (hoặc xác định converged)

**Nếu có một hoặc nhiều finding có thể hành động** (outcome `tasks_appended`):

Append vào **cuối** `tasks.md`, theo đúng contract append:

1. Quét toàn bộ task ID hiện có; gọi `M` là giá trị lớn nhất. Xác định số phase tiếp theo `N` (phase hiện có cao nhất + 1).
2. Ghi một section header mới duy nhất `## Phase N: Convergence`.
3. Phát một checklist item cho mỗi actionable finding, ưu tiên CRITICAL/HIGH trước, gán ID có zero-padding `T{M+1:03d}, T{M+2:03d}, …`:

   ```markdown
   - [ ] T042 <imperative description> per <source-ref> (<gap-type>)
   ```

   `<source-ref>` truy vết task về nguồn gốc của nó: ví dụ `FR-003`, `SC-002`, `US1/AC2`, `plan: storage decision`, `Constitution II`, `runtime:WEB-ROUTE-001`.

   `<gap-type>` là một trong `missing`, `partial`, `contradicts`, `unrequested`.

   Task vi phạm constitution **BẮT BUỘC** phải được phát trước và mô tả là `CRITICAL`.
4. Không bao giờ tái sử dụng hoặc renumber ID hiện có. Nếu đã có một phase Convergence trước đó, thêm một phase mới, có số riêng ở bên dưới — không chạm vào phase cũ.

**Nếu không có finding có thể hành động** (outcome `converged`):

- **Không** sửa `tasks.md` — không thêm phase header rỗng.
- Xác định internal outcome là `converged`, nhưng **chưa phát thông báo hoàn tất cuối cùng** cho tới khi Final Modeling Gate pass.
- Chỉ xác định outcome `converged` khi Project Docs Promotion Check cũng sạch: mọi capability đã implement + verify đã được promote vào project-level docs/diagram liên quan hoặc feature không tác động mental model chung; planned-only semantics chưa implement không được xuất hiện trong `docs/`.
- Đồng thời, mọi Runtime Risk `APPLIES` phải có task/evidence hoàn tất; không còn false-N/A hoặc runtime validation bắt buộc ở trạng thái `FAIL/BLOCKED/unavailable`.
- Giữ số liệu tóm tắt để báo sau Final Modeling Gate.

### 9. Cung cấp hành động tiếp theo (Handoff)

- Với `tasks_appended`: nêu số task đã append và phase tương ứng, đồng thời khuyến nghị chạy `$speckit-implement` để hoàn tất chúng; lưu ý rằng lần converge tiếp theo sẽ tìm thấy ít hoặc không còn item nào.
- Với `converged`: chuẩn bị khuyến nghị chuyển sang review / mở PR, nhưng chỉ phát handoff cuối cùng sau Final Modeling Gate.

### 10. Kiểm tra extension hook

Sau khi tạo kết quả, kiểm tra xem `.specify/extensions.yml` có tồn tại ở root của project hay không.

- Nếu có, đọc file và tìm các entry bên dưới key `hooks.after_converge`.
- Nếu YAML không thể parse hoặc không hợp lệ, không được âm thầm bỏ qua: thông báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm mọi hook bắt buộc (`optional: false`) đã đăng ký trong đó, sau đó tiếp tục như bình thường.
- Lọc bỏ các hook có `enabled` được đặt rõ ràng là `false`. Hook không có field `enabled` mặc định được coi là đã bật.
- Với từng hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook và để việc đánh giá condition cho triển khai HookExecutor.
- Có thể nêu **provisional outcome** (`converged` hoặc `tasks_appended`) trước hook để phục vụ hook/follow-up, nhưng không tuyên bố command hoàn tất trước Final Modeling Gate.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau dựa trên cờ `optional`:
  - **Hook tùy chọn** (`optional: true`):

    ```text
    ## Hook mở rộng

    **Hook tùy chọn**: {extension}
    Command: `/{command}`
    Mô tả: {description}

    Prompt: {prompt}
    Để thực thi: `/{command}`
    ```

  - **Hook bắt buộc** (`optional: false`):

    ```text
    ## Hook mở rộng

    **Hook tự động**: {extension}
    Đang thực thi: `/{command}`
    EXECUTE_COMMAND: {command}
    ```

    Sau khi phát block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook hoàn tất trước khi tiếp tục. Chạy hook theo đúng cách bạn tự chạy command trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị ở trên; ví dụ agent ở chế độ skills chạy dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ phát block mà không chạy hook thì chưa được tính là đã thực thi.

- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua mà không cần thông báo.

## Final Modeling Gate sau Converge

Trước khi báo cáo converge hoàn tất, **luôn** chạy `$speckit-system-modeling-vi` ở mode `converge`.

- Đây là final gate vì không có phase kế tiếp đảm nhiệm lazy check.
- Diagram Check có thể âm; khi đó ghi `no-diagram-needed` trong `.modeling-state.json` và không tạo file.
- Khi cần visual, output nằm trong `FEATURE_DIR/converge-diagram/`.
- Gap diagram phải trace về spec/plan/task; không trở thành nguồn task độc lập.
- Chỉ báo outcome cuối cùng sau khi gate `converge` đã pass.
- Sau gate pass: nếu outcome là `converged`, báo **"✅ Converged — phần triển khai đáp ứng spec, intended technical design, plan và tasks."**; nếu outcome là `tasks_appended`, báo phase/task đã append và handoff sang `$speckit-implement`.

## Optional companion skill — convergence audit

Đọc protocol tại `../companion-skills.md`.

Nếu repo có companion phù hợp, Converge MUST audit thêm:
- stack-specific prevention trong plan/tasks đã hiện diện trong current implementation chưa;
- deferred browser/runtime evidence còn task mở đúng không;
- generated artifact có stale/hand-edit/drift không;
- toolchain/canonical command có drift giữa config, CI và docs không;
- test harness/mock/runtime provenance có debt chưa materialize thành task không;
- generic runtime lesson mới có cần promote upstream hay chỉ là local/template incident.

Gap đủ thực tế phải append thành task convergence cụ thể; không đánh converged nếu companion-required evidence còn thiếu.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-converge`
- Tên gốc: `speckit-converge`
- Chính sách: `faithful`
- Commit nguồn: `390659c4ee776dfaca1eb1049862652611f962d2`
