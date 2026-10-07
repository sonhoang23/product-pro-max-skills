---
name: "speckit-checklist-vi"
description: "Tạo checklist tùy chỉnh cho feature hiện tại dựa trên yêu cầu của người dùng."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/checklist.md"
---


## Mục đích của checklist: "Unit Test cho câu chữ yêu cầu"

**KHÁI NIỆM CỐT LÕI**: Checklist là **UNIT TEST CHO CÁCH VIẾT YÊU CẦU** — dùng để đánh giá chất lượng, độ rõ ràng và tính đầy đủ của yêu cầu trong một phạm vi cụ thể.

**KHÔNG dùng để xác minh/kiểm thử implementation**:

- ❌ KHÔNG phải "Xác minh nút bấm hoạt động đúng"
- ❌ KHÔNG phải "Kiểm thử xử lý lỗi có hoạt động"
- ❌ KHÔNG phải "Xác nhận API trả về 200"
- ❌ KHÔNG kiểm tra code/implementation có khớp với spec hay không

**DÙNG để đánh giá chất lượng yêu cầu**:

- ✅ "Yêu cầu về phân cấp thị giác đã được định nghĩa cho tất cả loại card chưa?" (tính đầy đủ)
- ✅ "'Hiển thị nổi bật' đã được định lượng bằng kích thước/vị trí cụ thể chưa?" (độ rõ ràng)
- ✅ "Yêu cầu về trạng thái hover có nhất quán giữa tất cả phần tử tương tác không?" (tính nhất quán)
- ✅ "Yêu cầu accessibility cho điều hướng bằng bàn phím đã được định nghĩa chưa?" (độ bao phủ)
- ✅ "Spec có định nghĩa điều gì xảy ra khi ảnh logo tải thất bại không?" (trường hợp biên)

**Ẩn dụ**: Nếu spec là code được viết bằng ngôn ngữ tự nhiên, checklist chính là bộ unit test của nó. Bạn đang kiểm tra xem yêu cầu có được viết tốt, đầy đủ, không mơ hồ và sẵn sàng để implementation hay chưa — KHÔNG phải kiểm tra implementation có hoạt động hay không.

**Quyền sở hữu và vòng đời checkbox**:

- Checklist tùy chỉnh do command này tạo ra là artifact phục vụ review chất lượng yêu cầu và thuộc quyền đánh dấu của reviewer.
- `[x]` nghĩa là reviewer xác định tiêu chí về chất lượng yêu cầu đã được đáp ứng.
- `[x]` KHÔNG có nghĩa công việc implementation đã hoàn tất.
- Command này tạo mới hoặc nối thêm các mục checklist; TUYỆT ĐỐI KHÔNG được tự đánh dấu các mục vừa tạo thành `[x]`.
- Agent chỉ được hỗ trợ đánh giá các mục khi reviewer yêu cầu rõ ràng.
- `checklists/requirements.md` là checklist chất lượng spec tích hợp sẵn, được `$speckit-specify` và `$speckit-clarify` duy trì riêng; không được áp dụng ngoại lệ đó cho các checklist tùy chỉnh được tạo ở đây.

## Đầu vào của người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi tạo checklist)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.before_checklist`.
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

    Wait for the result of the hook command before proceeding to the Execution Steps.
    ```
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong rồi mới tiếp tục sang các bước thực thi. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` hiển thị theo nghĩa đen ở trên, ví dụ agent ở skills-mode chạy bằng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không gọi hook thì chưa được xem là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, âm thầm bỏ qua.

## Các bước thực thi

1. **Thiết lập**: Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -Template checklist-template` từ thư mục gốc repo và parse JSON để lấy FEATURE_DIR, danh sách AVAILABLE_DOCS và TEMPLATE_CONTENT.
   - Tất cả đường dẫn file phải là đường dẫn tuyệt đối.
   - Với dấu nháy đơn trong tham số như `"I'm Groot"`, dùng cú pháp escape, ví dụ: `'I'\''m Groot'` (hoặc dùng dấu nháy kép nếu có thể: `"I'm Groot"`).

