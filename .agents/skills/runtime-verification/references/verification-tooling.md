# Verification / Tooling Failure Patterns

Prefix chính: `VERIFY-*`

Dùng khi proof phụ thuộc package-script wrapper, shell argument forwarding, test runner mode, monorepo orchestrator, cancellation hoặc cách diễn giải exit evidence.

---

## VERIFY-001 — Command thực tế khác command verification tưởng đã chạy

**Applies when**

Verification đi qua package script/wrapper như pnpm/npm/yarn/turbo hoặc test runner có watch/run mode phụ thuộc vị trí dấu `--`, argument forwarding, binary resolution hoặc filtered package execution; đặc biệt khi repo pin một package-manager version nhưng host/agent thực tế có thể chạy version/path khác.

**Symptom**

Agent/người dùng nghĩ đã chạy one-shot test nhưng runner vào watch mode, bỏ flag, chạy target khác, process không terminate như expected, hoặc command con chạy xong nhưng wrapper cuối cùng vẫn trả lỗi kiểu "command not found". Một biến thể dễ gây chẩn đoán sai là child runner đã thực sự khởi động và đang FAIL, nhưng wrapper vẫn in thêm message giống lỗi binary-resolution; message wrapper lúc này có thể chỉ là triệu chứng collateral thay vì failure độc lập.

**General root cause**

Wrapper biến đổi/forward tham số khác assumption; evidence được suy từ command nhập vào thay vì command/runner thực tế.

**Why tests miss it**

Đây chính là tầng chạy test; không có test khác tự phát hiện invocation semantics sai.

**Task-generation rule**

Khi verification phụ thuộc flag mode hoặc package filtering, task phải:
1. đọc package script thực tế;
2. đọc package-manager version được repo khai báo khi có `packageManager`/pin tương đương và đối chiếu với binary/version/path thực tế đang chạy;
3. chọn command canonical đã được package script hỗ trợ trước khi dùng direct exec;
4. xác minh argument forwarding/binary resolution trên package manager đang dùng, gồm cả child process nếu orchestrator spawn package manager lần nữa;
5. kiểm log cho thấy runner mode/target thực tế;
6. nếu child runner đã thực sự chạy nhưng FAIL và wrapper đồng thời báo lỗi resolution/command-not-found, phân loại tạm thành `INNER_RUNNER_FAILURE + POSSIBLE_WRAPPER_COLLATERAL`; sửa/rerun child failure trước khi kết luận wrapper có defect độc lập;
7. chỉ nâng thành `INDEPENDENT_WRAPPER_FAILURE` khi inner runner đã PASS hoặc không có child failure giải thích được mà canonical wrapper vẫn exit non-zero;
8. chỉ coi pass khi final wrapper exit cũng thành công, không chỉ inner runner đã in summary xanh.

**Required evidence**

Command thực tế, package-manager version/path được repo cấu hình và version/path thực tế khi có khả năng mismatch, target runner/binary được resolve, runner mode, target package, final wrapper exit code và test/file count đều khớp one-shot verification mong muốn; không còn process watch treo và không có wrapper-level failure sau khi inner runner hoàn tất. Nếu từng có wrapper error cùng lúc với child failure, evidence phải ghi rõ `INNER_RUNNER_FAILURE`, `WRAPPER_COLLATERAL_FAILURE` hoặc `INDEPENDENT_WRAPPER_FAILURE` dựa trên rerun causality; không tạo binary-resolution incident chỉ từ một message wrapper sau child failure. Direct fallback có thể là diagnostic evidence nhưng không được thay cho canonical-command PASS nếu canonical invocation vẫn lỗi.

---

## VERIFY-002 — Orchestrator cancellation bị hiểu nhầm là failure độc lập

**Applies when**

Monorepo/task runner chạy nhiều package/process song song và có fail-fast/cancel sibling behavior, hoặc concurrency tạo resource pressure như memory/file-descriptor exhaustion.

**Symptom**

Một package fail trước; sibling nhận exit code bất thường/terminated và bị báo fail dù khi chạy riêng lại pass. Hoặc root command song song OOM/panic trong runner trong khi từng package chạy riêng/serial đều sạch.

**General root cause**

Orchestrator chủ động dừng sibling sau primary failure; log tổng hợp không phân biệt root failure với collateral cancellation.

**Why tests miss it**

Nếu chỉ nhìn final failed task list/exit code, mọi task bị dừng đều trông giống failure độc lập.

**Task-generation rule**

