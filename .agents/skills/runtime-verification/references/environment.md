# Environment / Startup Failure Patterns

Prefix chính: `ENV-*`, `STARTUP-*`

Dùng cho failure pattern liên quan env var, port, runtime config, base URL, process startup, readiness, dependency boot order hoặc native runtime dependency.

---

## ENV-001 — Setup/install script ghi đè environment đang dùng được

**Applies when**

Repo có script setup/prepare/install/bootstrap hoặc package lifecycle như `postinstall`/`prepare` có thể tạo hay sửa `.env`, config local hoặc secret placeholder từ file example/template.

**Symptom**

Một command cài dependency/setup tưởng như không liên quan làm app/database/E2E đang chạy được chuyển sang lỗi auth, connection, base URL hoặc credential ngay sau đó.

**General root cause**

Bootstrap dùng copy/overwrite không phân biệt file đích đã tồn tại, nên environment local hợp lệ bị thay bằng giá trị example/default.

**Why tests miss it**

Unit/typecheck không chạy lifecycle install/setup; lỗi chỉ xuất hiện sau một command có side effect và thường bị hiểu nhầm là regression nghiệp vụ.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. mặc định `create-if-missing`, không overwrite environment đã tồn tại;
2. nếu cần reset, dùng explicit force/reset command;
3. coi install/setup là potentially mutating cho tới khi đã đọc lifecycle scripts liên quan;
4. verification phải snapshot/kiểm tra các env/config quan trọng trước và sau install/setup;
5. chạy một smoke check phụ thuộc env sau bootstrap.

**Required evidence**

Install/setup chạy mà file environment hiện hữu vẫn giữ nguyên giá trị mong muốn; app/database smoke check sau setup dùng đúng config.

---

## ENV-002 — Native dependency không tương thích runtime/OS hoặc payload/cache native hỏng

**Applies when**

Runtime/build dùng package có native addon/platform binary, đặc biệt khi package manager cài optional platform dependencies hoặc toolchain phụ thuộc Node/OS/architecture cụ thể.

**Symptom**

Build/start/import fail với lỗi như `Failed to load native binding`, `MODULE_NOT_FOUND` cho file `.node`, ABI mismatch, hoặc cache native không materialize/load được.

**General root cause**

Native binary phù hợp platform/runtime không được cài, package/version kéo binary không tương thích, install script bị chặn, hoặc native cache/payload/permission bị hỏng.

**Why tests miss it**

Typecheck, unit test và frontend test thuần JS/TS có thể pass mà không import code path native dùng lúc production build/plugin bootstrap trên target OS.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. có smoke import hoặc production build cho package/plugin native trên target OS/runtime thực tế;
2. kiểm package-manager policy đối với optional/build scripts;
3. khi lỗi, xác định package/version native cụ thể trước khi đổi code nghiệp vụ;
4. ưu tiên version pin/compatible runtime hoặc reinstall native payload có kiểm chứng; không coi downgrade ngẫu nhiên là fix nếu chưa xác nhận root cause.

**Required evidence**

Native package/plugin import được trên target runtime và production build/start dùng code path đó pass. Nếu fix bằng pin version, lockfile phải phản ánh version đã verify.

---

## ENV-003 — Verification giả định path separator của một hệ điều hành

**Applies when**

Test/script/architecture check so sánh filesystem path dạng string hoặc dùng glob/path normalization xuyên Windows và POSIX.

**Symptom**

Check pass trên Linux/macOS nhưng fail trên Windows với `\\` vs `/`, hoặc ngược lại, dù file/module đúng.

**General root cause**

Verification so raw path string thay vì normalize bằng API path/platform-neutral representation; hoặc workflow sinh shell/script cho OS đích bằng cách flatten cấu trúc block thành chuỗi separator tùy tiện, làm cú pháp hợp lệ trên giấy trở thành invalid program trên shell thật.

**Why tests miss it**

CI/dev chỉ chạy trên một OS nên assumption không lộ ra cho đến khi workflow chạy ở OS khác.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. normalize path trước khi so sánh hoặc dùng API/path matcher platform-neutral;
2. thêm ít nhất một assertion không phụ thuộc separator;
3. với generated shell/script, bảo toàn syntax structure của shell đích; không ghép block/object/multiline program bằng separator tùy ý chỉ vì command đơn lẻ có thể join bằng separator;
4. smoke syntax/execute script trên shell/OS đích trước khi dùng output làm runtime evidence.

**Required evidence**

Verification pass với path đã normalize trên target OS; không còn hard-coded separator trong invariant cross-platform liên quan; generated shell/script parse và chạy thành công trên shell đích, trả output machine-readable mong đợi khi workflow phụ thuộc output đó.

---

## ENV-004 — Dependency install/relink làm biến đổi verification environment ngoài scope dự kiến

**Applies when**

Verification cần cài/thêm/cập nhật dependency, relink workspace/node_modules hoặc regenerate lockfile trước khi test/build/browser runner có thể chạy.

**Symptom**

Một install tưởng chỉ thêm một dependency lại purge/relink `node_modules`, làm local binary tạm thời biến mất, chạy lifecycle ngoài dự kiến, hoặc tạo lockfile diff lớn chứa nhiều peer/transitive resolution không trực tiếp thuộc dependency được yêu cầu; install dở dang khiến verification command sau đó hỏng theo cách mới.

**General root cause**

Workflow coi install/relink là thao tác hẹp/read-only đối với môi trường verification, trong khi package manager có thể chạy lifecycle, thay graph resolution, relink executable và rewrite lockfile phụ thuộc version/config hiện tại.

**Why tests miss it**

Failure xảy ra trước hoặc giữa lúc test runner được materialize. Unit/typecheck hiện có không chứng minh môi trường sau install vẫn tương đương môi trường trước đó.

