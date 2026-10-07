---
name: "speckit-clarify-vi"
description: "Xác định các phần chưa được đặc tả đầy đủ trong feature spec hiện tại bằng cách đặt tối đa 5 câu hỏi làm rõ có mục tiêu cao, sau đó ghi câu trả lời trở lại vào spec."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/clarify.md"
---


## Đầu vào người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi làm rõ)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của project hay không.
- Nếu có, đọc file và tìm các entry dưới key `hooks.before_clarify`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: hãy báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục bình thường.
- Loại các hook có `enabled` được đặt rõ ràng là `false`. Với hook không có field `enabled`, mặc định coi là đã bật.
- Với mỗi hook còn lại, **không** tự diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook và để việc đánh giá condition cho implementation của HookExecutor.
- Khi dựng lệnh gọi từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
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

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    Sau khi phát block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách gọi thực tế có thể khác với id `{command}` hiển thị ở trên; ví dụ agent chạy ở skills mode có thể gọi dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ phát block mà không gọi hook thì chưa được tính là đã chạy hook.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua âm thầm.

## Quy trình

Mục tiêu: Phát hiện và giảm sự mơ hồ hoặc các điểm quyết định còn thiếu trong feature specification đang hoạt động, đồng thời ghi trực tiếp các nội dung làm rõ vào file spec.

Lưu ý: Workflow làm rõ này được kỳ vọng hoàn tất trước technical planning. Người dùng **không cần** gọi `$speckit-system-modeling-vi` thủ công sau clarify; khi `$speckit-plan` bắt đầu, plan tự chạy Lazy Modeling Gate `spec` và chỉ invoke modeling nếu gate thiếu hoặc stale. Nếu người dùng bỏ qua clarify (ví dụ exploratory spike), planning vẫn có thể tiếp tục nhưng rủi ro phải sửa spec/modeling sau đó tăng.

Các bước thực thi:

1. Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly` từ thư mục gốc repo **một lần** (chế độ kết hợp `--json --paths-only` / `-Json -PathsOnly`). Parse tối thiểu các field trong JSON payload:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Có thể lấy thêm `IMPL_PLAN`, `TASKS` cho các chained flow sau này.)
   - Nếu parse JSON thất bại, dừng và hướng dẫn người dùng chạy lại `$speckit-specify` hoặc kiểm tra môi trường feature branch.
   - Với dấu nháy đơn trong tham số như "I'm Groot", dùng cú pháp escape: ví dụ `'I'\''m Groot'` (hoặc dùng nháy kép nếu có thể: `"I'm Groot"`).

2. **NẾU TỒN TẠI**: Load `.specify/memory/constitution.md` để lấy các nguyên tắc project và constraint về governance.