Khi multi-task build/test fail, verification phải:
1. xác định task fail đầu tiên và log root cause;
2. phân loại task khác là PRIMARY_FAILURE, COLLATERAL_CANCELLED hoặc INDEPENDENT_FAILURE;
3. chạy riêng task collateral quan trọng nếu cần xác minh;
4. nếu primary failure là resource pressure, chạy package quan trọng riêng rồi rerun orchestrator với concurrency an toàn trước khi sửa product code;
5. chỉ tạo fix cho task có root cause độc lập.

**Required evidence**

Root failure được xác định từ log đầu tiên; task collateral chạy riêng hoặc có evidence rõ về cancellation; với resource pressure, individual/serial rerun chứng minh rule/product code sạch trước khi phân loại ENV/runner; không sửa source của sibling chỉ dựa trên exit code bị terminate.

---

## VERIFY-003 — Evidence bị stale sau khi source/config/artifact thay đổi

**Applies when**

Một gate đã PASS, sau đó source code, config, test harness hoặc generated artifact liên quan bị sửa trước khi feature/release được chốt; hoặc source/working tree thay đổi ngay trong khi verification đang chạy.

**Symptom**

Agent giữ trạng thái PASS cũ dù HEAD hiện tại khác revision đã được verify; nói "tests đã pass trước đó" sau khi refactor phần được gate bao phủ; hoặc long-running watcher/generator bắt đầu ở clean revision nhưng source đổi giữa command làm output/evidence bị contaminated.

**General root cause**

Evidence không được gắn với revision/dependency scope; verification được xem như trạng thái vĩnh viễn thay vì proof của một snapshot cụ thể.

**Why tests miss it**

Bản thân test chỉ chứng minh revision lúc nó chạy. Không có cơ chế tự động biết source đã đổi sau đó nếu workflow không theo dõi provenance/hash/dependency.

**Task-generation rule**

Khi pattern áp dụng:
1. ghi revision/working-tree state của evidence;
2. sau mỗi mutation, xác định gate nào bị ảnh hưởng;
3. chuyển evidence liên quan về STALE/PENDING;
4. rerun gate bị ảnh hưởng và aggregate gate phụ thuộc nó;
5. với long-running runtime/generator, snapshot revision + working-tree state trước và sau proof; nếu source đổi giữa run thì đánh dấu evidence/artifact CONTAMINATED/STALE và rerun từ stable checkout;
6. cho phép giữ PASS của gate độc lập khi có bằng chứng dependency của gate đó không đổi.

**Required evidence**

Final completion phải chỉ dựa trên proof còn hiệu lực ở revision cuối. Mỗi PASS quan trọng có provenance đủ để xác định source/config/artifact nó bao phủ; không dùng PASS của revision cũ cho phần đã đổi.

---

## VERIFY-004 — Exit code xanh nhưng verification có unexpected runtime/test warning

**Applies when**

Test/build/smoke command có thể exit 0 trong khi console/log xuất hiện warning tại runtime boundary như unhandled network request, hydration mismatch, accessibility/semantic violation, missing provider/runtime dependency, timezone/environment fallback hoặc unexpected mock fallthrough.

**Symptom**

Suite summary xanh nhưng log có warning cho thấy test harness/runtime không phản ánh interaction mong muốn; warning có thể báo request không được mock, semantic role sai hoặc một dependency đang rơi sang behavior ngoài dự kiến.

**General root cause**

Workflow coi exit code là evidence duy nhất và không phân loại warning theo ý nghĩa; test framework thường không fail mặc định với nhiều warning quan trọng.

**Why tests miss it**

Warning không nhất thiết throw/assert fail. Một test vẫn có thể đạt assertion hẹp trong khi boundary khác đang bị bỏ qua hoặc render sai semantics.

**Task-generation rule**

Khi pattern áp dụng, verification phải phân loại warning thành:
- `EXPECTED/KNOWN`: có lý do và owner rõ;
- `UNEXPECTED`: phải fix, thêm handler/assertion, hoặc ghi BLOCKED nếu chưa xác định được.
Không nâng gate thành "clean PASS" khi còn unexpected warning thuộc runtime/test boundary.

**Required evidence**

Command exit 0, expected assertions pass và log không còn unexpected runtime/test warning thuộc phạm vi gate. Warning deprecation/tooling không ảnh hưởng behavior có thể được ghi tech debt riêng thay vì chặn gate.


---

## VERIFY-005 — DOM test simulation lệch interaction thật của controlled/third-party form primitive

**Applies when**

