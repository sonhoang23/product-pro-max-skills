---
name: "runtime-verification"
description: >-
  Phân tích và phòng ngừa các lỗi runtime có thể tái diễn khi vibe coding. Dùng khi tạo task trước implementation,
  khi test/lint/typecheck đã pass nhưng app chạy thật vẫn lỗi, khi gặp 404/401 hoặc lỗi routing/auth/API/database/
  environment/browser/worker tương tự, khi cần phân loại Runtime Lesson Candidate, cập nhật failure pattern về
  canonical repo oh-my-skill, hoặc sync runtime-verification từ upstream về repo hiện tại.
compatibility: "Dùng được độc lập hoặc được gọi từ SpecKit; không yêu cầu một framework cụ thể."
metadata:
  author: "sonhoang23"
  source: "github"
  canonical_repo: "sonhoang23/oh-my-skill"
  canonical_branch: "main"
  canonical_path: "skills/runtime-verification"
  version: "1.12.0"
---

# Runtime Verification

## Mục tiêu

Biến các lỗi kiểu “code/test pass nhưng chạy thật vẫn hỏng” thành knowledge có thể tái sử dụng và thành nghĩa vụ task **trước khi implementation bắt đầu**.

Skill này **không phải một phase SpecKit mới** và không tự chạy toàn bộ hệ thống. Nó là cross-cutting prevention/knowledge engine chạy theo độ trưởng thành của feature để:
- dịch trái (shift-left) lesson runtime thành requirement/clarification khi behavior đã đủ tín hiệu;
- nhận diện runtime boundary và chốt prevention design khi technical architecture đã rõ;
- đối chiếu failure catalog bằng Progressive Disclosure, không quét mù toàn catalog ở mọi bước;
- trả output theo lifecycle mode với traceability xuyên `Risk → Requirement → Design → Task → Evidence`;
- mô tả preventive/verification obligation đủ cụ thể để task generator và implementation gate thực thi mà không phải suy lại failure semantics.

## Canonical upstream

Nguồn chuẩn duy nhất của skill này là:

- repo: `sonhoang23/oh-my-skill`
- branch: `main`
- path: `skills/runtime-verification`
- manifest: `skills/runtime-verification/manifest.json`

Mọi bản cài trong repo khác như `.agents/skills/runtime-verification/` là **consumer copy**, không phải source of truth.

Repo consumer MAY phát hiện Runtime Lesson Candidate, nhưng reusable knowledge MUST được promote về canonical upstream trước. Không duy trì hai catalog độc lập.

Nếu người dùng đã cho phép cập nhật trực tiếp upstream, promotion MUST commit thẳng vào `oh-my-skill/main`; không tạo branch/PR trung gian.

Nếu canonical manifest đặt `learning.promotion = direct-to-main` và agent có quyền ghi canonical repo, không hỏi lại về branch/PR. Nếu không có quyền ghi upstream, trạng thái promotion là `BLOCKED`: báo rõ lý do và **không** fallback sang sửa consumer copy như source of truth.

## Khi nào dùng

- **requirements mode**: `speckit-specify-vi` và `speckit-clarify-vi` dùng để phát hiện known-failure signal có thể chuyển thành behavior/acceptance/edge-case mà không kéo implementation detail vào spec.
- **design mode**: `speckit-plan-vi` dùng **BẮT BUỘC** để tạo Runtime Risk Design authoritative đầu tiên; `speckit-checklist-vi` dùng output này để kiểm chất lượng requirement.
- **tasks mode**: `speckit-tasks-vi` dùng **BẮT BUỘC** để refresh design inventory và map risk → task; `speckit-analyze-vi` dùng độc lập để audit coverage.
- **implementation mode**: `speckit-implement-vi` chỉ nạp risk/task liên quan, kiểm prevention design và evidence; không tự mở rộng scope bằng cách quét lại toàn catalog.
- **audit mode**: `speckit-converge-vi` kiểm false-N/A, missing coverage, stale evidence và nhận diện Runtime Lesson Candidate mới.
- `speckit-system-modeling-vi` **không dùng catalog làm source of truth**; nó chỉ visualize runtime-sensitive semantics đã tồn tại trong artifact có thẩm quyền.
- `speckit-constitution-vi` chỉ tham khảo lifecycle policy ở mức governance; không copy Risk ID/pattern cụ thể vào constitution.
- `speckit-taskstoissues-vi` không re-evaluate catalog; chỉ bảo toàn Risk ID/traceability đã có trong task.

