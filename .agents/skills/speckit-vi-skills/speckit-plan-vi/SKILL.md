---
name: "speckit-plan-vi"
description: "Thực thi workflow lập kế hoạch implementation bằng template plan để tạo các artifact thiết kế."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/plan.md"
---


## Đầu vào của người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi lập kế hoạch)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.before_plan`.
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục sang phần Outline. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Quy trình tổng quát

1. **Thiết lập**: Chạy `.specify/scripts/powershell/setup-plan.ps1 -Json` từ thư mục gốc repo và parse JSON để lấy FEATURE_SPEC, IMPL_PLAN, FEATURE_DIR, BRANCH. Với dấu nháy đơn trong tham số như `"I'm Groot"`, dùng cú pháp escape, ví dụ: `'I'\''m Groot'` (hoặc dùng dấu nháy kép nếu có thể: `"I'm Groot"`).

2. **Lazy Modeling Gate — spec**:
   - Sau khi resolve `FEATURE_DIR`, chạy `ensure-model(spec)` theo contract trong `speckit-system-modeling-vi`.
   - Đọc `FEATURE_DIR/.modeling-state.json`. Nếu gate `spec` đang pass + fresh thì tiếp tục ngay.
   - Nếu gate thiếu, stale, output mất hoặc feature cũ chưa có state, tự invoke `$speckit-system-modeling-vi` ở mode `spec`, chờ hoàn tất rồi kiểm tra lại.
   - Không yêu cầu người dùng gọi modeling thủ công trước `$speckit-plan`.
   - Nếu modeling trả `blocked` vì conflict/ambiguity upstream, dừng planning và báo artifact cần sửa.

3. **Nạp ngữ cảnh**:
   - Đọc FEATURE_SPEC và `.specify/memory/constitution.md`. Constitution là constraint cao nhất; FEATURE_SPEC (`spec.md`) là nguồn requirement chính.
   - Nếu tồn tại `FEATURE_DIR/spec-diagram/`, chỉ dùng các diagram này như visual aid dẫn xuất từ `spec.md`; diagram không phải nguồn requirement độc lập.
   - Nếu diagram spec mâu thuẫn với `spec.md` hoặc constitution, ưu tiên artifact text có thẩm quyền và yêu cầu đồng bộ lại bằng `$speckit-system-modeling-vi`.
   - Nạp template IMPL_PLAN (đã được copy sẵn).
   - Nếu `spec.md` có **Project Docs Impact**, đọc đúng các project-level docs được liệt kê để hiểu mental model hiện hành và xem chúng là **candidate promotion target sau implementation**; chúng không thay thế requirement/technical authority của spec/plan.

3a. **Runtime Design Risk Check — BẮT BUỘC**:
   - Nạp `.agents/skills/runtime-verification/SKILL.md` và gọi mode `design`.
   - Đọc `references/lifecycle-profile.md` + `catalog-index.md`, route theo runtime surface rồi chỉ mở pattern liên quan.
   - Tạo inventory authoritative đầu tiên cho feature mới và ghi vào `plan.md` section `## Runtime Risk Design` với bảng:
     `Risk ID | Status | Requirement refs | Evidence/trigger | Prevention design | Verification strategy`.
   - Mỗi risk `APPLIES` phải có prevention design đủ cụ thể để tasks không tự thiết kế lại failure semantics.
   - `NOT_APPLICABLE` phải có lý do gắn architecture/contract; không dùng "chưa implement" làm lý do.
   - `NEEDS_UPSTREAM` nghĩa là behavior/domain/contract có thẩm quyền còn thiếu: không invent trong plan.
   - Risk technical-only có thể ghi `Requirement refs = N/A — technical boundary` thay vì tạo requirement giả.
   - Plan chỉ chốt verification strategy; không giả lập runtime PASS.


4. **Thực thi workflow lập kế hoạch**: Theo cấu trúc trong template IMPL_PLAN để:
   - Điền phần Technical Context (đánh dấu các thông tin kỹ thuật chưa biết là "NEEDS CLARIFICATION")
   - Điền phần Constitution Check dựa trên constitution
   - Đánh giá các gate (ERROR nếu vi phạm không có lý do chính đáng)
   - Giai đoạn 0: Tạo research.md (giải quyết toàn bộ NEEDS CLARIFICATION ở mức technical design)
   - Giai đoạn 1: Tạo data-model.md, contracts/, quickstart.md
   - Đánh giá lại Constitution Check sau khi thiết kế và kiểm tra technical design vẫn trace được về spec và các quyết định technical đã ghi trong plan
   - Tạo **Project Docs Promotion Plan** ngắn trong `plan.md`: project-level docs nào có thể cần cập nhật **sau khi phase implementation tương ứng hoàn tất + verification pass + implementation modeling fresh**, thay đổi mental model nào dự kiến được promote, và project diagram nào cần Diagram Check. Plan MUST NOT sửa `docs/` hoặc project diagrams. Nếu không có tác động xuyên repo, ghi `None`.
   - Reconcile `Runtime Risk Design` sau research/data-model/contracts vì technical discovery có thể làm status/trigger thay đổi; mọi risk `APPLIES` phải còn trace được về requirement ref hoặc technical boundary rõ ràng.

## Hook bắt buộc sau khi thực thi

**Bạn BẮT BUỘC phải hoàn tất phần này trước khi báo cáo hoàn thành cho người dùng.**

Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu không tồn tại, hoặc không có hook nào được đăng ký trong `hooks.after_plan`, chuyển sang phần Báo cáo hoàn tất.
- Nếu có, đọc file và tìm các entry trong key `hooks.after_plan`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục sang phần Báo cáo hoàn tất.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có trường `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có trường `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để phần đánh giá điều kiện cho implementation của HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo cờ `optional`:
  - **Hook bắt buộc** (`optional: false`) — **Bạn BẮT BUỘC phải xuất `EXECUTE_COMMAND:` cho từng hook bắt buộc**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
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