3. Load file spec hiện tại. Thực hiện một lượt quét có cấu trúc để tìm độ mơ hồ và mức độ bao phủ theo taxonomy dưới đây. Với mỗi nhóm, đánh dấu trạng thái: Clear / Partial / Missing. Tạo một coverage map nội bộ để ưu tiên xử lý (không xuất raw map trừ khi không có câu hỏi nào được đặt).

   Phạm vi chức năng & hành vi:
   - Mục tiêu cốt lõi của người dùng & tiêu chí thành công
   - Các nội dung được tuyên bố rõ là ngoài phạm vi
   - Phân biệt vai trò / persona người dùng

   Domain & mô hình dữ liệu:
   - Entity, attribute, relationship
   - Quy tắc định danh & tính duy nhất
   - Lifecycle/chuyển trạng thái
   - Giả định về dung lượng / quy mô dữ liệu

   Tương tác & luồng UX:
   - Hành trình / chuỗi thao tác quan trọng của người dùng
   - Trạng thái lỗi/rỗng/loading
   - Ghi chú về accessibility hoặc localization

   Thuộc tính chất lượng phi chức năng:
   - Hiệu năng (mục tiêu latency, throughput)
   - Khả năng mở rộng (horizontal/vertical, giới hạn)
   - Độ tin cậy & tính sẵn sàng (uptime, kỳ vọng recovery)
   - Observability (logging, metrics, tracing signals)
   - Bảo mật & quyền riêng tư (authN/Z, bảo vệ dữ liệu, giả định về mối đe dọa)
   - Constraint về compliance / quy định pháp lý (nếu có)

   Tích hợp & dependency bên ngoài:
   - Dịch vụ/API bên ngoài và failure mode
   - Định dạng import/export dữ liệu
   - Giả định về protocol/versioning

   Edge case & xử lý lỗi:
   - Kịch bản tiêu cực
   - Rate limiting / throttling
   - Giải quyết xung đột (ví dụ chỉnh sửa đồng thời)

   Constraint & tradeoff:
   - Constraint kỹ thuật (ngôn ngữ, storage, hosting)
   - Tradeoff hoặc phương án thay thế đã bị loại bỏ một cách rõ ràng

   Thuật ngữ & tính nhất quán:
   - Thuật ngữ glossary chuẩn
   - Synonym cần tránh / thuật ngữ deprecated

   Tín hiệu hoàn tất:
   - Khả năng kiểm thử acceptance criteria
   - Các chỉ báo định lượng theo kiểu Definition of Done

   Khác / placeholder:
   - Marker TODO / quyết định chưa xử lý
   - Tính từ mơ hồ ("robust", "intuitive") nhưng thiếu định lượng

   Với mỗi nhóm ở trạng thái Partial hoặc Missing, thêm một cơ hội đặt câu hỏi ứng viên, trừ khi:
   - Việc làm rõ sẽ không làm thay đổi đáng kể implementation hoặc chiến lược validation
   - Nội dung đó chỉ liên quan đến phương pháp implementation, so sánh tech stack hoặc phân rã task (ghi chú nội bộ)

3a. **Runtime Requirement Signal enrichment**:
   - Nếu có `.agents/skills/runtime-verification/SKILL.md`, gọi mode `requirements`.
   - Chỉ dùng pattern detectable từ requirements; pattern stage `design/tasks/implementation` không được tạo câu hỏi.
   - Signal làm lộ behavior có nhiều cách hiểu thực sự khác nhau được thêm vào coverage map/queue ưu tiên.
   - Câu hỏi phải hỏi **behavior/acceptance**, không hỏi implementation mechanism.
   - Lesson chỉ cần technical design được đánh dấu nội bộ `DEFERRED_TO_PLAN` và không tiêu tốn quota 5 câu.
   - Khi câu trả lời được ghi vào spec, giữ requirement/acceptance ref để plan trace lại.


4. Tạo (nội bộ) một hàng đợi ưu tiên các câu hỏi làm rõ ứng viên (tối đa 5). **KHÔNG** xuất tất cả cùng lúc. Áp dụng các constraint sau:
    - Tối đa 5 câu hỏi cho toàn bộ session.
    - Mỗi câu hỏi phải có thể trả lời bằng MỘT TRONG HAI dạng:
       - Một lựa chọn trắc nghiệm ngắn (2–5 phương án riêng biệt, loại trừ lẫn nhau), HOẶC
       - Một câu trả lời một từ / cụm từ ngắn (ràng buộc rõ: "Answer in <=5 words").
    - Chỉ đưa vào các câu hỏi mà câu trả lời có ảnh hưởng đáng kể đến architecture, data modeling, phân rã task, test design, hành vi UX, mức độ sẵn sàng vận hành hoặc validation về compliance.
    - Cân bằng độ bao phủ giữa các nhóm: ưu tiên các nhóm chưa rõ có tác động cao nhất; tránh hỏi hai câu tác động thấp khi còn một vùng tác động cao duy nhất (ví dụ security posture) chưa được giải quyết.
    - Loại các câu đã có câu trả lời, preference về style không quan trọng hoặc chi tiết thực thi ở mức plan (trừ khi chúng chặn tính đúng đắn).
    - Ưu tiên các nội dung làm rõ giúp giảm rủi ro làm lại ở downstream hoặc ngăn acceptance test bị lệch.
    - Nếu còn hơn 5 nhóm chưa giải quyết, chọn 5 nhóm đứng đầu theo heuristic (Impact * Uncertainty).