## Lifecycle modes

Caller SHOULD truyền mode rõ ràng. Caller cũ không truyền mode mặc định **`tasks`** để backward compatible với contract trước 1.10.0.

### 1. `requirements`

Mục tiêu: ngăn known failure ngay ở requirement mà không quyết định implementation.

Output **Runtime Requirement Signals**:
- `Risk ID`
- `Signal status`: `SIGNAL | NOT_APPLICABLE | DEFERRED | NEEDS_UPSTREAM`
- `Evidence`
- `Requirement implication`
- `Requirement/AC/edge-case ref` nếu đã materialize vào spec
- `Disposition`: xử lý trong spec/clarify hay defer sang design

Quy tắc:
- Chỉ pattern có `Earliest detectable stage = requirements` mới tạo signal trực tiếp.
- Pattern stage sau phải `DEFERRED`; không kéo browser executable, cache library, migration tooling, runner command hoặc implementation detail vào spec.
- Requirement implication phải technology-agnostic và mô tả user-visible/domain behavior, acceptance, recovery, permission, lifecycle hoặc quality expectation.
- Nếu signal làm lộ ambiguity có hệ quả behavior khác nhau, `clarify` ưu tiên hỏi; nếu chỉ là technical choice, defer sang plan.

### 2. `design`

Mục tiêu: chốt risk kỹ thuật sau khi architecture/integration đã đủ rõ.

Output **Runtime Risk Design**:
- `Risk ID`
- `Status`: `APPLIES | NOT_APPLICABLE | NEEDS_UPSTREAM`
- `Requirement refs`
- `Evidence/trigger`
- `Failure mode`
- `Prevention design obligation`
- `Verification strategy`

Đây là inventory authoritative đầu tiên cho feature mới. `NEEDS_UPSTREAM` nghĩa là spec/requirement/contract có thẩm quyền còn thiếu; không tự phát minh behavior trong plan.

### 3. `tasks`

Mục tiêu: chuyển Runtime Risk Design thành delivery obligation.

Output giữ status design và bổ sung:
- `Task obligation`
- `Placement`
- `Task IDs`
- `Required evidence`

Feature legacy chưa có Runtime Risk Design trong `plan.md` MAY bootstrap bằng design evaluation read-only để backward compatible; phải đánh dấu `legacy-bootstrap`.

### 4. `implementation`

Mục tiêu: thực thi đúng prevention design và thu evidence đúng boundary. Không re-scan toàn catalog; chỉ nạp Risk ID được task/plan tham chiếu.

Evidence: `PASS | FAIL | BLOCKED | STALE | CONTAMINATED`.

Nếu implementation cần đổi intended behavior/design để xử lý risk, quay lại artifact có thẩm quyền trước; không dùng code để âm thầm rewrite semantics.

### 5. `audit`

Kiểm tối thiểu false-N/A, missing trace, prevention-design drift, evidence BLOCKED/STALE/CONTAMINATED bị coi nhầm PASS và Runtime Lesson Candidate mới.

## Authority và traceability

Runtime verification là **knowledge/checking layer**, không chen vào authority chain:

```text
constitution
  > spec.md
    > plan.md + technical design artifacts
      > tasks.md
        > implementation state
```

Traceability mục tiêu:

```text
Risk ID
  → Requirement / Acceptance / Edge case
    → Prevention design
      → Task
        → Runtime evidence
```

