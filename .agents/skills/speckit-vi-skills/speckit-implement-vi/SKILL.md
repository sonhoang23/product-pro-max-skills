---
name: "speckit-implement-vi"
description: "Thực thi kế hoạch implementation bằng cách xử lý và thực hiện toàn bộ task được định nghĩa trong tasks.md"
compatibility: "Yêu cầu cấu trúc dự án spec-kit có thư mục .specify/"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/implement.md"
---


## Đầu vào của người dùng

```text
$ARGUMENTS
```

Bạn **BẮT BUỘC** phải xem xét đầu vào của người dùng trước khi tiếp tục (nếu không rỗng).

## Kiểm tra trước khi thực thi

**Kiểm tra extension hook (trước khi implementation)**:
- Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu có, đọc file và tìm các entry trong key `hooks.before_implement`.
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

1. Chạy `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` từ thư mục gốc repo và parse danh sách FEATURE_DIR cùng AVAILABLE_DOCS. Mọi đường dẫn phải là đường dẫn tuyệt đối. Với dấu nháy đơn trong tham số như "I'm Groot", dùng cú pháp escape, ví dụ: 'I'\''m Groot' (hoặc dùng dấu nháy kép nếu có thể: "I'm Groot").

2. **Lazy Modeling Gate — tasks**:
   - Sau khi resolve `FEATURE_DIR`, chạy `ensure-model(tasks)` theo contract trong `speckit-system-modeling-vi`.
   - Nếu gate `tasks` pass + fresh thì tiếp tục ngay.
   - Nếu thiếu/stale/output mất/state legacy, tự invoke `$speckit-system-modeling-vi` ở mode `tasks`, chờ hoàn tất rồi kiểm tra lại.
   - Diagram Check có thể âm; `no-diagram-needed` vẫn là gate pass hợp lệ.
   - Nếu gate `blocked`, không bắt đầu code.

3. **Kiểm tra trạng thái checklist** (nếu FEATURE_DIR/checklists/ tồn tại):
   - Xem các marker checklist như một gate chỉ đọc: quét trạng thái checkbox, báo cáo trạng thái và hỏi trước khi tiếp tục khi cần; **KHÔNG** sửa file checklist hoặc marker.
   - `checklists/requirements.md` là checklist chất lượng spec tích hợp sẵn do `$speckit-specify` và `$speckit-clarify` duy trì; các checklist tùy chỉnh do `$speckit-checklist` tạo là artifact review chất lượng yêu cầu thuộc quyền sở hữu của reviewer.
   - Với checklist tùy chỉnh, `[x]` nghĩa là reviewer đã xác định tiêu chí chất lượng yêu cầu được đáp ứng; nó **KHÔNG** có nghĩa là công việc implementation đã hoàn tất.
   - Quét tất cả file checklist trong thư mục checklists/.
   - Với mỗi checklist, đếm:
     - Tổng số mục: Tất cả dòng khớp `- [ ]`, `- [X]` hoặc `- [x]`.
     - Mục đã check: Các dòng khớp `- [X]` hoặc `- [x]`.
     - Mục chưa check: Các dòng khớp `- [ ]`.
   - Tạo bảng trạng thái:

     ```text
     | Checklist | Total | Checked | Unchecked | Status |
     |-----------|-------|---------|-----------|--------|
     | ux.md     | 12    | 12      | 0         | ✓ PASS |
     | test.md   | 8     | 5       | 3         | ✗ FAIL |
     | security.md | 6   | 6       | 0         | ✓ PASS |
     ```

   - Tính trạng thái tổng thể:
     - **PASS**: Tất cả checklist có 0 mục chưa check.
     - **FAIL**: Có ít nhất một checklist còn mục chưa check.

   - **Nếu có checklist còn mục chưa check**:
     - Hiển thị bảng cùng số lượng mục chưa check.
     - **DỪNG** và hỏi: "Một số checklist vẫn còn mục chưa được đánh dấu hoàn tất. Bạn có muốn tiếp tục implementation không? (yes/no)"
     - Chờ phản hồi của người dùng trước khi tiếp tục.
     - Nếu người dùng trả lời "no", "wait" hoặc "stop", dừng thực thi.
     - Nếu người dùng trả lời "yes", "proceed" hoặc "continue", tiếp tục sang bước 4.

   - **Nếu tất cả checklist đã được check**:
     - Hiển thị bảng cho thấy tất cả checklist đều pass.
     - Tự động tiếp tục sang bước 4.

