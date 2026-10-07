---
name: "speckit-specify-vi"
description: "Tạo hoặc cập nhật đặc tả tính năng từ mô tả tính năng bằng ngôn ngữ tự nhiên."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/specify.md"
---


## Đầu vào người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi tạo đặc tả)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.before_specify`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có trường `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có trường `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để phần đánh giá điều kiện cho implementation của HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo cờ `optional`:
  - **Hook trước tùy chọn** (`optional: true`):
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục đến phần Phác thảo. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Phác thảo

Phần văn bản người dùng nhập sau `$speckit-specify` trong message kích hoạt **chính là** mô tả tính năng. Giả định bạn luôn có nội dung đó trong cuộc hội thoại này, ngay cả khi `$ARGUMENTS` xuất hiện nguyên văn ở bên dưới. Không yêu cầu người dùng nhập lại trừ khi họ gọi command mà không cung cấp nội dung.

Với mô tả tính năng đó, thực hiện như sau:

1. **Tạo một tên ngắn gọn** (2-4 từ) cho tính năng:
   - Phân tích mô tả tính năng và trích ra các từ khóa có ý nghĩa nhất.
   - Tạo tên ngắn 2-4 từ thể hiện đúng bản chất của tính năng.
   - Ưu tiên dạng động-từ + danh-từ khi phù hợp (ví dụ: "add-user-auth", "fix-payment-bug").
   - Giữ nguyên thuật ngữ kỹ thuật và từ viết tắt (OAuth2, API, JWT, v.v.).
   - Giữ tên ngắn gọn nhưng đủ mô tả để nhìn qua là hiểu tính năng.
   - Ví dụ:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **Tạo branch** (tùy chọn, qua hook):

   Nếu một hook `before_specify` đã chạy thành công trong phần Kiểm tra trước khi thực thi ở trên, hook đó sẽ tạo/chuyển sang một git branch và xuất JSON chứa `BRANCH_NAME` cùng `FEATURE_NUM`. Ghi nhận các giá trị này để tham chiếu, nhưng tên branch **không** quyết định tên thư mục spec.

   Nếu người dùng cung cấp rõ `GIT_BRANCH_NAME`, truyền nguyên giá trị đó cho hook để script tạo branch dùng đúng giá trị này làm tên branch (bỏ qua toàn bộ quá trình sinh prefix/suffix).

3. **Tạo thư mục spec cho tính năng**:

   Theo mặc định, spec nằm trong thư mục `specs/`, trừ khi người dùng cung cấp rõ `SPECIFY_FEATURE_DIRECTORY`.

   **Thứ tự phân giải `SPECIFY_FEATURE_DIRECTORY`**:
   1. Nếu người dùng cung cấp rõ `SPECIFY_FEATURE_DIRECTORY` (ví dụ qua biến môi trường, argument hoặc configuration), dùng nguyên giá trị đó.
   2. Nếu không, tự tạo bên trong `specs/`:
      - Kiểm tra `.specify/init-options.json` để lấy `feature_numbering` (ưu tiên) hoặc `branch_numbering` (đã deprecated, chỉ dùng để migration — sẽ bị loại bỏ trong một bản phát hành tương lai).
      - Nếu `"timestamp"`: prefix là `YYYYMMDD-HHMMSS` (timestamp hiện tại).
      - Nếu `"sequential"` hoặc không có: prefix là `NNN` (số 3 chữ số khả dụng tiếp theo sau khi quét các thư mục hiện có trong `specs/`).
      - Tạo tên thư mục: `<prefix>-<short-name>` (ví dụ: `003-user-auth` hoặc `20260319-143022-user-auth`).
      - Đặt `SPECIFY_FEATURE_DIRECTORY` thành `specs/<directory-name>`.
      - Nếu dùng `branch_numbering` (và không có `feature_numbering`), xuất cảnh báo một dòng: "⚠️ `branch_numbering` in init-options.json is deprecated. Rename to `feature_numbering`."

   **Tạo thư mục và file spec**:
   - `mkdir -p SPECIFY_FEATURE_DIRECTORY`
   - Phân giải `spec-template` đang hoạt động thông qua stack phân giải preset/template của Spec Kit (tương đương `specify preset resolve spec-template`).
   - Copy file `spec-template` đã phân giải sang `SPECIFY_FEATURE_DIRECTORY/spec.md` làm điểm khởi đầu.
   - Đặt `SPEC_FILE` thành `SPECIFY_FEATURE_DIRECTORY/spec.md`.
   - Lưu đường dẫn đã phân giải vào `.specify/feature.json`:
     ```json
     {
       "feature_directory": "<resolved feature dir>"
     }
     ```
     Ghi giá trị đường dẫn thư mục đã phân giải thực tế (ví dụ `specs/003-user-auth`), không ghi chuỗi literal `SPECIFY_FEATURE_DIRECTORY`.
     Việc này giúp các command phía sau (`$speckit-clarify`, `$speckit-system-modeling-vi`, `$speckit-plan`, `$speckit-tasks`, v.v.) tìm được thư mục tính năng mà không phụ thuộc vào quy ước tên git branch.

   **QUAN TRỌNG**:
   - Mỗi lần gọi `$speckit-specify` chỉ được tạo đúng một tính năng.
   - Tên thư mục spec và tên git branch độc lập với nhau — chúng có thể giống nhau, nhưng đó là lựa chọn của người dùng.
   - Thư mục spec và file spec luôn được command này tạo, không phải do hook tạo.