2. **NẾU TỒN TẠI**: Đọc `.specify/memory/constitution.md` để lấy các nguyên tắc của dự án và ràng buộc quản trị.

3. **Làm rõ ý định (động)**: Tạo tối đa BA câu hỏi làm rõ ban đầu theo ngữ cảnh (không dùng danh mục câu hỏi soạn sẵn). Các câu hỏi **BẮT BUỘC** phải:
   - Được tạo từ cách diễn đạt của người dùng + các tín hiệu trích xuất từ spec/plan/tasks.
   - Chỉ hỏi về thông tin có thể làm thay đổi đáng kể nội dung checklist.
   - Tự bỏ qua từng câu nếu `$ARGUMENTS` đã làm rõ nội dung đó.
   - Ưu tiên độ chính xác hơn độ bao quát.

   Thuật toán tạo câu hỏi:
   1. Trích xuất tín hiệu: từ khóa domain của feature (ví dụ: auth, latency, UX, API), chỉ dấu rủi ro ("critical", "must", "compliance"), gợi ý về stakeholder ("QA", "review", "security team") và deliverable được nêu rõ ("a11y", "rollback", "contracts").
   2. Gom các tín hiệu thành những vùng trọng tâm tiềm năng (tối đa 4), xếp hạng theo mức liên quan.
   3. Xác định đối tượng sử dụng và thời điểm có khả năng nhất (author, reviewer, QA, release) nếu chưa được nêu rõ.
   4. Phát hiện các chiều còn thiếu: độ rộng phạm vi, độ sâu/mức nghiêm ngặt, trọng tâm rủi ro, ranh giới loại trừ, acceptance criteria có thể đo lường.
   5. Tạo câu hỏi từ các dạng sau:
      - Thu hẹp phạm vi (ví dụ: "Checklist có cần bao gồm các điểm tích hợp với X và Y hay chỉ giới hạn ở tính đúng đắn của module cục bộ?")
      - Ưu tiên rủi ro (ví dụ: "Những vùng rủi ro tiềm năng nào cần có tiêu chí chặn bắt buộc?")
      - Hiệu chỉnh độ sâu (ví dụ: "Đây là danh sách sanity check nhẹ trước commit hay là cổng kiểm soát chính thức trước release?")
      - Xác định đối tượng dùng (ví dụ: "Checklist chỉ do author dùng hay peer cũng dùng khi review PR?")
      - Xác định phạm vi loại trừ (ví dụ: "Lần này có cần loại trừ rõ các mục tối ưu hiệu năng không?")
      - Khoảng trống về nhóm kịch bản (ví dụ: "Chưa phát hiện recovery flow — rollback / partial failure có nằm trong phạm vi không?")

   Quy tắc định dạng câu hỏi:
   - Nếu đưa ra các lựa chọn, tạo bảng gọn với các cột: Lựa chọn | Phương án | Vì sao quan trọng.
   - Tối đa các lựa chọn từ A–E; bỏ bảng nếu câu trả lời tự do rõ ràng hơn.
   - Không bao giờ yêu cầu người dùng nhắc lại điều họ đã nói.
   - Tránh suy đoán các nhóm không có căn cứ. Nếu chưa chắc, hỏi rõ: "Xác nhận xem X có nằm trong phạm vi hay không."

   Giá trị mặc định khi không thể tương tác:
   - Độ sâu: Standard
   - Đối tượng: Reviewer (PR) nếu liên quan đến code; nếu không thì Author
   - Trọng tâm: 2 cụm có mức liên quan cao nhất

   Xuất các câu hỏi với nhãn Q1/Q2/Q3. Sau khi có câu trả lời: nếu vẫn còn ≥2 nhóm kịch bản (Alternate / Exception / Recovery / Non-Functional domain) chưa rõ, bạn **CÓ THỂ** hỏi thêm tối đa HAI câu follow-up có mục tiêu cụ thể (Q4/Q5), mỗi câu kèm một dòng giải thích lý do (ví dụ: "Rủi ro ở recovery path vẫn chưa được làm rõ"). Tổng số câu hỏi không được vượt quá năm. Không hỏi thêm nếu người dùng đã nói rõ rằng họ không muốn tiếp tục làm rõ.