5. Vòng lặp hỏi tuần tự (interactive):
    - Mỗi lần chỉ đưa ra **CHÍNH XÁC MỘT** câu hỏi.
    - **Chất lượng cách viết câu hỏi (áp dụng cho mọi câu hỏi, MC hoặc short-answer):**
       - Mở đầu bằng `**Question:**`, sau đó là một câu hỏi đầy đủ kết thúc bằng `?`. Phần nội dung trước dấu `?` phải tự có nghĩa khi đứng riêng.
       - **KHÔNG BAO GIỜ** dùng topic label, section heading hoặc requirement id làm chính câu hỏi. Ví dụ `Acceptance device/runtime matrix (FR-023)` là **KHÔNG HỢP LỆ** — đó là label, không phải câu hỏi.
       - Sau dấu `?`, suffix duy nhất được phép là requirement/question id trong ngoặc và là tùy chọn. Định dạng chính xác: `**Question:** <interrogative>?` hoặc `**Question:** <interrogative>? (FR-023)`. Không bao giờ đặt id trước dấu `?`, và không bao giờ dùng id (đứng riêng hoặc đi kèm topic label) làm toàn bộ prompt.
       - Ngay sau dòng câu hỏi, thêm một câu "Why it matters" bằng ngôn ngữ dễ hiểu (nêu hệ quả đối với acceptance hoặc shipping) trước phần recommendation/options.
       - Dùng cách diễn đạt đời thường; chỉ đưa jargon vào khi được định nghĩa ngay trong cùng câu. Tự kiểm tra: người đọc không biết Spec Kit vẫn phải có thể trả lời chỉ từ dòng Question. Ngắn gọn thì được, khó hiểu thì không.
    - Với câu hỏi trắc nghiệm:
       - **Phân tích tất cả phương án** và xác định **phương án phù hợp nhất** dựa trên:
          - Best practice cho loại project
          - Pattern phổ biến trong các implementation tương tự
          - Giảm rủi ro (security, performance, maintainability)
          - Mức độ phù hợp với các mục tiêu hoặc constraint đã nêu rõ trong spec
       - Trình bày **phương án đề xuất** nổi bật ở đầu cùng lý do rõ ràng (1–2 câu giải thích vì sao đây là lựa chọn tốt nhất).
       - Định dạng: `**Recommended:** Option [X] - <reasoning>`
       - Sau đó render tất cả phương án dưới dạng bảng Markdown:

       | Option | Description |
       |--------|-------------|
       | A | <Option A description> |
       | B | <Option B description> |
       | C | <Option C description> (add D/E as needed up to 5) |
       | Short | Provide a different short answer (<=5 words) (Include only if free-form alternative is appropriate) |

       - Sau bảng, thêm: `You can reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.`
    - Với dạng short-answer (không có các lựa chọn rời rạc có ý nghĩa):
       - Đưa ra **câu trả lời gợi ý** dựa trên best practice và context.
       - Định dạng: `**Suggested:** <your proposed answer> - <brief reasoning>`
       - Sau đó xuất: `Format: Short answer (<=5 words). You can accept the suggestion by saying "yes" or "suggested", or provide your own answer.`
    - Sau khi người dùng trả lời:
       - Nếu người dùng trả lời "yes", "recommended" hoặc "suggested", dùng recommendation/suggestion đã nêu trước đó làm câu trả lời.
       - Nếu không, kiểm tra xem câu trả lời có ánh xạ được vào một option hoặc đáp ứng constraint <=5 từ hay không.
       - Nếu còn mơ hồ, hỏi lại ngắn gọn để phân biệt (vẫn tính là cùng một câu hỏi; không chuyển sang câu tiếp theo).
       - Khi câu trả lời đạt yêu cầu, ghi vào working memory (chưa ghi xuống disk) rồi chuyển sang câu tiếp theo trong queue.
    - Dừng hỏi thêm khi:
       - Mọi điểm mơ hồ quan trọng đã được giải quyết sớm (các mục còn lại trong queue trở nên không cần thiết), HOẶC
       - Người dùng báo đã xong ("done", "good", "no more"), HOẶC
       - Đã hỏi đủ 5 câu.
    - Không bao giờ tiết lộ trước các câu hỏi còn lại trong queue.
    - Nếu ngay từ đầu không có câu hỏi hợp lệ nào, lập tức báo không có điểm mơ hồ quan trọng.