Risk thuần tooling/environment có thể bắt đầu từ plan/tasks theo `Earliest detectable stage`, không cần tạo requirement giả.

## Input tối thiểu

Ưu tiên theo Progressive Disclosure:
1. `spec.md`: user story, acceptance, non-goal, boundary người dùng.
2. `plan.md`: architecture, app/service, runtime, auth, integration, deployment assumptions.
3. Khi liên quan: `contracts/`, `data-model.md`, `quickstart.md`, project-level docs current-state.
4. Lifecycle router: đọc `references/lifecycle-profile.md` để lọc pattern theo stage trước.
5. Catalog router: đọc `references/catalog-index.md`, sau đó chỉ mở đúng category file/pattern tương ứng; không nạp toàn bộ catalog.

Không suy behavior runtime từ boilerplate hoặc convention nếu artifact có thẩm quyền chưa quyết định điều đó. `requirements` mode không được kéo technical prevention xuống spec; `design` mode không được thay đổi business semantics đã chốt.

## Quy trình

### 1. Xác định runtime surface

Kiểm tra feature có tạo/thay đổi các boundary sau hay không:
- frontend deployable, base URL, entry route, deep link;
- authentication/session/cookie/token và protected API;
- frontend ↔ API hoặc service ↔ service;
- environment/config/port/base URL/CORS;
- database migration/schema/seed cần cho luồng chạy thật;
- browser-only behavior, hydration, asset, offline/runtime dependency;
- queue/worker/background job;
- file/object storage hoặc external dependency;
- startup/readiness/health behavior của process;
- generated artifact/contract phụ thuộc runtime đang chạy như OpenAPI client types, SDK hoặc schema snapshot;
- user-visible write lifecycle và query/cache/read-model convergence sau mutation;
- entity-facing selector/list/pagination/search/editability có behavior chỉ lộ khi data async, dataset lớn hoặc lifecycle/history thay đổi;
- modal/focus/inert, responsive/mobile và accessibility semantics của headless/polymorphic UI primitive;
- verification tooling/orchestrator/test runner khi command wrapper, watch mode hoặc cancellation có thể làm sai nghĩa evidence.

Chỉ chọn surface thực sự xuất hiện trong spec/plan; không tạo risk chỉ vì stack có khả năng hỗ trợ nó.

### 2. Match failure pattern

Với mỗi surface, dùng `catalog-index.md` để chọn category file, rồi chỉ đọc các pattern trong category đó có điều kiện áp dụng tương ứng và xác định:
- `APPLIES`: điều kiện áp dụng có bằng chứng trong artifact.
- `NOT_APPLICABLE`: không có boundary/condition tương ứng; phải có lý do ngắn.
- `NEEDS_UPSTREAM`: cần một quyết định thuộc spec/plan/contract nhưng artifact hiện tại chưa đủ để xác định behavior đúng; không được đoán.

### 3. Tạo Runtime Risk Inventory

Mỗi risk trả tối thiểu:

| Field | Ý nghĩa |
|---|---|
| Risk ID | ID ổn định từ failure catalog |
| Status | APPLIES / NOT_APPLICABLE / NEEDS_UPSTREAM |
| Evidence | Artifact/boundary khiến risk áp dụng hoặc không áp dụng |
| Failure mode | Hệ thống có thể hỏng theo cách nào |
| Task obligation | Việc preventive/verification cần có trong tasks |
| Placement | Phase/story nơi risk được tạo ra |
| Required evidence | Bằng chứng implementation/runtime cần đạt để task được hoàn tất |

## Stage-aware pattern matching

Per-risk lifecycle metadata nằm tại `references/lifecycle-profile.md`. Caller MUST dùng profile này trước category detail để tránh xử lý pattern quá sớm.