4. **Hiểu yêu cầu của người dùng**: Kết hợp `$ARGUMENTS` + câu trả lời làm rõ:
   - Suy ra chủ đề checklist (ví dụ: security, review, deploy, ux).
   - Tổng hợp các mục bắt buộc mà người dùng nêu rõ.
   - Ánh xạ trọng tâm đã chọn vào khung category.
   - Suy ra ngữ cảnh còn thiếu từ spec/plan/tasks (KHÔNG được bịa).

5. **Nạp ngữ cảnh feature**: Đọc từ FEATURE_DIR:
   - spec.md: Yêu cầu và phạm vi feature.
   - plan.md (nếu có): Chi tiết kỹ thuật, dependency.
   - tasks.md (nếu có): Các task implementation.

   **Chiến lược nạp ngữ cảnh**:
   - Chỉ nạp những phần cần thiết liên quan đến các vùng trọng tâm đang hoạt động (tránh đổ toàn bộ file).
   - Ưu tiên tóm tắt phần dài thành các bullet ngắn về kịch bản/yêu cầu.
   - Dùng progressive disclosure: chỉ truy xuất thêm khi phát hiện khoảng trống.
   - Nếu tài liệu nguồn lớn, tạo các mục tóm tắt trung gian thay vì nhúng nguyên văn.

5a. **Runtime-derived requirement quality context**:
   - Nếu `plan.md` có `Runtime Risk Design`, đọc các risk `APPLIES` và requirement refs của chúng.
   - Nạp `.agents/skills/runtime-verification/SKILL.md` ở mode `design` chỉ khi cần hiểu requirement implication của Risk ID liên quan; không re-scan toàn catalog.
   - Sinh checklist item để kiểm **chất lượng requirement**, không kiểm implementation; dùng trace marker `[runtime:<Risk ID>]`.
   - Ví dụ đúng: "Yêu cầu về dependent surfaces phải hội tụ sau confirmed write đã được định nghĩa chưa? [Completeness, runtime:UI-007]".
   - Ví dụ sai: "Chạy browser và xác minh invalidateQueries hoạt động".
   - Risk technical-only không cần requirement-level wording thì không ép tạo checklist item giả; Tasks/Implement chịu trách nhiệm technical gate.