Command kết thúc sau phần thiết kế của Giai đoạn 1. Báo cáo branch, đường dẫn IMPL_PLAN và các artifact đã tạo.

Không bắt buộc chạy modeling `plan` ngay tại cuối command. `$speckit-tasks` sẽ tự chạy `ensure-model(plan)` trước khi tạo tasks. Người dùng MAY gọi `$speckit-system-modeling-vi` thủ công nếu muốn xem technical model ngay sau planning.

## Các giai đoạn

### Giai đoạn 0: Lập đề cương & nghiên cứu

1. **Trích xuất các thông tin chưa biết từ Technical Context** ở trên:
   - Với mỗi NEEDS CLARIFICATION → tạo research task
   - Với mỗi dependency → tạo best practices task
   - Với mỗi integration → tạo patterns task

2. **Tạo và điều phối các research agent**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Tổng hợp kết quả** trong `research.md` theo định dạng:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Đầu ra**: research.md với toàn bộ NEEDS CLARIFICATION đã được giải quyết

### Giai đoạn 1: Thiết kế & contract

**Điều kiện tiên quyết:** `research.md` đã hoàn tất

1. **Thiết kế data model từ feature spec + technical plan** → `data-model.md`:
   - Bắt đầu từ entity/domain concept và lifecycle được `spec.md` yêu cầu; không phát minh business entity mới chỉ vì thuận tiện implementation.
   - Bổ sung field, type, persistence mapping và validation cần cho implementation dựa trên requirements.
   - State transition kỹ thuật phải nhất quán với behavior trong spec; nếu cần thay đổi business lifecycle, quay lại `spec.md` trước.

2. **Định nghĩa interface contract** (nếu dự án có interface bên ngoài) → `/contracts/`:
   - Xác định những interface mà dự án cung cấp cho người dùng hoặc hệ thống khác
   - Ghi lại contract theo định dạng phù hợp với loại dự án
   - Ví dụ: public API cho library, command schema cho CLI tool, endpoint cho web service, grammar cho parser, UI contract cho application
   - Bỏ qua nếu dự án hoàn toàn chỉ dùng nội bộ (build script, tool dùng một lần, v.v.)

3. **Tạo hướng dẫn validation quickstart** → `quickstart.md`:
   - Ghi lại các kịch bản validation có thể chạy để chứng minh feature hoạt động end-to-end
   - Bao gồm prerequisite, command thiết lập, command test/run và expected outcome
   - Dùng link hoặc reference đến contract và chi tiết data model thay vì lặp lại chúng
   - Không đưa vào toàn bộ implementation code, body của model/service/controller, migration hoặc test suite hoàn chỉnh
   - Giữ artifact này như một hướng dẫn validation/run; chi tiết implementation thuộc về `tasks.md` và giai đoạn implementation

**Đầu ra**: data-model.md, /contracts/*, quickstart.md

## Quy tắc chính

- Dùng đường dẫn tuyệt đối cho thao tác filesystem; dùng đường dẫn tương đối theo project cho reference trong tài liệu
- Constitution > `spec.md` > `plan.md`/technical design artifacts về thẩm quyền. Diagram là derived view, không nằm trong authority chain. Plan được phép bổ sung technical design nhưng không được âm thầm thay đổi requirement/business semantics của spec.
- Component/package/deployment/design class, database schema, API/interface implementation và framework/module boundaries thuộc plan; không đẩy các quyết định này ngược vào spec như thể chúng là requirement.
- Project-level docs là implemented truth hợp nhất của repo; plan chỉ xác định candidate promotion target và không copy planned feature semantics vào `docs/`.
- ERROR nếu gate thất bại hoặc vẫn còn clarification chưa được giải quyết.

## Hoàn tất khi

- [ ] Lazy Modeling Gate `spec` đã pass + fresh trước khi technical planning bắt đầu
- [ ] Workflow lập kế hoạch đã được thực thi và các artifact thiết kế đã được tạo
- [ ] Đã xác định Project Docs Promotion Plan cho project-level docs bị tác động hoặc ghi rõ `None`.
- [ ] Extension hook đã được điều phối hoặc bỏ qua theo các quy tắc trong phần Hook bắt buộc sau khi thực thi ở trên
- [ ] Đã báo cáo hoàn tất cho người dùng với branch, đường dẫn plan và các artifact đã tạo

## Optional companion skill — BẮT BUỘC khi repo cài companion

Đọc protocol tại `../companion-skills.md`.

Trước khi chốt technical design:
1. discover companion theo protocol;
2. nếu có companion phù hợp, **MUST** đọc `SKILL.md` của companion và chỉ mở reference liên quan tới stack boundary của feature;
3. đối chiếu với `runtime-verification`: generic failure dùng Risk ID canonical, companion chỉ cung cấp cách áp dụng cụ thể theo template;
4. materialize prevention design cần authority vào `plan.md`, `research.md`, `data-model.md` hoặc `contracts/` phù hợp;
5. không để companion âm thầm rewrite business semantics từ spec;
6. ghi ngắn companion nào đã dùng, guardrail nào áp dụng và artifact nào chứa quyết định.

Nếu companion phát hiện technical decision chưa có authority nhưng làm thay đổi business behavior, đánh `NEEDS_UPSTREAM` và quay lại spec/clarify thay vì tự quyết trong plan.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-plan`
- Tên gốc: `speckit-plan`
- Chính sách: `faithful`
- Commit nguồn: `566943554c617128f73e2e4864aeb713bacd0478`