6. Tích hợp sau **MỖI** câu trả lời đã được chấp nhận (cách cập nhật tăng dần):
    - Duy trì representation trong memory của spec (load một lần từ đầu) cùng raw file content.
    - Với câu trả lời đầu tiên được tích hợp trong session:
       - Đảm bảo có section `## Clarifications` (nếu thiếu thì tạo ngay sau section context/overview cấp cao nhất theo spec template).
       - Bên dưới, tạo subheading `### Session YYYY-MM-DD` cho ngày hôm nay nếu chưa có.
    - Ngay sau khi chấp nhận câu trả lời, append một bullet: `- Q: <question> → A: <final answer>`.
    - Sau đó áp dụng ngay nội dung làm rõ vào section phù hợp nhất:
       - Mơ hồ về chức năng → Cập nhật hoặc thêm bullet trong Functional Requirements.
       - Tương tác người dùng / phân biệt actor → Cập nhật subsection User Stories hoặc Actors (nếu có) với role, constraint hoặc scenario đã được làm rõ.
       - Data shape / entity → Cập nhật Data Model (thêm field, type, relationship) nhưng giữ thứ tự; ghi constraint mới một cách ngắn gọn.
       - Constraint phi chức năng → Thêm/sửa tiêu chí đo lường trong Success Criteria > Measurable Outcomes (chuyển tính từ mơ hồ thành metric hoặc target rõ ràng).
       - Edge case / negative flow → Thêm bullet mới trong Edge Cases / Error Handling (hoặc tạo subsection này nếu template có placeholder).
       - Xung đột thuật ngữ → Chuẩn hóa thuật ngữ trong toàn spec; chỉ giữ thuật ngữ cũ khi cần bằng cách thêm `(formerly referred to as "X")` một lần.
    - Nếu nội dung làm rõ khiến một phát biểu mơ hồ trước đó không còn đúng, thay thế phát biểu đó thay vì tạo bản trùng; không để lại nội dung lỗi thời gây mâu thuẫn.
    - Lưu file spec **SAU MỖI** lần tích hợp để giảm rủi ro mất context (atomic overwrite).
    - Giữ nguyên formatting: không sắp xếp lại các section không liên quan; giữ nguyên heading hierarchy.
    - Mỗi nội dung làm rõ được chèn phải tối thiểu và có thể kiểm thử (tránh narrative drift).

7. Validation (thực hiện sau **MỖI** lần ghi và một lượt cuối):
   - Session Clarifications chứa đúng một bullet cho mỗi câu trả lời đã được chấp nhận (không trùng).
   - Tổng số câu hỏi đã hỏi (và được chấp nhận) ≤ 5.
   - Các section đã cập nhật không còn placeholder mơ hồ mà câu trả lời mới vừa giải quyết.
   - Không còn phát biểu trước đó bị mâu thuẫn (quét để loại các phương án nay đã không còn hợp lệ).
   - Cấu trúc Markdown hợp lệ; heading mới duy nhất được phép: `## Clarifications`, `### Session YYYY-MM-DD`.
   - Thuật ngữ nhất quán: dùng cùng một thuật ngữ chuẩn trong tất cả section đã cập nhật.
   - **Re-run Project Docs Impact Check** nếu clarification làm đổi actor, system boundary/surface, core flow, domain/lifecycle, permission/ownership hoặc semantics dùng chung; cập nhật mục `Project Docs Impact` trong `spec.md` để thêm/bỏ đúng project-level docs bị tác động.

8. Ghi spec đã cập nhật trở lại `FEATURE_SPEC`.