- Stage order: `requirements → design → tasks → implementation`.
- Pattern chưa tới stage của caller là `DEFERRED`, không phải `NOT_APPLICABLE`.
- `requirements`: không dùng absence của technical architecture để kết luận N/A; chỉ promote lesson thành requirement khi failure có user/domain observable consequence.
- `design`: xác định `APPLIES/N/A/NEEDS_UPSTREAM` authoritative và map requirement refs nếu có.
- `tasks`: bắt đầu từ Runtime Risk Design; refresh để phát hiện drift/false-N/A.
- `implementation`: chỉ đọc Risk ID đang thực thi.
- `audit`: kiểm toàn chuỗi trace theo current artifacts.


## Contract với task generator

- Mỗi risk `APPLIES` phải map tới **ít nhất một task cụ thể**.
- Task phải nằm ở phase/story tạo ra boundary; không dồn mặc định thành “runtime test cuối dự án”.
- Nếu một task đã cover đủ risk thì tái sử dụng và trace Risk ID; không duplicate.
- Runtime-risk task có thể là implementation, integration, smoke/e2e/runtime verification hoặc kết hợp; điều quan trọng là nó phòng/phát hiện đúng failure mode.
- Quy tắc “test là tùy chọn” của task generator không được dùng để bỏ runtime-risk obligation.
- `NEEDS_UPSTREAM` chặn việc tuyên bố task plan hoàn tất; caller phải quay lại artifact có thẩm quyền thay vì invent behavior.

## Evidence semantics

Khi runtime-risk task được implement, evidence chỉ có:
- `PASS`: đúng proof mà pattern yêu cầu đã chạy và đạt.
- `FAIL`: proof đã chạy và thất bại.
- `BLOCKED`: chưa thể chạy do thiếu environment/dependency/quyền/tool.

`BLOCKED`, `unavailable`, “chưa chạy được” hoặc test ở tầng khác pass **không phải PASS**.

### Evidence Integrity Protocol

Ngoài trạng thái PASS/FAIL/BLOCKED, mọi proof runtime có khả năng bị nhầm process, nhầm command, nhầm artifact hoặc nhầm nguyên nhân MUST ghi đủ provenance tối thiểu:

| Field | Bắt buộc xác định |
|---|---|
| Command | Command thực tế đã chạy sau khi shell/package-manager wrapper resolve tham số |
| Target | Package/service/app/test suite mà command thực sự tác động |
| Revision | Source revision/commit hoặc working-tree state dùng để tạo runtime/artifact |
| Runtime identity | Process/service nào đang phục vụ request; port/endpoint nào được probe |
| Exit evidence | Exit code và summary có ý nghĩa như test count/task count/build result |
| Artifact evidence | Generated artifact nào thay đổi, được review và có nằm trong source control theo contract hay không |
| Environment mutation | Command có thay đổi env/config/database/generated state hay không |
| Stable verification window | Revision + working-tree state có giữ ổn định từ lúc probe/start tới khi proof/generation kết thúc hay bị concurrent workflow/watcher sửa source |
| Failure causality | PRIMARY_FAILURE / COLLATERAL_CANCELLED / INDEPENDENT_FAILURE khi có nhiều process/task |

Quy tắc:
- `command printed` không đồng nghĩa `command intended`; phải xác minh argument forwarding của package script/test runner khi nó ảnh hưởng mode chạy.
- `generator succeeded` không đồng nghĩa artifact đúng revision; nếu generator đọc từ runtime endpoint, phải xác minh process hiện tại start thành công và endpoint thuộc revision mong muốn.
- `tests/build xanh ở một package` không được dùng để suy package sibling pass.
- Khi orchestrator dừng/cancel sibling sau một failure, exit code của sibling chỉ là collateral cho tới khi command sibling được chạy độc lập hoặc có evidence nó tự fail.
- Command setup/install không được âm thầm coi là read-only; nếu nó có thể mutate `.env`, database hoặc generated artifacts, task phải kiểm tra side effect trước/sau.
- Với generated contract/artifact, PASS chỉ khi source runtime đúng revision, working tree giữ ổn định xuyên suốt probe/generation, generation thành công, diff được review, consumer verification chạy đạt và artifact canonical đã được lưu theo contract của repo.
- Nếu source/config/generated artifact thay đổi **trong khi** long-running verification/generator đang chạy, proof đó bị coi `CONTAMINATED/STALE` cho boundary bị ảnh hưởng; không tiếp tục dùng artifact/result chỉ vì command đã exit 0.
- Exit code 0 không tự động đồng nghĩa verification sạch. Warning bất ngờ tại runtime/test boundary như unhandled network request, hydration mismatch, accessibility/semantic violation, missing provider/runtime dependency phải được phân loại và xử lý hoặc ghi rõ là KNOWN/ACCEPTED; không được âm thầm bỏ qua chỉ vì suite xanh.