6. **Tạo checklist** — dùng TEMPLATE_CONTENT làm template cấu trúc và tạo "Unit Test cho yêu cầu":
   - Tạo thư mục `FEATURE_DIR/checklists/` nếu chưa tồn tại.
   - Tạo tên file checklist duy nhất:
     - Dùng tên ngắn, mô tả đúng domain (ví dụ: `ux.md`, `api.md`, `security.md`).
     - Định dạng: `[domain].md`.
   - Cách xử lý file:
     - Nếu file CHƯA tồn tại: tạo file mới và đánh số mục bắt đầu từ CHK001.
     - Nếu file đã tồn tại: nối thêm các mục mới vào file hiện có, tiếp tục từ CHK ID cuối cùng (ví dụ, nếu mục cuối là CHK015 thì bắt đầu từ CHK016).
   - Không bao giờ xóa hoặc thay thế nội dung checklist hiện có — luôn giữ nguyên và nối thêm.
   - Mọi mục vừa tạo phải để ở trạng thái chưa đánh dấu (`[ ]`); trạng thái checkbox thuộc quyền reviewer.

   **NGUYÊN TẮC CỐT LÕI — Kiểm tra yêu cầu, không kiểm tra implementation**:
   Mỗi mục checklist **BẮT BUỘC** phải đánh giá CHÍNH CÁC YÊU CẦU theo:
   - **Tính đầy đủ**: Đã có đủ mọi yêu cầu cần thiết chưa?
   - **Độ rõ ràng**: Yêu cầu có cụ thể và không mơ hồ không?
   - **Tính nhất quán**: Các yêu cầu có thống nhất với nhau không?
   - **Khả năng đo lường**: Có thể xác minh yêu cầu một cách khách quan không?
   - **Độ bao phủ**: Đã đề cập mọi kịch bản/trường hợp biên chưa?

   **Cấu trúc category** — nhóm mục theo các chiều chất lượng của yêu cầu:
   - **Requirement Completeness** (Mọi yêu cầu cần thiết đã được ghi lại chưa?)
   - **Requirement Clarity** (Yêu cầu có cụ thể và không mơ hồ không?)
   - **Requirement Consistency** (Các yêu cầu có thống nhất và không xung đột không?)
   - **Acceptance Criteria Quality** (Tiêu chí thành công có đo lường được không?)
   - **Scenario Coverage** (Các flow/trường hợp đã được bao phủ hết chưa?)
   - **Edge Case Coverage** (Các điều kiện biên đã được định nghĩa chưa?)
   - **Non-Functional Requirements** (Performance, Security, Accessibility, v.v. — đã được quy định chưa?)
   - **Dependencies & Assumptions** (Dependency và assumption đã được ghi lại và xác thực chưa?)
   - **Ambiguities & Conflicts** (Điểm nào cần làm rõ?)

   **CÁCH VIẾT MỤC CHECKLIST — "Unit Test cho câu chữ yêu cầu"**:

   ❌ **SAI** (kiểm tra implementation):
   - "Xác minh landing page hiển thị 3 episode card"
   - "Kiểm thử trạng thái hover hoạt động trên desktop"
   - "Xác nhận click vào logo sẽ điều hướng về trang chủ"

   ✅ **ĐÚNG** (kiểm tra chất lượng yêu cầu):
   - "Số lượng và layout chính xác của featured episode đã được quy định chưa?" [Completeness]
   - "'Hiển thị nổi bật' đã được định lượng bằng kích thước/vị trí cụ thể chưa?" [Clarity]
   - "Yêu cầu về trạng thái hover có nhất quán giữa tất cả phần tử tương tác không?" [Consistency]
   - "Yêu cầu điều hướng bằng bàn phím đã được định nghĩa cho tất cả UI tương tác chưa?" [Coverage]
   - "Hành vi fallback khi ảnh logo tải thất bại đã được quy định chưa?" [Edge Cases]
   - "Trạng thái loading cho dữ liệu episode bất đồng bộ đã được định nghĩa chưa?" [Completeness]
   - "Spec có định nghĩa phân cấp thị giác giữa các UI element cạnh tranh sự chú ý không?" [Clarity]

   **CẤU TRÚC MỖI MỤC**:
   Mỗi mục nên theo mẫu:
   - Dạng câu hỏi về chất lượng yêu cầu.
   - Tập trung vào điều ĐƯỢC VIẾT (hoặc chưa được viết) trong spec/plan.
   - Kèm chiều chất lượng trong ngoặc vuông `[Completeness/Clarity/Consistency/etc.]`.
   - Tham chiếu section của spec bằng `[Spec §X.Y]` khi kiểm tra yêu cầu hiện có.
   - Dùng marker `[Gap]` khi kiểm tra yêu cầu còn thiếu.

   **VÍ DỤ THEO CHIỀU CHẤT LƯỢNG**:

   Completeness:
   - "Yêu cầu xử lý lỗi đã được định nghĩa cho mọi failure mode của API chưa? [Gap]"
   - "Yêu cầu accessibility đã được quy định cho tất cả phần tử tương tác chưa? [Completeness]"
   - "Yêu cầu breakpoint trên mobile đã được định nghĩa cho responsive layout chưa? [Gap]"

   Clarity:
   - "'Tải nhanh' đã được định lượng bằng ngưỡng thời gian cụ thể chưa? [Clarity, Spec §NFR-2]"
   - "Tiêu chí chọn 'episode liên quan' đã được định nghĩa rõ ràng chưa? [Clarity, Spec §FR-5]"
   - "'Nổi bật' đã được định nghĩa bằng thuộc tính thị giác có thể đo lường chưa? [Ambiguity, Spec §FR-4]"

   Consistency:
   - "Yêu cầu điều hướng có thống nhất trên mọi trang không? [Consistency, Spec §FR-10]"
   - "Yêu cầu đối với card component có nhất quán giữa landing page và detail page không? [Consistency]"

   Coverage:
   - "Yêu cầu cho kịch bản zero-state (không có episode) đã được định nghĩa chưa? [Coverage, Edge Case]"
   - "Các kịch bản người dùng tương tác đồng thời đã được đề cập chưa? [Coverage, Gap]"
   - "Yêu cầu cho trường hợp tải dữ liệu một phần bị lỗi đã được quy định chưa? [Coverage, Exception Flow]"

   Measurability:
   - "Yêu cầu về phân cấp thị giác có thể đo lường/kiểm chứng được không? [Acceptance Criteria, Spec §FR-1]"
   - "'Cân bằng trọng lượng thị giác' có thể được xác minh khách quan không? [Measurability, Spec §FR-2]"

   **Phân loại và bao phủ kịch bản** (tập trung vào chất lượng yêu cầu):
   - Kiểm tra xem yêu cầu có tồn tại cho các nhóm: Primary, Alternate, Exception/Error, Recovery, Non-Functional.
   - Với mỗi nhóm kịch bản, hỏi: "Yêu cầu cho [loại kịch bản] có đầy đủ, rõ ràng và nhất quán không?"
   - Nếu thiếu một nhóm kịch bản: "Yêu cầu cho [loại kịch bản] được chủ đích loại khỏi phạm vi hay đang bị thiếu? [Gap]"
   - Bao gồm resilience/rollback khi có thay đổi trạng thái: "Yêu cầu rollback khi migration thất bại đã được định nghĩa chưa? [Gap]"

   **Yêu cầu về traceability**:
   - TỐI THIỂU: ≥80% số mục **BẮT BUỘC** phải có ít nhất một tham chiếu traceability.
   - Mỗi mục nên tham chiếu: section của spec `[Spec §X.Y]`, hoặc dùng marker: `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`.
   - Nếu chưa có hệ thống ID: "Đã thiết lập quy ước ID cho requirement và acceptance criteria chưa? [Traceability]"

   **Làm lộ diện và xử lý vấn đề** (các vấn đề về chất lượng yêu cầu):
   Đặt câu hỏi về chính yêu cầu:
   - Mơ hồ: "Từ 'nhanh' đã được định lượng bằng metric cụ thể chưa? [Ambiguity, Spec §NFR-1]"
   - Xung đột: "Yêu cầu điều hướng giữa §FR-10 và §FR-10a có xung đột không? [Conflict]"
   - Giả định: "Giả định 'podcast API luôn sẵn sàng' đã được xác thực chưa? [Assumption]"
   - Dependency: "Yêu cầu đối với podcast API bên ngoài đã được ghi lại chưa? [Dependency, Gap]"
   - Thiếu định nghĩa: "'Phân cấp thị giác' đã được định nghĩa bằng tiêu chí có thể đo lường chưa? [Gap]"

   **Hợp nhất nội dung**:
   - Giới hạn mềm: nếu số mục ứng viên thô > 40, ưu tiên theo rủi ro/tác động.
   - Gộp các mục gần như trùng nhau khi chúng kiểm tra cùng một khía cạnh của yêu cầu.
   - Nếu có >5 trường hợp biên tác động thấp, tạo một mục: "Các trường hợp biên X, Y, Z đã được đề cập trong yêu cầu chưa? [Coverage]"

   **🚫 TUYỆT ĐỐI CẤM** — Các dạng sau biến checklist thành bài kiểm thử implementation thay vì kiểm tra yêu cầu:
   - ❌ Bất kỳ mục nào bắt đầu bằng "Xác minh", "Kiểm thử", "Xác nhận", "Kiểm tra" + hành vi implementation.
   - ❌ Tham chiếu đến việc chạy code, thao tác người dùng hoặc hành vi hệ thống.
   - ❌ "Hiển thị đúng", "hoạt động đúng", "chạy như mong đợi".
   - ❌ "Click/nhấp", "navigate/điều hướng", "render", "load/tải", "execute/thực thi".
   - ❌ Test case, test plan, quy trình QA.
   - ❌ Chi tiết implementation (framework, API, algorithm).

   **✅ MẪU BẮT BUỘC** — Các dạng này kiểm tra chất lượng yêu cầu:
   - ✅ "[Loại yêu cầu] đã được định nghĩa/quy định/ghi lại cho [kịch bản] chưa?"
   - ✅ "[Thuật ngữ mơ hồ] đã được định lượng/làm rõ bằng tiêu chí cụ thể chưa?"
   - ✅ "Yêu cầu giữa [section A] và [section B] có nhất quán không?"
   - ✅ "[Yêu cầu] có thể được đo/xác minh khách quan không?"
   - ✅ "[Trường hợp biên/kịch bản] đã được đề cập trong yêu cầu chưa?"
   - ✅ "Spec có định nghĩa [khía cạnh còn thiếu] không?"