9. **Re-validate Spec Quality Checklist** (nếu tồn tại):
   - Kiểm tra xem `FEATURE_DIR/checklists/requirements.md` có tồn tại hay không.
   - Nếu **KHÔNG** tồn tại, bỏ qua bước này âm thầm.
   - Nếu có:
     1. Đọc file checklist.
     2. Xác định tất cả các dòng checkbox theo GitHub task-list — các dòng khớp `- [ ]`, `- [x]` hoặc `- [X]` (không phân biệt hoa thường, chấp nhận khoảng trắng đầu dòng cho item lồng nhau) và nằm ngoài code fence. Bỏ qua toàn bộ nội dung khác (heading, note, bullet không phải checkbox, metadata).
     3. Với mỗi dòng checkbox, ghi trạng thái marker hiện tại (checked hoặc unchecked) và text của item vào before-snapshot list.
     4. Đánh giá lại từng checkbox item dựa trên **spec đã cập nhật** (phiên bản vừa lưu ở bước 7).
     5. Với mỗi checkbox item, chỉ cập nhật khi trạng thái checked/unchecked thực sự thay đổi:
        - Nếu item giờ đạt và trước đó unchecked: đổi `[ ]` thành `[x]`.
        - Nếu item giờ không đạt và trước đó checked: đổi `[x]`/`[X]` thành `[ ]`.
        - Nếu trạng thái không đổi: giữ nguyên marker (bao gồm cả kiểu chữ hiện có) để tránh cosmetic diff.
     6. Lưu file checklist đã cập nhật. **Chỉ toggle phần marker `[ ]`/`[x]` của các dòng checkbox có trạng thái thay đổi.** Mọi nội dung khác trong file — heading, metadata, note, thứ tự dòng, whitespace — phải giữ nguyên để tránh diff nhiễu.
     7. So sánh before-snapshot với trạng thái hiện tại để tính ba danh sách dùng cho Completion Report:
        - **Newly passing**: item đổi từ unchecked sang checked.
        - **Regressions**: item đổi từ checked sang unchecked.
        - **Still unchecked**: item vẫn unchecked.
     8. Ghi lại số lượng pass trước/sau theo checked/total checkbox items (ví dụ: "12/16 → 15/16 items passing").

Quy tắc hành vi:

- Nếu không tìm thấy điểm mơ hồ có ý nghĩa (hoặc mọi câu hỏi tiềm năng đều có tác động thấp), trả lời: "No critical ambiguities detected worth formal clarification." và đề xuất tiếp tục.
- Nếu thiếu file spec, hướng dẫn người dùng chạy `$speckit-specify` trước (không tạo spec mới ở đây).
- Không bao giờ vượt quá 5 câu hỏi đã hỏi trong toàn session (các lượt hỏi lại để làm rõ cùng một câu không tính là câu mới).
- Tránh câu hỏi suy đoán về tech stack trừ khi thiếu thông tin đó chặn tính rõ ràng về chức năng.
- Tôn trọng tín hiệu kết thúc sớm của người dùng ("stop", "done", "proceed").
- Nếu không hỏi câu nào vì mức độ bao phủ đã đầy đủ, xuất một coverage summary ngắn gọn (mọi category là Clear), sau đó đề xuất chuyển sang bước tiếp theo.
- Nếu đã hết quota mà vẫn còn category tác động cao chưa giải quyết, nêu rõ chúng dưới mục Deferred cùng lý do.

Context để ưu tiên: $ARGUMENTS

## Hook bắt buộc sau khi thực thi

**Bạn BẮT BUỘC phải hoàn thành section này trước khi báo hoàn tất cho người dùng.**

Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc project hay không.
- Nếu không tồn tại, hoặc không có hook nào được đăng ký dưới `hooks.after_clarify`, chuyển sang Completion Report.
- Nếu có, đọc file và tìm các entry dưới key `hooks.after_clarify`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: hãy báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và không hook nào được kiểm tra, bao gồm cả hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục tới Completion Report.
- Loại các hook có `enabled` được đặt rõ ràng là `false`. Với hook không có field `enabled`, mặc định coi là đã bật.
- Với mỗi hook còn lại, **không** tự diễn giải hoặc đánh giá biểu thức `condition` của hook:
  - Nếu hook không có field `condition`, hoặc field này là null/rỗng, coi hook là có thể thực thi.
  - Nếu hook định nghĩa `condition` không rỗng, bỏ qua hook và để việc đánh giá condition cho implementation của HookExecutor.