4. Nạp file `spec-template` đang hoạt động đã được phân giải để hiểu các section bắt buộc.

5. **NẾU TỒN TẠI**: Nạp `.specify/memory/constitution.md` để lấy các nguyên tắc dự án và ràng buộc quản trị.

5a. **Project Docs Impact Check**:
   - Chỉ đọc các project-level docs có khả năng liên quan trong `docs/` (ví dụ system context, architecture, flow, domain, security, API convention); không quét hoặc copy toàn bộ `docs/` nếu feature thuần cục bộ.
   - Xác định feature có làm thay đổi mental model dùng chung như actor, system surface/boundary, flow lớn, domain/lifecycle, permission/ownership, architecture/security hoặc convention xuyên repo hay không.
   - Nếu có, ghi trong `spec.md` một mục ngắn **Project Docs Impact** liệt kê đường dẫn project-level docs có khả năng phải được **promote/cập nhật sau implementation**. Đây chỉ là impact metadata của planned change, không phải technical implementation detail và không cho phép sửa `docs/` ở bước specify.
   - Nếu không có tác động xuyên repo, ghi `Project Docs Impact: None` hoặc bỏ mục này khi template/project convention cho phép.
   - Project-level docs phản ánh implemented truth hiện tại và không được dùng để ghi đè requirement của feature; nếu feature đang đề xuất trạng thái tương lai khác `docs/`, xem đó là planned change bình thường. Chỉ coi project docs stale khi capability tương ứng đã implement + verify nhưng chưa được promote.


5b. **Runtime Requirement Signal Check — BẮT BUỘC, phase-aware**:
   - Nếu tồn tại `.agents/skills/runtime-verification/SKILL.md`, gọi mode `requirements`.
   - Đọc `references/lifecycle-profile.md` trước, sau đó chỉ mở category/pattern có `Earliest detectable stage = requirements` và surface thực sự xuất hiện; không quét toàn catalog.
   - Với signal `SIGNAL`, chuyển lesson thành requirement/acceptance/edge-case **technology-agnostic** và giữ requirement ref để plan trace lại.
   - Với `DEFERRED`, không kéo technical detail xuống spec; để `speckit-plan-vi` xử lý.
   - Với `NEEDS_UPSTREAM` chỉ hỏi/làm rõ khi thiếu quyết định behavior/domain/user-visible có thẩm quyền. Technical choice thuần túy không được biến thành câu hỏi specify.
   - Runtime signal là prevention hint, không phải source requirement độc lập.