### Final Revision Verification Rule

Evidence chỉ có hiệu lực cho đúng revision/working-tree state đã tạo ra nó.

Khi source/config/generated artifact thay đổi sau một lần verify:
1. xác định gate nào thực sự bị ảnh hưởng bởi thay đổi;
2. đánh dấu evidence của các gate đó là `STALE`/`PENDING`, không giữ `PASS` cũ như thể vẫn đại diện cho HEAD mới;
3. chỉ rerun các gate bị ảnh hưởng hoặc các gate aggregate phụ thuộc chúng;
4. không bắt buộc rerun gate độc lập không bị thay đổi, nhưng phải có provenance chứng minh dependency không đổi;
5. final completion chỉ được chốt khi mọi required gate còn hiệu lực trên revision cuối cùng.

Ví dụ: backend source không đổi sau API E2E pass thì không cần chạy lại API E2E chỉ vì frontend sửa import; ngược lại, frontend refactor sau frontend test pass làm evidence frontend cũ trở thành stale cho phần bị ảnh hưởng.

### Generated artifact freshness

Khi feature phụ thuộc generated artifact từ runtime/service khác, task plan SHOULD tạo một chuỗi proof thay vì một lệnh generate đơn lẻ:

1. bảo đảm runtime target dự kiến có thể bind/start;
2. xác minh process target thật sự start thành công, không có port conflict/readiness failure;
3. probe một capability/schema mới đại diện cho revision cần generate;
4. chạy generator;
5. review generated diff để phát hiện stale/wrong schema;
6. chạy consumer typecheck/test liên quan;
7. lưu/commit artifact nếu repo coi generated output là canonical tracked artifact;
8. xác minh revision cuối cùng chứa artifact mới.

## Quản lý catalog phân loại

Một lỗi chỉ nên được promote thành reusable pattern khi thỏa cả:
1. Có thể tái diễn ở nhiều feature/project, không chỉ là typo cục bộ.
2. Có điều kiện kích hoạt nhận diện được từ spec/plan/architecture.
3. Có symptom/failure mode rõ.
4. Có root cause đủ tổng quát.
5. Giải thích được vì sao verification hiện tại có thể bỏ sót.
6. Có task-generation rule và required evidence cụ thể để ngăn/phát hiện lỗi sớm hơn.

Không thêm một incident riêng lẻ vào catalog nếu chưa rút được rule tổng quát. Pattern mới phải được đặt vào đúng category file và đăng ký prefix/category trong `catalog-index.md` nếu là nhóm mới.

## Upstream learning protocol

Khi một repo consumer gặp lỗi trong lúc vibe code:

1. **Fix local incident trước** nếu cần để hiểu đúng root cause; không promote một phỏng đoán.
2. Phân loại kết quả thành:
   - `LOCAL_INCIDENT`: chỉ đặc thù repo/tình huống, không update canonical catalog.
   - `UPSTREAM_CANDIDATE`: thỏa 6 điều kiện reusable pattern ở trên.
   - `KNOWN_PATTERN`: catalog canonical đã có pattern tương đương; chỉ update upstream nếu lesson mới làm pattern chính xác/hữu ích hơn.