Frontend dùng controlled input, React Hook Form/Formik hoặc component primitive của thư viện như Base UI/Radix/custom Select/MoneyInput/Dialog, và unit/integration test chạy trong jsdom/happy-dom bằng synthetic event helpers; primitive có thể có portal/inert lifecycle hoặc disabled/accessibility semantics riêng.

**Symptom**

DOM value nhìn như đã đổi nhưng form state/validation/mutation payload không đổi; `fireEvent.change` làm input hiển thị giá trị mới nhưng RHF không nhận; role/label query không tìm thấy trigger vì control thực tế là button/combobox hoặc accessible name có required marker/extra text; query như `getByRole('alert')` fail vì nhiều semantic error cùng tồn tại; mock mutation gọi `onError/onSuccess` ở timing khác runtime thật nên RHF state bị ghi đè hoặc mutation tưởng như không chạy; test fail trong jsdom nhưng browser interaction tương ứng hoạt động.

**General root cause**

Test harness mô phỏng một DOM event/lifecycle hẹp thay vì chuỗi interaction mà component library/controlled state thực sự dựa vào; abstraction của third-party primitive có event/role/focus semantics khác native control mà test đang giả định; query/assertion cũng có thể giả định accessible name hoặc role là duy nhất dù DOM hợp lệ có nhiều phần tử cùng semantics.

**Why tests miss it**

Assertion chỉ nhìn DOM value hoặc text có thể bỏ sót form state và mutation payload; ngược lại jsdom có thể fail vì event model không đủ gần browser dù product runtime đúng.

**Task-generation rule**

Khi pattern áp dụng:
1. ưu tiên user-level interaction như `userEvent` hoặc helper chính thức của component library cho text/custom controls;
2. query control theo accessible role/name/semantics thực tế thay vì exact rendered label text hoặc giả định native-label trên polymorphic trigger;
3. nếu một role hợp lệ có thể xuất hiện nhiều lần như `alert`, scope bằng region/form/container hoặc assert đúng text/name thay vì giả định global uniqueness;
4. mock mutation/callback phải giữ lifecycle gần runtime thật: submit hoàn tất trước khi phát `onError/onSuccess`, và assertion phải chờ state transition có ý nghĩa thay vì chỉ queue callback tùy ý;
5. kiểm đồng thời DOM value, form/validation state và mutation/request payload cho interaction quan trọng;
6. giữ browser smoke/E2E cho primitive có behavior phụ thuộc focus/portal/keyboard/browser;
7. với disabled/polymorphic control, xác minh native/ARIA semantics thực thay vì chỉ data attribute; với dialog/portal, verify close/focus/inert trên browser khi critical;
8. nếu jsdom fail nhưng browser pass, phân loại test-harness mismatch trước khi sửa business logic hoặc API semantics.

**Required evidence**

Interaction test chứng minh giá trị hiển thị, form state/validation và mutation/request payload cùng thay đổi đúng; accessible role/name phản ánh control thực tế; mutation mock/callback không chạy trước lifecycle submit thực tế; assertion được scope đúng khi role không unique; với interaction browser-sensitive, browser smoke/E2E tương ứng pass. Không coi chỉ DOM value đổi là đủ proof và không coi jsdom-only failure là product-runtime failure nếu chưa reproduce trên browser.


---

## VERIFY-006 — Test rerender làm mất provider/context và tạo false state-reset failure

**Applies when**

Frontend test dùng helper bọc component bằng QueryClientProvider, Router, i18n/store/theme/form provider hoặc context tương tự, rồi gọi `rerender()` để mô phỏng locale/config/prop change mà kỳ vọng component state/draft được giữ.

**Symptom**

Initial render đúng nhưng sau `rerender(<Component />)` provider biến mất hoặc instance provider mới được tạo; component remount/reset, unsaved form/date/payment state quay về initial fixture, query cache/router context biến mất và test báo state-preservation failure dù browser runtime giữ state đúng.

**General root cause**

Custom render helper chỉ bọc provider ở lần render đầu nhưng trả thẳng Testing Library `rerender`; lần rerender không đi qua cùng wrapper/provider instance hoặc wrapper factory tạo dependency mới.

**Why tests miss it**

Component/unit test chỉ nhìn state sau rerender và dễ quy lỗi cho feature logic. Browser runtime thường không tháo toàn bộ provider tree khi đổi locale/prop, nên cùng flow có thể pass trên browser.

**Task-generation rule**