**Task-generation rule**

Khi pattern áp dụng:
1. snapshot `git status/diff` và các config/env quan trọng trước install;
2. xác minh package-manager version/config đúng repo trước khi mutate dependency graph;
3. chỉ coi install hoàn tất khi command exit thành công;
4. review manifest + lockfile diff theo scope dependency mong muốn; diff transitive lớn phải được giải thích, không tự động coi là lỗi nhưng cũng không được bỏ qua;
5. xác minh target executable/`.bin` hoặc runner cần thiết tồn tại sau relink;
6. chạy canonical verification command sau install để chứng minh environment mới usable;
7. nếu install bị dừng/fail, coi environment là potentially dirty cho tới khi integrity được xác minh lại.

**Required evidence**

Pre/post working-tree state được ghi nhận, install/relink exit thành công, manifest/lockfile diff được review và có nguyên nhân hợp lý, target runner resolve được sau install, env/config quan trọng không bị thay đổi ngoài dự kiến và canonical verification command có thể chạy trên environment sau mutation.

---

## ENV-005 — OS file lock chặn checkout hoặc cleanup của verification runner

**Applies when**

Workflow chạy trên hệ điều hành có file-lock semantics chặt (đặc biệt Windows), trong khi editor, dev server, browser runner, report viewer, antivirus/indexer hoặc process stale có thể giữ handle trên source file hay artifact mà Git/test runner cần replace/delete.

**Symptom**

Git pull/checkout báo `unable to unlink old ...`, `Invalid argument` hoặc tương tự; test runner fail trước khi collect/run test với `EPERM: operation not permitted, unlink ...`, thường tại output/cache như `test-results/.last-run.json`. Nhiều lỗi có thể xuất hiện liên tiếp nhưng đều xảy ra trước product runtime.

**General root cause**

Một process ngoài command verification vẫn giữ file handle, hoặc runner cố dọn output directory cũ đang bị khóa. Source checkout có thể bị partial/stale nếu file code không replace được; runner cleanup có thể fail trước test collection.

**Why tests miss it**

Không có test nào chạy được khi cleanup fail; unit/typecheck trước đó cũng không chứng minh local checkout hiện tại khớp target revision. Log dễ bị hiểu nhầm thành product/browser failure dù lỗi xảy ra ở filesystem boundary.

**Task-generation rule**

Khi pattern áp dụng:
1. phân loại incident là environment/tooling BLOCKED nếu runner chưa collect test; không ghi browser/product FAIL;
2. xác minh local revision và file freshness sau mọi `unable to unlink` bằng `git status`, `git rev-parse HEAD` và diff/compare với target remote trước khi chạy lại;
3. xác định process giữ handle (dev server, Playwright/report viewer, editor extension, antivirus/indexer hoặc process stale) và dừng đúng process khi có thể; tránh kill toàn bộ process không liên quan;
4. với artifact output bị khóa nhưng source checkout đã xác minh fresh, có thể dùng output directory mới/unique làm diagnostic hoặc rerun; không dùng output-dir bypass để che source file vẫn stale;
5. sau khi unlock, chạy lại canonical checkout/verification command từ đầu và ghi final exit/test count;
6. nếu lock tái diễn, cấu hình runner để tách output/report khỏi file được viewer/process khác giữ hoặc bổ sung cleanup ownership rõ ràng.

**Required evidence**

Target source revision được materialize đầy đủ sau checkout, không còn unresolved/stale file do unlink failure; canonical runner bắt đầu collect/run test thay vì fail tại filesystem cleanup; final evidence ghi command, revision, output directory và test count/exit. Nếu dùng fresh `--output` chỉ để chẩn đoán, phải chứng minh source checkout đã fresh trước và vẫn rerun canonical path sau khi lock được xử lý.

---

## STARTUP-001 — Port conflict làm verification nói chuyện với stale/wrong process

**Applies when**

Generator, smoke test hoặc frontend gọi service qua fixed port/base URL và workflow có thể còn process cũ đang listen.

**Symptom**

Process mới báo `EADDRINUSE`/không start, nhưng generator/request vẫn “thành công”; output lại phản ánh schema/behavior cũ hoặc revision khác.

**General root cause**

Verification chỉ kiểm endpoint reachable, không xác minh process vừa start chính là process/revision mong muốn; hoặc dùng freshness marker có thể tự thay đổi bởi command verification/read-only khác (ví dụ metadata/index mtime bị refresh), tạo false stale/false fresh khi nhiều worker chạy song song.

**Why tests miss it**

Endpoint health vẫn xanh vì stale process; generator không biết source runtime sai revision.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. kiểm tra port/process trước start;
2. fail fast nếu process mới không bind/start;
3. probe capability/version/schema đại diện cho revision mới;
4. coi generic health/readiness endpoint là supporting evidence, không thay capability-specific probe; nếu health phụ thuộc database/external service không liên quan capability đang verify thì phải phân loại failure đó riêng;
5. freshness marker phải gắn với checkout/revision movement hoặc explicit runtime revision token và phải ổn định trước các command read-only/parallel worker; không dùng marker có thể bị chính verification refresh;
6. chỉ sau đó mới chạy generator/smoke flow phụ thuộc endpoint;
7. nếu có stale process, dừng/đổi port rõ ràng thay vì tiếp tục.

**Required evidence**

Process target start thành công trên expected port và đúng runtime identity/revision, freshness marker không thay đổi giả do chính verification/parallel worker, capability-specific probe trả behavior/schema mong đợi, rồi dependent generator/smoke check mới pass. Generic `/health` xanh hoặc đỏ một mình không đủ để chứng minh capability target ready hoặc broken khi endpoint đó bao gồm dependency ngoài scope.