6. Thực hiện flow sau:
    1. Parse mô tả của người dùng từ arguments.
       Nếu rỗng: ERROR "No feature description provided"
    2. Trích xuất các khái niệm chính từ mô tả.
       Xác định: actor, action, data, constraint.
    3. Với các khía cạnh chưa rõ:
       - Đưa ra suy đoán có cơ sở dựa trên ngữ cảnh và tiêu chuẩn ngành.
       - Chỉ đánh dấu bằng [NEEDS CLARIFICATION: specific question] nếu:
         - Lựa chọn ảnh hưởng đáng kể đến phạm vi tính năng hoặc trải nghiệm người dùng.
         - Có nhiều cách hiểu hợp lý với hệ quả khác nhau.
         - Không có giá trị mặc định hợp lý.
       - **GIỚI HẠN: Tối đa 3 marker [NEEDS CLARIFICATION] tổng cộng**.
       - Ưu tiên nội dung cần làm rõ theo mức tác động: phạm vi > security/privacy > trải nghiệm người dùng > chi tiết kỹ thuật.
    4. Điền section User Scenarios & Testing.
       Nếu không xác định được user flow rõ ràng: ERROR "Cannot determine user scenarios"
    5. Tạo Functional Requirements.
       Mỗi requirement phải có thể kiểm thử.
       Dùng các giá trị mặc định hợp lý cho chi tiết chưa được nêu (ghi lại các assumption trong section Assumptions).
    6. Xác định Success Criteria.
       Tạo các outcome có thể đo lường và không phụ thuộc công nghệ.
       Bao gồm cả metric định lượng (thời gian, performance, volume) và đánh giá định tính (mức hài lòng của người dùng, mức hoàn thành task).
       Mỗi tiêu chí phải có thể xác minh mà không cần chi tiết implementation.
    7. Xác định Key Entities (nếu có dữ liệu liên quan).
    8. Trả về: SUCCESS (spec ready for clarification)

7. Ghi đặc tả vào SPEC_FILE theo cấu trúc template, thay placeholder bằng chi tiết cụ thể suy ra từ mô tả tính năng (arguments), đồng thời giữ nguyên thứ tự và heading của các section.