Khi test cần state preservation qua rerender:
1. custom render helper phải dùng Testing Library `wrapper` hoặc custom rerender bảo đảm provider tree được giữ;
2. stateful provider quan trọng như QueryClient/store/router phải giữ cùng instance trừ khi test cố ý reset;
3. phân biệt rerender với unmount/remount trong assertion và test naming;
4. khi failure chỉ xuất hiện sau test rerender, kiểm provider identity trước khi sửa production state logic;
5. browser smoke nên cover user-facing state preservation quan trọng như locale switch hoặc responsive/config change.

**Required evidence**

Rerender đi qua cùng provider tree và cùng stateful provider instance theo contract; unsaved state/query/router context được giữ khi feature yêu cầu; test chỉ reset khi có explicit remount/reset action. Nếu browser pass nhưng test rerender reset, phải chứng minh provider identity trước khi kết luận product bug.

---

## VERIFY-007 — Responsive DOM trong jsdom bị đếm như nhiều UI cùng hiển thị

**Applies when**

Component render đồng thời desktop/mobile hoặc breakpoint-specific branches và dùng CSS media utilities như `hidden md:block`, trong khi unit/integration test chạy trong jsdom/happy-dom không thực thi layout/media-query visibility như browser thật.

**Symptom**

`getAllByText`/global role query thấy duplicate item gấp đôi, ví dụ hai record xuất hiện bốn lần vì desktop table và mobile cards đều có trong DOM; assertion count fail dù browser tại một viewport chỉ hiển thị một branch.

**General root cause**

Test suy visible UI từ DOM presence trong environment không có layout engine/media-query behavior đầy đủ. Responsive CSS ẩn branch ở browser nhưng jsdom vẫn expose cả hai subtrees cho query.

**Why tests miss it**

Snapshot/DOM query không biết phần tử nào thực sự visible theo breakpoint; browser E2E thường pass vì viewport/CSS engine áp dụng visibility thật.

**Task-generation rule**

Khi component có responsive duplicate representation:
1. unit test phải scope assertion vào semantic container/region cụ thể bằng `within()` thay vì global count;
2. không dùng global duplicate count làm proof cho visible item count nếu cùng data render ở nhiều responsive branches;
3. browser/visual test phải kiểm visibility, overflow và interaction tại viewport đại diện;
4. nếu cần unit-test breakpoint logic thật, dùng explicit media-query abstraction/mocking thay vì giả định jsdom CSS visibility;
5. không xóa một responsive branch chỉ để làm global query unique.

**Required evidence**

Unit assertion được scope vào đúng representation/container; browser viewport evidence chứng minh branch mong muốn visible và branch còn lại không gây duplicate interaction; count/interaction semantics đúng ở desktop và mobile.


---

## VERIFY-008 — Test setup/precondition failure bị che bởi downstream symptom

**Applies when**

E2E/unit/integration helper tạo prerequisite theo chuỗi như register → login, seed → mutate, create entity → lifecycle action, nhưng helper không assert ngay status/invariant của bước setup.

**Symptom**

Bước sau báo lỗi dễ gây chẩn đoán sai, ví dụ login 401 dù registration trước đó thực ra bị validation reject, hoặc close/update test fail vì fixture đã vi phạm invariant từ lúc tạo.

**General root cause**

Setup được coi là plumbing “chắc chắn thành công”; failure của prerequisite không fail fast nên symptom trôi xuống boundary khác và bị quy nhầm cho auth/product/service đang test.

**Why tests miss it**

Helper thường bỏ qua response status/body của setup để giảm boilerplate; fixture dùng literal có thể drift khỏi validation/business rule mới mà compiler không biết.

**Task-generation rule**

Khi pattern áp dụng:
1. mỗi setup prerequisite có failure mode phải assert status/result/invariant ngay tại bước tạo;
2. fixture phải thỏa domain invariant cần thiết cho action đang test;
3. helper auth/seed/create phải fail fast với response/body đủ chẩn đoán;
4. khi downstream fail, inspect setup chain trước khi sửa boundary downstream;
5. không nới business invariant chỉ để fixture cũ pass.

**Required evidence**

Setup steps đều có explicit success assertion; fixture invariant được chứng minh; downstream action chỉ chạy sau prerequisite pass; khi cố tình làm setup invalid, test fail tại đúng setup boundary thay vì symptom muộn.

---

## VERIFY-009 — Test harness drift hoặc mutable mock leak tạo false product regression

**Applies when**

