# Environment doctor

Nạp file này khi người dùng yêu cầu chạy diagnostics, health check hoặc troubleshooting lần đầu, hoặc khi họ gọi `/diagram-design:doctor` hay `/doctor`.

Mục tiêu là tạo một báo cáo một lần để kiểm tra mức độ sẵn sàng cục bộ cho import/export và command routing của Diagram Design, **không thay đổi file của người dùng và không cài dependency**.

Resolve installation của Diagram Design từ reference đang được nạp này, **không** từ current working directory của người dùng. Một project directory thông thường là nơi dự kiến sẽ gọi doctor và không được coi đó là lỗi đường dẫn repository.

Dùng hai diagnostic mode:

- **Installed-skill mode** (mặc định): kiểm tra runtime và skill installation đã resolve. Không yêu cầu các file chỉ dành cho maintainer trong repository.
- **Maintainer-checkout mode**: chỉ dùng khi installation root đã resolve có `CONTRIBUTING.md`, `.github/workflows/ci.yml` và `scripts/verify-plugin-package.py`. Khi đó bổ sung các repository-integrity check bên dưới.

## Inputs

Flag tùy chọn:

- `--strict` — coi warning là failure trong summary cuối.
- `--json` — in thêm báo cáo JSON có thể đọc bằng máy ngoài human summary.

Nếu không có flag, chạy ở standard mode.

## Các kiểm tra bắt buộc

Chạy **tất cả** check theo đúng thứ tự dưới đây và báo mỗi check là `pass`, `warn` hoặc `fail`.

1. Python runtime

- Resolve `python3` trước, sau đó `python`.
- Yêu cầu version >= 3.10.
- `fail` nếu không tìm thấy Python interpreter.
- `fail` nếu version thấp hơn 3.10.

2. Playwright cho PNG export

- Kiểm tra Playwright có import được trong active Python interpreter (`import playwright`) hay không.
- Kiểm tra Chromium đã được cài cho Playwright chưa (`playwright install --help` có mặt là đủ để xác nhận command presence; khi thực tế cho phép thì ưu tiên kiểm tra thêm browser cache).
- Nếu thiếu, đánh dấu `warn` và in **chính xác** setup hint:
  - `pip install playwright && playwright install chromium`
- Tuyệt đối không tự động cài dependency.

3. Expected script presence — chỉ maintainer-checkout mode

Xác minh các repository script sau tồn tại:

- `scripts/verify-drawio-import.py`
- `scripts/verify-mermaid-import.py`
- `scripts/verify-motion.py`
- `scripts/lint-skin.py`
- `scripts/verify-docs-sync.py`

Thiếu script là `fail` trong maintainer-checkout mode.

Trong installed-skill mode, báo rằng maintainer scripts không áp dụng; việc chúng không có mặt **không** phải warning hay failure.

4. Plugin wiring surfaces — chỉ maintainer-checkout mode

Xác minh các Claude command file tồn tại và trỏ đúng reference:

- `commands/export-diagram.md` -> `references/export.md`
- `commands/import-drawio.md` -> `references/import-drawio.md`
- `commands/import-mermaid.md` -> `references/import-mermaid.md`
- `commands/profile.md` -> `references/profiles.md`
- `commands/doctor.md` -> `references/doctor.md`

Xác minh các Pi prompt file tồn tại và trỏ đúng reference:

- `prompts/export-diagram.md` -> `references/export.md`
- `prompts/import-mermaid.md` -> `references/import-mermaid.md`
- `prompts/profile.md` -> `references/profiles.md`
- `prompts/doctor.md` -> `references/doctor.md`

- Missing file là `fail`.
- Reference routing không khớp là `fail`.
- Trong installed-skill mode, báo maintainer command/prompt wiring không áp dụng; repository routing tree thiếu hoặc chỉ có một phần không được coi là failure.

5. Các lỗi đường dẫn thường gặp

- Xác minh `SKILL.md` nằm bên dưới installation root đã resolve. Không tìm file này tương đối từ project hiện tại của người dùng và không hướng dẫn họ `cd` vào maintainer repository.
- Phát hiện rủi ro quoting đường dẫn Windows khi path có khoảng trắng nhưng command example được cung cấp không đặt path trong dấu nháy.
- Phát hiện các đường dẫn tới installed skill cục bộ không tồn tại, nếu command output có nhắc tới chúng.
- Đánh dấu các trường hợp này là `warn` và đưa ra fix suggestion cụ thể.
- Nếu `SKILL.md` ở installation root đã resolve bị thiếu, hãy đề xuất reinstall/update Diagram Design, **không** đề xuất chuyển sang một repository checkout.

## Output contract

Luôn in:

1. Một summary line ngắn:

- `Doctor summary: <PASS|WARN|FAIL> (<pass_count> pass, <warn_count> warn, <fail_count> fail)`

2. Checklist một dòng cho mỗi check:

- `[PASS] Python 3.11.9 found at ...`
- `[WARN] Playwright not installed ...`
- `[FAIL] Missing scripts/verify-docs-sync.py`

3. Chỉ có phần `Next actions` khi tồn tại `warn` hoặc `fail`.

4. Nếu có `--json`, append một JSON object gồm:

- `status`
- `counts`
- `checks[]`, mỗi phần tử có `name`, `status`, `message`, và optional `fix`
- `timestamp`

## Quy tắc an toàn và hành vi

- Chỉ diagnostic read-only: không sửa file, không cài package, không chạy destructive git command.
- Nếu command nào đó lỗi bất ngờ, capture stderr và tiếp tục các check còn lại.
- Không bao giờ nói một check đã pass nếu chưa trực tiếp xác minh trong lần chạy hiện tại.
- Ưu tiên remediation command rõ ràng, có thể copy-paste.

## Ví dụ kết quả

```text
Doctor summary: WARN (6 pass, 2 warn, 0 fail)
[PASS] Python 3.11.9 found at /usr/bin/python3
[WARN] Playwright package not found in active interpreter
[PASS] scripts/verify-drawio-import.py present
...

Next actions
- Install PNG export dependencies: pip install playwright && playwright install chromium
- Re-run: /diagram-design:doctor --strict
```