7. **Tham chiếu cấu trúc**: Tạo checklist theo template chuẩn trong `.specify/templates/checklist-template.md` về title, meta section, category heading, ownership note, notes section và định dạng ID. Nếu template không khả dụng, dùng: H1 title, các dòng meta về purpose/created, một ownership note giải thích rằng `[x]` nghĩa là reviewer chấp thuận chất lượng yêu cầu, các section `##` chứa dòng `- [ ] CHK### <requirement item>` với ID tăng toàn cục từ CHK001, và phần notes ghi rõ `$speckit-implement` đọc trạng thái checklist nhưng không sửa marker.

8. **Báo cáo**: Xuất đường dẫn đầy đủ đến file checklist, số lượng mục và tóm tắt lần chạy này đã tạo file mới hay nối thêm vào file có sẵn. Tóm tắt:
   - Các vùng trọng tâm đã chọn.
   - Mức độ sâu.
   - Actor/thời điểm.
   - Các mục bắt buộc do người dùng nêu rõ đã được đưa vào.

**Quan trọng**: Mỗi lần gọi command `$speckit-checklist` dùng một tên file checklist ngắn, dễ mô tả và sẽ tạo file mới hoặc nối thêm vào file đã tồn tại. Nhờ đó có thể:

- Có nhiều checklist thuộc các loại khác nhau (ví dụ: `ux.md`, `test.md`, `security.md`).
- Dùng tên file đơn giản, dễ nhớ và thể hiện mục đích checklist.
- Dễ nhận biết và điều hướng trong thư mục `checklists/`.