Frontend/unit/browser tests dùng partial module mocks, mutable mock implementation/state, terminal state injection hoặc shared journey/helper chứa nhiều assertion/prerequisite hơn acceptance đang verify; production component/hook dependencies và shared helper scope thay đổi theo thời gian.

**Symptom**

Test fail trước interaction đầu tiên vì mock thiếu export mới; test sau nhận behavior/onSuccess của test trước; terminal sync/error state được set trực tiếp nhưng state machine chưa đi qua action gây ra nó; hoặc browser journey fail ở unrelated assertion của shared helper trước khi tới business step mà task yêu cầu.

**General root cause**

Harness không mirror dependency surface hiện tại hoặc mutable mock state không được reset/isolate; test mô phỏng kết quả cuối mà bỏ qua causal transition của product lifecycle; shared helper conflates nhiều acceptance surface nên behavior không thuộc task trở thành prerequisite bắt buộc.

**Why tests miss it**

Mỗi test nhìn riêng có fixture hợp lý; partial mock compile/runtime chỉ fail khi component consume export mới; order-dependent leak có thể chỉ xuất hiện khi chạy suite đầy đủ; helper reuse nhìn có vẻ DRY nhưng có thể che việc journey đang fail trước target boundary.

**Task-generation rule**

Khi pattern áp dụng:
1. reset mutable mocks/state trong beforeEach hoặc tạo fixture instance mới;
2. partial module mock phải cung cấp mọi export path component thực sự consume, ưu tiên importActual + override hẹp khi phù hợp;
3. assertion cho sync/success/error phải đi qua action/transition gây ra state thay vì set terminal state tùy ý;
4. failure trước first product interaction phải được phân loại harness/setup trước;
5. chạy cả test file/suite, không chỉ isolated case, để phát hiện order-dependent leak;
6. shared helper phải parameterize/opt-out assertion ngoài acceptance của caller; mỗi critical assertion nên trace được về task/requirement hoặc nằm trong suite chuyên trách riêng;
7. khi journey fail trước target business interaction, phân loại setup/helper scope trước product regression.

**Required evidence**

Test file chạy deterministic độc lập và trong suite; không thiếu consumed export; mock implementation/state không leak giữa cases; success/error/sync UI chỉ xuất hiện sau causal action tương ứng; targeted browser journey tới được boundary nghiệp vụ cần verify mà không bị unrelated helper assertion chặn; browser/product logic không bị sửa chỉ để bù harness drift.


---

## VERIFY-010 — Verification tool auto-parallelism gây OOM hoặc false infrastructure failure

**Applies when**

Lint/test/build/analysis tool tự chọn số worker/thread theo CPU và chạy trên máy local/CI có giới hạn memory, file descriptor hoặc native allocator thấp hơn mức parallelism mặc định.

**Symptom**

Verification fail bằng OOM, allocator panic, worker crash, random process termination hoặc exit non-zero trước khi báo lỗi source có ý nghĩa; cùng code có thể pass khi chạy ít worker hơn.

**General root cause**

Runner tối ưu throughput theo CPU concurrency nhưng resource bottleneck thực tế là RAM/native allocator/OS limit. Workflow hiểu infrastructure exhaustion như product/lint/test failure thay vì xác minh lại với bounded concurrency.

**Why tests miss it**

Đây là failure của chính verification runtime; source diagnostics có thể chưa kịp chạy. Máy mạnh hoặc CI khác không reproduce nên lỗi trông nondeterministic.

**Task-generation rule**

Khi tool hỗ trợ worker/thread control và failure có dấu hiệu resource exhaustion:
1. ghi command, target, OS/runtime và failure signature trước khi đổi source;
2. rerun cùng target với bounded concurrency chính thức của tool, ưu tiên giá trị nhỏ như 1 khi cần chẩn đoán;
3. nếu bounded run cho diagnostics source thật, xử lý diagnostics đó bình thường; nếu bounded run sạch, phân loại incident ban đầu là environment/runner capacity;
4. khi repo thường xuyên chạy trên environment đó, pin canonical lint/test/build command về concurrency ổn định thay vì dùng workaround ad-hoc;
5. không tắt rule/test hoặc tăng memory mù quáng trước khi phân biệt source failure và runner exhaustion.

**Required evidence**

Canonical bounded-concurrency command chạy tới completion trên target environment; exit/result diagnostics có ý nghĩa; nếu run ban đầu OOM nhưng bounded run pass thì ghi rõ causality là verification infrastructure, không phải product regression. Repo script/CI phải phản ánh concurrency đã verify nếu đây là constraint ổn định.
