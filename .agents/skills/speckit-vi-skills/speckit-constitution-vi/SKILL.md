---
name: "speckit-constitution-vi"
description: "Tạo hoặc cập nhật hiến chương dự án từ các nguyên tắc do người dùng cung cấp trực tiếp hoặc nhập theo tương tác."
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/constitution.md"
---

## Đầu vào người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu có nội dung).

## Giới hạn phạm vi

Phạm vi công việc của command này chỉ giới hạn ở việc cập nhật chính hiến chương dự án. Các template và command phụ thuộc sẽ đọc hiến chương tại runtime và không được chỉnh sửa tại đây.

- Phân loại từng phần trong đầu vào của người dùng thành nội dung thuộc hiến chương hoặc một ý định riêng không thuộc quản trị.
- Nếu đầu vào có yêu cầu triển khai feature, sinh code, refactor, build hoặc deployment, bạn **KHÔNG ĐƯỢC** thực hiện các yêu cầu đó. Thay vào đó, hãy trích chúng thành các ý định hoãn lại.
- Bạn **KHÔNG ĐƯỢC** tạo, sửa hoặc xóa source file của ứng dụng, feature route, component, test, file deployment hay artifact nào khác không liên quan đến workflow của hiến chương.
- Nếu chưa rõ một instruction có thuộc nội dung hiến chương hay không, hãy hỏi lại để làm rõ trước khi thay đổi.
- Sau khi hoàn tất cập nhật hiến chương, thêm một phần `Next Actions` cho từng ý định đã hoãn. Liệt kê ý định ban đầu và đề xuất command Spec Kit phù hợp để xử lý tiếp, chẳng hạn `$speckit-specify`, nhưng không được tự gọi command đó.
- Nếu không có ý định nào ngoài phạm vi quản trị, bỏ phần `Next Actions`.

## Known-failure prevention — mức governance

Nếu repo có `.agents/skills/runtime-verification/SKILL.md`, đọc **chỉ lifecycle/authority policy**; không nạp failure catalog và không copy Risk ID cụ thể vào constitution.

- Constitution MAY chốt nguyên tắc project-wide về phòng ngừa known reusable failure, evidence integrity và authority chain.
- Không biến runtime catalog thành authority layer mới và không thêm requirement feature cụ thể vào constitution.
- Nếu user không yêu cầu governance principle tương ứng, chỉ dùng policy này để tránh tạo quy tắc mâu thuẫn; không tự phát minh điều khoản.


## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi cập nhật hiến chương)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry dưới key `hooks.before_constitution`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và rằng chưa có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục quy trình bình thường.
- Loại các hook có `enabled` được đặt rõ ràng là `false`. Hook không có field `enabled` được xem là bật mặc định.
- Với từng hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition`:
  - Nếu hook không có field `condition`, hoặc giá trị null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để việc đánh giá điều kiện cho implementation `HookExecutor`.
- Khi tạo command invocation từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với từng hook có thể thực thi, xuất nội dung sau tùy theo flag `optional`:
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ nó hoàn tất trước khi tiếp tục. Hãy chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` literal ở trên, ví dụ agent chạy theo chế độ skills có thể dùng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không chạy hook thì chưa được xem là đã thực thi.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua mà không cần thông báo.

## Quy trình

Bạn đang cập nhật hiến chương dự án tại `.specify/memory/constitution.md`. Khung hiến chương đang hoạt động được resolve tại thời điểm chạy command từ `constitution-template` thông qua stack resolve preset/template của Spec Kit.

Thực hiện theo luồng sau:

1. Chạy `.specify/scripts/powershell/resolve-template.ps1 constitution-template -Json` từ thư mục gốc của repository và parse `TEMPLATE_CONTENT` thành template đang hoạt động.
   - Resolver dùng chung sẽ áp dụng project override, các preset layer được compose và extension layer trước khi fallback về core template. Quy trình này **BẮT BUỘC** phải thành công trước khi tiếp tục.
   - Nếu resolver thất bại, dừng lại và báo lỗi resolve; không được tiếp tục chỉ với một template layer riêng lẻ.
   - Nếu `.specify/memory/constitution.md` đã tồn tại, tải file đó làm nguồn chứa các giá trị và amendment riêng của dự án hiện tại. Giữ lại thông tin vẫn còn áp dụng khi đưa scaffold mới đã resolve vào.
   - Nếu file chưa tồn tại, dùng template đã resolve làm tài liệu khởi đầu.
   - Không ghi ngược thay đổi vào bất kỳ template layer có version nào.
   - Xác định mọi placeholder token có dạng `[ALL_CAPS_IDENTIFIER]`.
   **QUAN TRỌNG**: Người dùng có thể yêu cầu số lượng nguyên tắc ít hơn hoặc nhiều hơn số có trong template. Nếu họ chỉ định số lượng, hãy tôn trọng yêu cầu đó và vẫn bám theo cấu trúc chung của template. Cập nhật tài liệu tương ứng.

2. Thu thập hoặc suy ra giá trị cho các placeholder:
   - Nếu đầu vào của người dùng trong hội thoại đã cung cấp giá trị, dùng giá trị đó.
   - Nếu chưa có, suy ra từ context hiện có trong repo (README, docs, các phiên bản hiến chương trước nếu được nhúng).
   - Với ngày quản trị: `RATIFICATION_DATE` là ngày thông qua ban đầu (nếu không biết thì hỏi hoặc đánh dấu TODO), `LAST_AMENDED_DATE` là ngày hôm nay nếu có thay đổi; nếu không thay đổi thì giữ nguyên giá trị cũ.
   - `CONSTITUTION_VERSION` phải tăng theo quy tắc semantic versioning:
     - MAJOR: Xóa hoặc định nghĩa lại nguyên tắc/quy tắc quản trị theo cách không tương thích ngược.
     - MINOR: Thêm nguyên tắc/section mới hoặc mở rộng đáng kể hướng dẫn.
     - PATCH: Làm rõ, chỉnh câu chữ, sửa lỗi chính tả hoặc tinh chỉnh không làm thay đổi ngữ nghĩa.
   - Nếu chưa rõ nên tăng version theo loại nào, trình bày lý do đề xuất trước khi chốt.

3. Soạn nội dung hiến chương đã cập nhật, dùng template đã resolve làm cấu trúc bắt buộc:
   - Thay mọi placeholder bằng nội dung cụ thể (không để lại token trong ngoặc vuông, trừ các template slot mà dự án chủ động chưa định nghĩa; nếu giữ lại phải giải thích rõ lý do).
   - Giữ nguyên hệ phân cấp heading. Comment có thể bỏ sau khi đã thay nội dung, trừ khi chúng vẫn còn giá trị giải thích.
   - Đảm bảo mỗi section Nguyên tắc có: tên ngắn gọn, đoạn văn hoặc danh sách bullet mô tả các quy tắc không thể thỏa hiệp, và phần lý do rõ ràng nếu bản thân quy tắc chưa đủ dễ hiểu.
   - Đảm bảo section Quản trị nêu rõ quy trình amendment, chính sách versioning và kỳ vọng về việc rà soát tuân thủ.

4. Tạo Sync Impact Report dưới dạng HTML comment ở đầu file hiến chương sau khi cập nhật.
   Report này là scratch material tạm thời để con người review amendment, không phải nội dung quản trị; dự kiến sẽ được xóa trước khi file hiến chương đã sửa được commit.
   - Thay đổi version: cũ → mới.
   - Danh sách các nguyên tắc đã sửa (tiêu đề cũ → tiêu đề mới nếu có đổi tên).
   - Các section được thêm.
   - Các section bị xóa.
   - TODO cần xử lý tiếp nếu có placeholder nào được chủ động hoãn.

5. Validate trước khi xuất kết quả cuối:
   - Không còn token trong ngoặc vuông nào chưa được giải thích.
   - Dòng version khớp với report.
   - Ngày dùng định dạng ISO `YYYY-MM-DD`.
   - Các nguyên tắc phải mang tính tuyên bố, có thể kiểm chứng và không mơ hồ (ví dụ dùng "should" thì phải đổi thành MUST/SHOULD kèm lý do phù hợp).

6. Ghi nội dung hiến chương hoàn chỉnh trở lại `.specify/memory/constitution.md` (ghi đè).