Để tránh lộn xộn, dùng các loại mô tả rõ và dọn những checklist đã lỗi thời khi không còn cần.

## Ví dụ về loại checklist và mục mẫu

**Chất lượng yêu cầu UX:** `ux.md`

Các mục mẫu (kiểm tra yêu cầu, KHÔNG kiểm tra implementation):

- "Yêu cầu về phân cấp thị giác đã được định nghĩa bằng tiêu chí có thể đo lường chưa? [Clarity, Spec §FR-1]"
- "Số lượng và vị trí của các UI element đã được quy định rõ chưa? [Completeness, Spec §FR-1]"
- "Yêu cầu về trạng thái tương tác (hover, focus, active) có được định nghĩa nhất quán không? [Consistency]"
- "Yêu cầu accessibility đã được quy định cho tất cả phần tử tương tác chưa? [Coverage, Gap]"
- "Hành vi fallback khi ảnh tải thất bại đã được định nghĩa chưa? [Edge Case, Gap]"
- "'Hiển thị nổi bật' có thể được đo lường khách quan không? [Measurability, Spec §FR-4]"

**Chất lượng yêu cầu API:** `api.md`

Các mục mẫu:

- "Định dạng error response đã được quy định cho mọi kịch bản thất bại chưa? [Completeness]"
- "Yêu cầu rate limiting đã được định lượng bằng ngưỡng cụ thể chưa? [Clarity]"
- "Yêu cầu authentication có nhất quán trên tất cả endpoint không? [Consistency]"
- "Yêu cầu retry/timeout cho dependency bên ngoài đã được định nghĩa chưa? [Coverage, Gap]"
- "Chiến lược versioning đã được ghi lại trong yêu cầu chưa? [Gap]"

**Chất lượng yêu cầu Performance:** `performance.md`