4. Nạp và phân tích ngữ cảnh implementation:
   - **BẮT BUỘC**: Đọc tasks.md để lấy đầy đủ danh sách task và kế hoạch thực thi.
   - **BẮT BUỘC**: Đọc plan.md để lấy tech stack, kiến trúc và cấu trúc file.
   - **KHI TASK THAM CHIẾU US/FR HOẶC CORE BEHAVIOR**: đọc phần tương ứng trong `spec.md`.
   - **NẾU CÓ `spec-diagram/` hoặc `plan-diagram/`**: chỉ đọc khi visual context giúp hiểu flow/architecture của task; source of truth vẫn là `spec.md`, `plan.md`, `data-model.md` và `contracts/`.
   - **NẾU CÓ task `Project Docs Promotion` trong phase hiện tại của `tasks.md`**: chỉ đọc/sửa đúng project-level docs/diagram mà task tham chiếu **sau khi** implementation task và validation của phase đã hoàn tất, đồng thời gate `implementation:phase-XX` đã pass + fresh; không tự mở rộng phạm vi sang tài liệu không liên quan.
   - **NẾU CÓ**: Đọc data-model.md để lấy entity và relationship.
   - **NẾU CÓ**: Đọc contracts/ để lấy đặc tả API và yêu cầu test.
   - **NẾU CÓ**: Đọc research.md để lấy quyết định kỹ thuật và constraint.
   - **NẾU CÓ**: Đọc .specify/memory/constitution.md để lấy các constraint quản trị.
   - **NẾU CÓ**: Đọc quickstart.md để lấy các kịch bản integration.
   - **NẾU `tasks.md` có `Runtime Risk Coverage`**: đọc trace `Risk ID → plan prevention design → Task ID → Required evidence`. Khi thực hiện task có runtime-risk reference, nạp `.agents/skills/runtime-verification/SKILL.md` ở mode `implementation` và chỉ Risk ID/category tương ứng; không chạy lại toàn catalog để tự mở rộng scope.
   - Đọc prevention design tương ứng trong `plan.md`. Nếu implementation cần đổi intended behavior/design để xử lý risk, dừng phần affected và cập nhật artifact có thẩm quyền trước; không để code âm thầm trở thành source of truth.
   - Implementation không được âm thầm thay đổi business semantics trong `spec.md` hoặc intended technical design trong `plan.md`/technical artifacts; nếu technical reality buộc phải đổi, dừng và cập nhật upstream artifact trước.

5. **Xác minh thiết lập dự án**:
   - **BẮT BUỘC**: Tạo/xác minh các file ignore dựa trên thiết lập thực tế của dự án.

   **Logic phát hiện & tạo file**:
   - Kiểm tra lệnh sau có chạy thành công hay không để xác định repo có phải Git repo không (nếu có thì tạo/xác minh .gitignore):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Kiểm tra Dockerfile* có tồn tại hoặc Docker được nhắc trong plan.md → tạo/xác minh .dockerignore.
   - Kiểm tra .eslintrc* có tồn tại → tạo/xác minh .eslintignore.
   - Kiểm tra eslint.config.* có tồn tại → bảo đảm các entry `ignores` trong config bao phủ các pattern bắt buộc.
   - Kiểm tra .prettierrc* có tồn tại → tạo/xác minh .prettierignore.
   - Kiểm tra .npmrc hoặc package.json có tồn tại → tạo/xác minh .npmignore (nếu publish).
   - Kiểm tra có file terraform (*.tf) → tạo/xác minh .terraformignore.
   - Kiểm tra có cần .helmignore hay không (có Helm chart) → tạo/xác minh .helmignore.

   **Nếu file ignore đã tồn tại**: Xác minh file có các pattern thiết yếu, chỉ thêm những pattern quan trọng còn thiếu.
   **Nếu file ignore chưa tồn tại**: Tạo file với đầy đủ pattern cho công nghệ đã phát hiện.

   **Các pattern phổ biến theo công nghệ** (từ tech stack trong plan.md):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `*.dll`, `autom4te.cache/`, `config.status`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Pattern riêng theo tool**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