8. **Xác thực chất lượng đặc tả**: Sau khi ghi bản spec đầu tiên, xác thực theo các tiêu chí chất lượng:

   a. **Tạo checklist chất lượng spec**: Tạo file checklist tại `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` theo cấu trúc template checklist với các mục xác thực sau:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]

      **Purpose**: Validate specification completeness and quality before clarification and system modeling
      **Created**: [DATE]
      **Feature**: [Link to spec.md]

      ## Content Quality

      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed

      ## Requirement Completeness

      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified
      - [ ] Project-level documentation impact is identified when the feature changes shared mental models
      - [ ] Known runtime-failure signals detectable at requirement stage are reflected as technology-agnostic behavior/acceptance/edge-case requirements or explicitly deferred

      ## Feature Readiness

      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification

      ## Notes

      - Items marked incomplete require spec updates before `$speckit-clarify`; sau khi spec/clarify hoàn tất có thể gọi thẳng `$speckit-plan`, command này tự chạy Lazy Modeling Gate `spec` trước technical planning
      ```

   b. **Chạy bước xác thực**: Rà soát spec theo từng mục checklist:
      - Với mỗi mục, xác định pass hay fail.
      - Ghi lại vấn đề cụ thể đã phát hiện (trích dẫn section liên quan của spec).

   c. **Xử lý kết quả xác thực**:

      - **Nếu tất cả mục đều pass**: Đánh dấu checklist hoàn tất và chuyển sang phần Hook bắt buộc sau khi thực thi.

      - **Nếu có mục fail (không tính [NEEDS CLARIFICATION])**:
        1. Liệt kê các mục fail và vấn đề cụ thể.
        2. Cập nhật spec để xử lý từng vấn đề.
        3. Chạy lại xác thực cho đến khi tất cả mục đều pass (tối đa 3 vòng).
        4. Nếu vẫn còn fail sau 3 vòng, ghi các vấn đề còn lại vào phần notes của checklist và cảnh báo người dùng.

      - **Nếu vẫn còn marker [NEEDS CLARIFICATION]**:
        1. Trích xuất tất cả marker [NEEDS CLARIFICATION: ...] từ spec.
        2. **KIỂM TRA GIỚI HẠN**: Nếu có nhiều hơn 3 marker, chỉ giữ lại 3 marker quan trọng nhất (theo tác động phạm vi/security/UX) và đưa ra suy đoán có cơ sở cho phần còn lại.
        3. Với mỗi nội dung cần làm rõ (tối đa 3), trình bày các lựa chọn cho người dùng theo định dạng sau:

           ```markdown
           ## Question [N]: [Topic]

           **Context**: [Quote relevant spec section]

           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]

           **Suggested Answers**:

           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |

           **Your choice**: _[Wait for user response]_
           ```

        4. **QUAN TRỌNG - Định dạng bảng**: Đảm bảo bảng Markdown được định dạng đúng:
           - Dùng khoảng trắng nhất quán và căn các dấu pipe.
           - Mỗi cell phải có khoảng trắng quanh nội dung: `| Content |`, không phải `|Content|`.
           - Dòng phân cách header phải có ít nhất 3 dấu gạch ngang: `|--------|`.
           - Kiểm tra bảng render đúng trong Markdown preview.
        5. Đánh số câu hỏi tuần tự (Q1, Q2, Q3 - tối đa 3 câu tổng cộng).
        6. Trình bày toàn bộ câu hỏi cùng lúc trước khi chờ phản hồi.
        7. Chờ người dùng trả lời lựa chọn cho tất cả câu hỏi (ví dụ: "Q1: A, Q2: Custom - [details], Q3: B").
        8. Cập nhật spec bằng cách thay từng marker [NEEDS CLARIFICATION] bằng câu trả lời người dùng đã chọn hoặc cung cấp.
        9. Chạy lại xác thực sau khi tất cả nội dung cần làm rõ đã được giải quyết.

   d. **Cập nhật checklist**: Sau mỗi vòng xác thực, cập nhật file checklist với trạng thái pass/fail hiện tại.

## Hook bắt buộc sau khi thực thi

**Bạn BẮT BUỘC phải hoàn tất phần này trước khi báo cáo hoàn thành cho người dùng.**

Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu không tồn tại, hoặc không có hook nào được đăng ký trong `hooks.after_specify`, chuyển sang phần Báo cáo hoàn thành.
- Nếu có, đọc file và tìm các entry trong key `hooks.after_specify`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không có hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục đến phần Báo cáo hoàn thành.
- Loại các hook có `enabled` được đặt rõ ràng thành `false`. Hook không có trường `enabled` mặc định được xem là đã bật.
- Với mỗi hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có trường `condition`, hoặc giá trị là null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để phần đánh giá điều kiện cho implementation của HookExecutor.
- Khi tạo command invocation từ tên hook command, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau tùy theo cờ `optional`:
  - **Hook bắt buộc** (`optional: false`) — **BẮT BUỘC phải xuất `EXECUTE_COMMAND:` cho từng hook bắt buộc**:
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

## Báo cáo hoàn thành

Báo cáo kết quả cho người dùng với:
- `SPECIFY_FEATURE_DIRECTORY` — đường dẫn thư mục tính năng.
- `SPEC_FILE` — đường dẫn file spec.
- Tóm tắt kết quả checklist.
- Mức độ sẵn sàng cho giai đoạn tiếp theo (`$speckit-clarify` khi cần; sau đó có thể gọi thẳng `$speckit-plan`, command này tự bảo đảm modeling gate `spec`).

**LƯU Ý:** Việc tạo branch do hook `before_specify` (git extension) xử lý. Việc tạo thư mục spec và file spec luôn do core command này xử lý.

## Hướng dẫn nhanh

- Tập trung vào **WHAT** người dùng cần và **WHY**.
- Tránh HOW để implementation (không tech stack, API, cấu trúc code).
- Viết cho stakeholder nghiệp vụ, không phải developer.
- KHÔNG tạo checklist nhúng bên trong spec. Đây là nhiệm vụ của một command riêng.

### Yêu cầu đối với section

- **Section bắt buộc**: Phải hoàn thành cho mọi tính năng.
- **Section tùy chọn**: Chỉ đưa vào khi phù hợp với tính năng.
- Khi một section không áp dụng, xóa hoàn toàn section đó (không để "N/A").

### Dành cho AI tạo sinh

Khi tạo spec này từ prompt của người dùng:

1. **Đưa ra suy đoán có cơ sở**: Dùng ngữ cảnh, tiêu chuẩn ngành và pattern phổ biến để lấp khoảng trống.
2. **Ghi lại assumption**: Ghi các giá trị mặc định hợp lý trong section Assumptions.
3. **Giới hạn nội dung cần làm rõ**: Tối đa 3 marker [NEEDS CLARIFICATION] - chỉ dùng cho quyết định quan trọng:
   - Ảnh hưởng đáng kể đến phạm vi tính năng hoặc trải nghiệm người dùng.
   - Có nhiều cách hiểu hợp lý với hệ quả khác nhau.
   - Không có giá trị mặc định hợp lý.
4. **Ưu tiên nội dung cần làm rõ**: phạm vi > security/privacy > trải nghiệm người dùng > chi tiết kỹ thuật.
5. **Suy nghĩ như tester**: Mọi requirement mơ hồ phải fail mục checklist "testable and unambiguous".
6. **Các vùng thường cần làm rõ** (chỉ khi không có giá trị mặc định hợp lý):
   - Phạm vi và ranh giới tính năng (bao gồm/loại trừ các use case cụ thể).
   - Loại người dùng và quyền hạn (nếu có nhiều cách hiểu mâu thuẫn).
   - Yêu cầu security/compliance (khi có ý nghĩa đáng kể về pháp lý/tài chính).

**Ví dụ về giá trị mặc định hợp lý** (không hỏi về các mục này):

- Data retention: Thực hành tiêu chuẩn của ngành cho domain.
- Performance target: Kỳ vọng tiêu chuẩn đối với ứng dụng web/mobile, trừ khi có yêu cầu khác.
- Error handling: Message thân thiện với người dùng kèm fallback phù hợp.
- Authentication method: Session-based hoặc OAuth2 tiêu chuẩn cho ứng dụng web.
- Integration pattern: Dùng pattern phù hợp với dự án (REST/GraphQL cho web service, function call cho library, CLI arg cho tool, v.v.).

### Hướng dẫn Success Criteria

Success criteria phải:

1. **Có thể đo lường**: Bao gồm metric cụ thể (thời gian, phần trăm, số lượng, tỷ lệ).
2. **Không phụ thuộc công nghệ**: Không nhắc đến framework, ngôn ngữ, database hoặc tool.
3. **Tập trung vào người dùng**: Mô tả outcome từ góc nhìn người dùng/doanh nghiệp, không phải nội bộ hệ thống.
4. **Có thể xác minh**: Có thể kiểm thử/xác thực mà không cần biết chi tiết implementation.

**Ví dụ tốt**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Ví dụ không tốt** (tập trung vào implementation):

- "API response time is under 200ms" (quá kỹ thuật, hãy dùng "Users see results instantly")
- "Database can handle 1000 TPS" (chi tiết implementation, hãy dùng metric hướng tới người dùng)
- "React components render efficiently" (phụ thuộc framework)
- "Redis cache hit rate above 80%" (phụ thuộc công nghệ)

## Hoàn tất khi

- [ ] Đặc tả đã được ghi vào `SPEC_FILE` và được xác thực theo quality checklist.
- [ ] Đã chạy Project Docs Impact Check và ghi nhận project-level docs bị tác động khi cần.
- [ ] Extension hook đã được dispatch hoặc bỏ qua theo quy tắc trong phần Hook bắt buộc sau khi thực thi ở trên.
- [ ] Đã báo cáo hoàn thành cho người dùng với thư mục tính năng, đường dẫn file spec và kết quả checklist.

## Optional companion skill

Đọc protocol tại `../companion-skills.md`.

Ở stage specify:
- companion kỹ thuật không phải source requirement;
- không kéo framework/library/command/generated-artifact mechanics vào `spec.md`;
- nếu companion làm lộ một consequence user/domain-visible đã được mô tả hoặc có authority từ input, materialize consequence đó theo ngôn ngữ technology-agnostic;
- technical prevention còn lại phải `DEFERRED` sang plan;
- nếu repo không có companion, workflow không thay đổi.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-specify`
- Tên gốc: `speckit-specify`
- Chính sách: `faithful`
- Commit nguồn: `9420e2f3e493179ef9b31d9644965a83771a0c92`