Các mục mẫu:

- "Yêu cầu performance đã được định lượng bằng metric cụ thể chưa? [Clarity]"
- "Mục tiêu performance đã được định nghĩa cho tất cả critical user journey chưa? [Coverage]"
- "Yêu cầu performance dưới các điều kiện tải khác nhau đã được quy định chưa? [Completeness]"
- "Yêu cầu performance có thể được đo lường khách quan không? [Measurability]"
- "Yêu cầu degradation trong kịch bản tải cao đã được định nghĩa chưa? [Edge Case, Gap]"

**Chất lượng yêu cầu Security:** `security.md`

Các mục mẫu:

- "Yêu cầu authentication đã được quy định cho tất cả protected resource chưa? [Coverage]"
- "Yêu cầu bảo vệ dữ liệu đã được định nghĩa cho thông tin nhạy cảm chưa? [Completeness]"
- "Threat model đã được ghi lại và các yêu cầu đã được căn chỉnh theo đó chưa? [Traceability]"
- "Yêu cầu security có nhất quán với các nghĩa vụ compliance không? [Consistency]"
- "Yêu cầu ứng phó khi security failure/breach đã được định nghĩa chưa? [Gap, Exception Flow]"

## Phản ví dụ: Những điều KHÔNG được làm

**❌ SAI — Các mục này kiểm tra implementation, không phải yêu cầu:**

```markdown
- [ ] CHK001 - Xác minh landing page hiển thị 3 episode card [Spec §FR-001]
- [ ] CHK002 - Kiểm thử trạng thái hover hoạt động đúng trên desktop [Spec §FR-003]
- [ ] CHK003 - Xác nhận click logo sẽ điều hướng về home page [Spec §FR-010]
- [ ] CHK004 - Kiểm tra section related episodes hiển thị 3-5 mục [Spec §FR-005]
```

**✅ ĐÚNG — Các mục này kiểm tra chất lượng yêu cầu:**

```markdown
- [ ] CHK001 - Số lượng và layout của featured episode đã được quy định rõ chưa? [Completeness, Spec §FR-001]
- [ ] CHK002 - Yêu cầu về trạng thái hover có được định nghĩa nhất quán cho tất cả phần tử tương tác không? [Consistency, Spec §FR-003]
- [ ] CHK003 - Yêu cầu điều hướng có rõ ràng cho tất cả brand element có thể nhấp không? [Clarity, Spec §FR-010]
- [ ] CHK004 - Tiêu chí chọn related episode đã được ghi lại chưa? [Gap, Spec §FR-005]
- [ ] CHK005 - Yêu cầu về loading state cho dữ liệu episode bất đồng bộ đã được định nghĩa chưa? [Gap]
- [ ] CHK006 - Yêu cầu về "phân cấp thị giác" có thể được đo lường khách quan không? [Measurability, Spec §FR-001]
```

**Khác biệt chính:**

- Sai: Kiểm tra hệ thống có hoạt động đúng không.
- Đúng: Kiểm tra yêu cầu có được viết đúng không.
- Sai: Xác minh hành vi.
- Đúng: Đánh giá chất lượng yêu cầu.
- Sai: "Hệ thống có làm X không?"
- Đúng: "X đã được quy định rõ chưa?"

## Kiểm tra sau khi thực thi

**Kiểm tra extension hook (sau khi tạo checklist)**:
Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.after_checklist`.
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

Checklist vẫn là **unit test cho câu chữ requirement**, không phải checklist implementation.

- Không biến rule của companion thành các mục kiểu “chạy typecheck”, “API trả 200”, “Playwright pass”.
- MAY dùng companion để kiểm xem requirement/acceptance consequence đã materialize có được viết rõ, đầy đủ, không mâu thuẫn hay không.
- Technical prevention/evidence của companion thuộc plan/tasks/implementation, không thuộc checklist requirement trừ khi user-visible behavior cần được đặc tả.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-checklist`
- Tên gốc: `speckit-checklist`
- Chính sách: `faithful`
- Commit nguồn: `390659c4ee776dfaca1eb1049862652611f962d2`