- Khi dựng lệnh gọi từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với mỗi hook có thể thực thi, xuất nội dung sau dựa trên cờ `optional`:
  - **Hook bắt buộc** (`optional: false`) — **Bạn BẮT BUỘC phải phát `EXECUTE_COMMAND:` cho từng hook bắt buộc**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    Sau khi phát block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ hook chạy xong trước khi tiếp tục. Chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách gọi thực tế có thể khác với id `{command}` hiển thị ở trên; ví dụ agent chạy ở skills mode có thể gọi dưới dạng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ phát block mà không gọi hook thì chưa được tính là đã chạy hook.
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

Báo cáo khi hoàn tất (sau khi vòng hỏi kết thúc hoặc dừng sớm):
- Số câu hỏi đã hỏi & đã trả lời.
- Đường dẫn tới spec đã cập nhật.
- Các section đã được chỉnh sửa (liệt kê tên).
- Trạng thái Spec Quality Checklist (nếu `FEATURE_DIR/checklists/requirements.md` đã được re-validate): hiển thị số lượng pass trước/sau (ví dụ: "Spec Quality Checklist: 12/16 → 15/16 items passing") và liệt kê mọi item đổi trạng thái — cả item mới được check (unchecked → checked) và regression (checked → unchecked). Nếu vẫn còn item unchecked, liệt kê chúng là những vùng cần chú ý.
- Coverage summary table liệt kê từng taxonomy category với Status: Resolved (trước đó Partial/Missing và đã xử lý), Deferred (vượt quota câu hỏi, hoặc nội dung còn lại chỉ liên quan tới phương pháp implementation, so sánh tech stack hoặc phân rã task), Clear (đã đủ rõ từ trước), Outstanding (vẫn Partial/Missing nhưng tác động thấp).
- Nếu còn Outstanding hoặc Deferred ảnh hưởng system boundary, actor, core flow, domain concept hoặc lifecycle, đề xuất chạy lại `$speckit-clarify` trước technical planning; không đẩy ambiguity cốt lõi sang Lazy Modeling Gate/plan.
- Báo rõ `Project Docs Impact` đã được rà lại hay không thay đổi sau clarification.
- Command tiếp theo mặc định: `$speckit-plan`. Plan tự chạy `ensure-model(spec)` trước khi lập kế hoạch; `$speckit-system-modeling-vi` chỉ cần gọi thủ công nếu người dùng muốn xem model ngay.

## Hoàn tất khi

- [ ] Đã xác định các điểm mơ hồ trong spec và tích hợp nội dung làm rõ vào file spec
- [ ] Đã re-validate spec quality checklist dựa trên spec đã cập nhật (nếu `FEATURE_DIR/checklists/requirements.md` tồn tại)
- [ ] Đã rà lại `Project Docs Impact` nếu clarification làm thay đổi mental model chung.
- [ ] Extension hook đã được dispatch hoặc bỏ qua theo đúng các quy tắc trong phần Mandatory Post-Execution Hooks ở trên
- [ ] Đã báo cáo hoàn tất cho người dùng, gồm số câu hỏi đã trả lời, các section đã chỉnh sửa, trạng thái checklist và coverage summary

## Optional companion skill

Đọc protocol tại `../companion-skills.md`.

Ở stage clarify:
- không dùng companion để ép technical choice thành requirement;
- chỉ dùng companion như tín hiệu để nhận ra ambiguity có thể dẫn tới **behavior khác nhau đối với user/domain**;
- nếu ambiguity chỉ là implementation/tooling choice, không hỏi user; defer sang `speckit-plan-vi`;
- không materialize stack-specific command/file/library detail vào spec.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-clarify`
- Tên gốc: `speckit-clarify`
- Chính sách: `faithful`
- Commit nguồn: `390659c4ee776dfaca1eb1049862652611f962d2`