7. Xuất bản tóm tắt cuối cùng cho người dùng gồm:
   - Version mới và lý do tăng version.
   - Mọi TODO placeholder hoặc hạng mục đã hoãn cần xử lý thủ công.
   - Commit message được đề xuất (ví dụ: `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).
   - Một phần `Next Actions` cho mọi ý định ngoài phạm vi quản trị đã bị hoãn.

## Yêu cầu định dạng và văn phong

- Dùng heading Markdown đúng như trong template (không hạ hoặc nâng cấp độ heading).
- Ngắt dòng rationale dài để dễ đọc (lý tưởng dưới 100 ký tự), nhưng không ép cứng đến mức câu văn mất tự nhiên.
- Chỉ để một dòng trống giữa các section.
- Tránh khoảng trắng thừa ở cuối dòng.

Nếu người dùng chỉ cung cấp cập nhật một phần (ví dụ chỉ sửa một nguyên tắc), vẫn phải thực hiện các bước validate và quyết định version.

Nếu thiếu thông tin quan trọng (ví dụ thực sự không biết ngày phê chuẩn), chèn `TODO(<FIELD_NAME>): explanation` và đưa mục đó vào Sync Impact Report trong phần hạng mục hoãn.

Chỉ được ghi vào `.specify/memory/constitution.md`; không tạo hoặc sửa source file của template.

## Kiểm tra sau khi thực thi

**Kiểm tra extension hook (sau khi cập nhật hiến chương)**:
Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry dưới key `hooks.after_constitution`.
- Nếu YAML không parse được hoặc không hợp lệ, không được âm thầm bỏ qua: báo cho người dùng rằng không thể đọc `.specify/extensions.yml` (kèm lỗi parser) và rằng chưa có hook nào được kiểm tra, bao gồm cả các hook bắt buộc (`optional: false`) đã đăng ký trong đó; sau đó tiếp tục quy trình bình thường.
- Loại các hook có `enabled` được đặt rõ ràng là `false`. Hook không có field `enabled` được xem là bật mặc định.
- Với từng hook còn lại, **không** cố diễn giải hoặc đánh giá biểu thức `condition`:
  - Nếu hook không có field `condition`, hoặc giá trị null/rỗng, xem hook là có thể thực thi.
  - Nếu hook có `condition` không rỗng, bỏ qua hook đó và để việc đánh giá điều kiện cho implementation `HookExecutor`.
- Khi tạo command invocation từ tên command của hook, thay dấu chấm (`.`) bằng dấu gạch ngang (`-`). Ví dụ: `speckit.git.commit` → `$speckit-git-commit`.
- Với từng hook có thể thực thi, xuất nội dung sau tùy theo flag `optional`:
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
    Sau khi xuất block trên, bạn **BẮT BUỘC** phải thực sự gọi hook và chờ nó hoàn tất trước khi tiếp tục. Hãy chạy hook theo đúng cách bạn tự chạy command đó trong agent/session hiện tại (cách invocation có thể khác với id `{command}` literal ở trên, ví dụ agent chạy theo chế độ skills có thể dùng `/skill:speckit-...` hoặc `$speckit-...`). Chỉ xuất block mà không chạy hook thì chưa được xem là đã thực thi.
- Nếu không có hook nào được đăng ký hoặc `.specify/extensions.yml` không tồn tại, bỏ qua mà không cần thông báo.

## Optional companion skill

Đọc protocol tại `../companion-skills.md`.

Ở stage constitution:
- MAY phát hiện companion local nhưng **không nạp technical reference chi tiết**;
- chỉ dùng để tránh tạo governance principle mâu thuẫn với policy template-wide mà người dùng đã chủ động chốt;
- không copy stack rule, file path, command, Risk ID hay implementation detail vào constitution;
- mọi technical obligation của companion được defer sang `speckit-plan-vi`.

Companion không thay đổi authority của constitution và không tự tạo điều khoản mới nếu user chưa yêu cầu.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-constitution`
- Tên gốc: `speckit-constitution`
- Chính sách: `faithful`
- Commit nguồn: `390659c4ee776dfaca1eb1049862652611f962d2`