3. Với `UPSTREAM_CANDIDATE` hoặc cải tiến `KNOWN_PATTERN`:
   - đọc bản canonical mới nhất từ `oh-my-skill/main` trước khi ghi;
   - chọn đúng category bằng `references/catalog-index.md`;
   - kiểm tra duplicate/overlap với các Risk ID hiện có;
   - update đúng category file; chỉ sửa index nếu thêm category/prefix mới;
   - giữ Risk ID ổn định; pattern mới dùng ID kế tiếp trong đúng prefix, không tái sử dụng ID cũ;
   - bump version trong `manifest.json` và metadata version của `SKILL.md`;
   - commit **trực tiếp** vào `main` với commit message mô tả lesson, không tạo branch/PR.
4. Sau khi upstream commit thành công, bản local consumer được xem là **stale** cho tới khi sync lại canonical skill.
5. Không sửa canonical chỉ để ghi lịch sử incident. Canonical lưu pattern tổng quát; bằng chứng repo cụ thể chỉ dùng để suy ra pattern.

### Quy tắc update thẳng main

Direct-to-main chỉ được thực hiện khi:
- người dùng đã cho phép workflow này hoặc canonical manifest đã xác nhận `learning.promotion = direct-to-main` trong ngữ cảnh mà user đã ủy quyền workflow;
- agent có quyền ghi vào canonical repo;
- root cause đã đủ chắc chắn;
- thay đổi không xóa/đổi nghĩa Risk ID hiện có một cách breaking;
- branch `main` chưa di chuyển kể từ lúc đọc canonical content, hoặc agent đã refresh/reconcile trước khi ghi.

Nếu không có quyền ghi canonical repo, trả `BLOCKED`, giữ lesson dưới dạng candidate trong repo/session hiện tại và không sửa local catalog như một canonical fork.

Nếu có conflict hoặc upstream đã thay đổi, refresh `main`, hợp nhất semantic trước rồi mới commit; không force-push.

## Sync protocol cho repo consumer

Sau khi canonical upstream thay đổi, repo consumer SHOULD kéo lại **toàn bộ** thư mục skill từ:

`sonhoang23/oh-my-skill@main:skills/runtime-verification`

về vị trí cài local, thường là:

`.agents/skills/runtime-verification/`

Quy tắc sync:
- canonical thắng đối với mọi file bên trong thư mục `runtime-verification`;
- không merge thủ công từng failure pattern giữa local/upstream;
- repo-specific integration với SpecKit hoặc workflow riêng phải nằm **ngoài** canonical skill folder;
- trước khi overwrite local, nếu phát hiện local-only change chưa có upstream, phân loại/promote lesson đó trước để tránh mất tri thức;
- sau sync, xác minh `manifest.json.version` local khớp upstream.

Công thức vận hành:

`learn locally → validate → promote thẳng upstream main → sync canonical xuống consumer`.

## Hoàn tất khi

- Runtime surface liên quan đã được nhận diện theo đúng lifecycle mode.
- Chỉ catalog entry liên quan và đủ stage được đánh giá; pattern stage sau được defer thay vì false-N/A.
- Output đúng contract của mode và giữ traceability tới artifact có thẩm quyền.
- Không có `NEEDS_UPSTREAM` bị âm thầm chuyển thành giả định.
- Output đủ để task generator tạo task mà không phải tự suy lại failure semantics.
- Runtime Lesson Candidate reusable đã được phân loại rõ là local-only hoặc đã promote về canonical upstream.
- Nếu upstream vừa thay đổi, consumer được đánh dấu/cảnh báo cần sync lại trước khi coi catalog local là mới nhất.
- Nếu promotion cần ghi canonical nhưng không có quyền ghi, kết quả phải là `BLOCKED`, không được âm thầm ghi vào consumer copy.
- Evidence runtime quan trọng có provenance đủ theo Evidence Integrity Protocol; không nhầm stale process, wrapper command hoặc collateral cancellation thành PASS/FAIL độc lập.
- Generated artifact phụ thuộc runtime đã được kiểm freshness theo đúng revision và consumer contract trước khi coi là PASS.