6. Parse cấu trúc tasks.md và trích xuất:
   - **Các phase của task**: Setup, Tests, Core, Integration, Polish.
   - **Dependency của task**: Quy tắc thực thi tuần tự và song song.
   - **Chi tiết task**: ID, mô tả, đường dẫn file, marker song song [P].
   - **Luồng thực thi**: Thứ tự và yêu cầu dependency.

7. Thực thi implementation theo kế hoạch task:
   - **Thực thi theo từng phase**: Hoàn thành từng phase trước khi chuyển sang phase tiếp theo.
   - **Lazy Modeling Gate giữa các phase**:
     - Trước khi bắt đầu Phase 1, gate `tasks` ở bước 2 đã phải pass.
     - Trước khi bắt đầu Phase N > 1, chạy `ensure-model(implementation:phase-(N-1))`.
     - Nếu gate phase trước pass + fresh → tiếp tục ngay.
     - Nếu thiếu/stale/output mất → tự invoke `$speckit-system-modeling-vi` ở mode `implementation` với scope phase trước, chờ hoàn tất và kiểm tra lại.
     - Nếu Diagram Check âm, ghi `no-diagram-needed` rồi tiếp tục; không ép tạo diagram.
     - Nếu resume giữa chừng, resolve phase hoàn tất gần nhất từ `tasks.md` + trạng thái implementation thực tế rồi gate phase đó trước khi chạy phase kế tiếp.
     - Không model phase đang code dở; modeling implementation mô tả current state của phase đã hoàn tất.
   - **Tôn trọng dependency**: Chạy task tuần tự theo đúng thứ tự; các task song song [P] có thể chạy cùng nhau.
   - **Theo cách tiếp cận TDD**: Thực thi task test trước task implementation tương ứng.
   - **Điều phối theo file**: Các task tác động đến cùng file phải chạy tuần tự.
   - **Checkpoint validation**: Xác minh code/tests/QA của phase hoàn tất trước. Với task được map từ Runtime Risk Coverage, evidence bắt buộc phải được ghi nhận là `PASS | FAIL | BLOCKED`; `unavailable`, "chưa chạy được" hoặc test tầng khác pass **không được** tự quy đổi thành runtime `PASS`. Task runtime-risk chưa có evidence bắt buộc thì không được đánh dấu `[X]`. Sau đó chạy modeling `implementation:phase-XX`; chỉ khi gate pass + fresh mới chạy Project Docs Promotion Check và promotion tasks của phase. Phase chỉ được đánh dấu hoàn tất sau cả promotion check (hoặc xác nhận `None`).

8. Quy tắc thực thi implementation:
   - **Setup trước**: Khởi tạo cấu trúc dự án, dependency và cấu hình.
   - **Test trước code**: Nếu cần viết test cho contract, entity và các kịch bản integration.
   - **Phát triển phần lõi**: Implement model, service, CLI command, endpoint.
   - **Công việc integration**: Kết nối database, middleware, logging, dịch vụ bên ngoài.
   - **Hoàn thiện và validation**: Unit test, tối ưu performance, tài liệu.

9. Theo dõi tiến độ và xử lý lỗi:
   - Báo cáo tiến độ sau mỗi task đã hoàn thành.
   - Dừng thực thi nếu bất kỳ task không song song nào thất bại.
   - Với các task song song [P], tiếp tục các task thành công và báo cáo những task thất bại.
   - Cung cấp thông báo lỗi rõ ràng, kèm ngữ cảnh để debug.
   - Đề xuất bước tiếp theo nếu không thể tiếp tục implementation.
   - **QUAN TRỌNG**: Với task đã hoàn thành, bảo đảm đánh dấu task thành [X] trong file tasks.

10. Validation khi hoàn tất:
   - Xác minh tất cả task bắt buộc đã hoàn thành.
   - Kiểm tra các feature đã implement khớp với specification gốc.
   - Xác nhận test pass và coverage đáp ứng yêu cầu.
   - Xác nhận mọi Runtime Risk `APPLIES` trong `tasks.md` đã có task hoàn tất với đúng evidence runtime yêu cầu; không dùng unit/integration/E2E pass để thay thế proof mà failure pattern yêu cầu ở entry/auth/browser/service boundary.
   - Xác nhận implementation còn phù hợp prevention design trong plan và requirement refs upstream; drift semantics chưa được hợp thức hóa làm phase chưa hoàn tất.
   - Xác nhận implementation tuân theo technical plan.
   - Chạy **Project Docs Promotion Check** cho phase vừa verify: nếu implementation làm thay đổi mental model chung, chỉ promote semantics đã tồn tại trong code/config/runtime và đã được implementation modeling xác nhận vào project-level docs/diagram tương ứng; không copy nguyên planned spec/plan.
   - Nếu phát hiện phase đã implement làm đổi mental model chung nhưng `tasks.md` không có promotion task, phase chưa hoàn tất; bổ sung/ghi gap có thể truy vết trước khi chuyển phase. Không chờ đến converge để lần đầu promote một capability đã implement.

Lưu ý: Command này giả định đã có đầy đủ task breakdown trong tasks.md. Nếu task chưa đầy đủ hoặc bị thiếu, đề xuất chạy `$speckit-tasks` trước để tạo lại danh sách task.

## Hook bắt buộc sau khi thực thi

**Bạn BẮT BUỘC phải hoàn thành phần này trước khi báo cáo hoàn tất cho người dùng.**

Kiểm tra xem `.specify/extensions.yml` có tồn tại ở thư mục gốc của dự án hay không.
- Nếu không tồn tại, hoặc không có hook nào được đăng ký trong `hooks.after_implement`, chuyển sang phần Báo cáo hoàn tất.
- Nếu có, đọc file và tìm các entry trong key `hooks.after_implement`.
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

## Modeling implementation theo kiểu lazy

Không bắt buộc chạy modeling ngay sau từng phase.

- Modeling của một phase được bảo đảm **trước khi phase kế tiếp bắt đầu**.
- Phase cuối cùng được `$speckit-converge` tự gate trước khi convergence analysis; nếu người dùng không chạy converge thì có thể gọi modeling thủ công khi cần.
- Output implementation vẫn nằm trong `FEATURE_DIR/implementation-diagram/`, ưu tiên filename `phase-XX-<model>.html`.
- Không regenerate sau từng task nhỏ.
- Diagram current-state phải phân biệt rõ với intended design.

## Báo cáo hoàn tất

Báo cáo trạng thái cuối cùng cùng phần tóm tắt công việc đã hoàn thành.

## Hoàn tất khi

- [ ] Lazy Modeling Gate `tasks` đã pass + fresh trước khi code bắt đầu.
- [ ] Mỗi phase sau chỉ bắt đầu sau khi modeling gate của phase implementation trước đã pass.
- [ ] Tất cả task trong tasks.md đã hoàn thành và được đánh dấu `[X]`.
- [ ] Mọi Runtime Risk `APPLIES` đã có task/evidence bắt buộc ở trạng thái PASS; không còn runtime task FAIL/BLOCKED bị coi là hoàn tất.
- [ ] Implementation đã được validation theo specification, plan/intended technical design và test coverage.
- [ ] Project Docs Promotion Check của mọi phase đã hoàn tất đã pass hoặc feature được xác nhận không làm thay đổi mental model chung.
- [ ] Extension hook đã được điều phối hoặc bỏ qua theo đúng quy tắc trong phần Hook bắt buộc sau khi thực thi ở trên.
- [ ] Đã báo cáo hoàn tất cho người dùng với phần tóm tắt công việc đã hoàn thành.

## Optional companion skill — BẮT BUỘC khi repo cài companion

Đọc protocol tại `../companion-skills.md`.

Trước khi thực hiện task chạm technical boundary:
1. discover/load companion phù hợp;
2. chỉ đọc reference liên quan tới task hiện tại;
3. thực thi stack-specific guardrail cùng prevention design đã materialize trong plan/tasks;
4. không hand-wave source-complete thành runtime PASS: evidence phải đúng boundary mà task yêu cầu;
5. source/config/generated artifact đổi sau PASS thì invalidates evidence liên quan theo Final Revision Verification Rule;
6. nếu implementation cần đổi business semantics để xử lý guardrail, dừng và quay lại artifact có thẩm quyền;
7. lesson mới đủ tổng quát phải được phân loại cho `runtime-verification`, không nhét vào companion như catalog thứ hai.

Báo cáo phase SHOULD nêu companion guardrail đã áp dụng và obligation còn `DEFERRED/BLOCKED`.


## Nguồn Việt hóa

- Skill gốc: `.agents/skills/speckit-skills/speckit-implement`
- Tên gốc: `speckit-implement`
- Chính sách: `faithful`
- Commit nguồn: `566943554c617128f73e2e4864aeb713bacd0478`
