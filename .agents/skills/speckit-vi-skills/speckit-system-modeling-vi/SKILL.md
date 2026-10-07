---
name: "speckit-system-modeling-vi"
description: "Phân tích, mô hình hóa và quản trị diagram xuyên suốt vòng đời Spec Kit: spec, plan, tasks, implementation và converge; dùng diagram-design-vi làm renderer."
compatibility: "Yêu cầu cấu trúc dự án Spec Kit có .specify/; với feature-scoped modeling cần .specify/feature.json hợp lệ."
metadata:
  author: "adaptation"
  source: "../../system-analysis-uml-skill"
---

# Speckit System Modeling VI

## Mục đích

Đây là lớp **system modeling xuyên suốt**, không phải một phase riêng chỉ chạy giữa `specify` và `plan`.

Skill này chịu trách nhiệm:

1. xác định artifact nguồn đang cần mô hình hóa;
2. đọc đúng source of truth của phase;
3. phân tích relation, boundary, flow, state, dependency và structure;
4. quyết định diagram nào thật sự có giá trị;
5. gọi `diagram-design-vi` để render;
6. đặt diagram cạnh đúng artifact theo convention;
7. giữ traceability, link hai chiều, chống duplicate và kiểm tra drift;
8. duy trì Diagram Atlas/Feature Ledger để diagram luôn discoverable khi repo và số feature tăng.

Skill **không tạo một lớp `analysis/` riêng**. Modeling là derived view của artifact nguồn; nếu phát hiện ambiguity hoặc conflict, phải quay lại sửa artifact có thẩm quyền thay vì tạo một bộ semantics cạnh tranh.

## Vị trí trong workflow

System modeling dùng **Lazy Modeling Gate**: người dùng không cần gọi skill này thủ công giữa mọi command. Command ở phase sau phải tự bảo đảm modeling gate của phase trước đã pass và còn fresh trước khi tiếp tục.

```text
specify / clarify
      ↓
plan
  └─ ensure-model(spec)

tasks
  └─ ensure-model(plan)

implement phase 1
  └─ ensure-model(tasks)

implement phase N
  └─ ensure-model(implementation phase N-1)

converge
  └─ ensure-model(latest implementation phase)
  └─ run model(converge) trước khi tuyên bố hoàn tất
```

Người dùng vẫn MAY gọi `$speckit-system-modeling-vi` trực tiếp để xem/cập nhật model sớm. Nếu `clarify` làm đổi spec sau một lần modeling trước đó, source fingerprint sẽ stale và `plan` tự chạy lại gate `spec`.

## Resolve active feature

Khi modeling thuộc một active feature:

1. đọc `.specify/feature.json`;
2. lấy `feature_directory`;
3. không hard-code đường dẫn feature hoặc suy từ branch;
4. nếu feature config thiếu/hỏng, dừng và yêu cầu sửa/chạy lại `$speckit-specify`.

Đặt `FEATURE_DIR = feature_directory`.

## Router theo artifact/phase

Xác định phase từ yêu cầu người dùng hoặc artifact vừa hoàn tất, rồi đọc đúng reference:

| Phase / nguồn | Reference | Output mặc định |
| --- | --- | --- |
| Research / product direction | `references/research.md` | `research-diagram/` cạnh artifact phù hợp |
| `spec.md` sau specify/clarify | `references/spec.md` | `FEATURE_DIR/spec-diagram/` |
| `plan.md` + technical design artifacts | `references/plan.md` | `FEATURE_DIR/plan-diagram/` |
| `tasks.md` | `references/tasks.md` | `FEATURE_DIR/tasks-diagram/` |
| Implementation theo phase/mốc | `references/implementation.md` | `FEATURE_DIR/implementation-diagram/` |
| Converge/current-state gap | `references/converge.md` | `FEATURE_DIR/converge-diagram/` |

Luôn đọc thêm:

- `references/modeling-rules.md`;
- `references/diagram-governance.md`;
- `references/traceability.md`;
- `references/diagram-atlas.md` khi repo dùng Diagram Atlas/Feature Ledger.

Chỉ đọc methodology từ `../../system-analysis-uml-skill/` khi loại model cần đến nó.

## Lazy Modeling Gate và state

Feature-scoped modeling MUST duy trì derived metadata tại:

`FEATURE_DIR/.modeling-state.json`

File này chỉ ghi trạng thái gate/freshness; nó **không** nằm trong authority chain và không chứa requirement/decision mới.

Schema khái niệm:

```json
{
  "schema_version": 1,
  "gates": {
    "spec": {
      "status": "modeled",
      "source_hashes": {
        "spec.md": "<git-hash-object>"
      },
      "outputs": ["spec-diagram/system-context.html"]
    },
    "plan": {
      "status": "no-diagram-needed",
      "source_hashes": {
        "plan.md": "<git-hash-object>"
      },
      "outputs": []
    },
    "tasks": {
      "status": "modeled",
      "source_hashes": {
        "tasks.md": "<git-hash-object>"
      },
      "outputs": ["tasks-diagram/critical-path.html"]
    },
    "implementation:phase-01": {
      "status": "no-diagram-needed",
      "source_hashes": {
        "tasks.md": "<git-hash-object>",
        "apps/.../file.ts": "<git-hash-object>"
      },
      "outputs": []
    }
  }
}
```

Trạng thái gate hợp lệ:

- `modeled`: Diagram Check dương và output cần thiết đã được tạo/cập nhật.
- `no-diagram-needed`: Diagram Check âm; không cần tạo diagram nhưng gate vẫn pass.
- `blocked`: modeling phát hiện ambiguity/conflict/drift cần sửa upstream; trạng thái này không pass gate.

### Freshness check

Một gate chỉ được xem là **fresh** khi:

1. entry tương ứng tồn tại và status là `modeled` hoặc `no-diagram-needed`;
2. tập source artifact hiện hành khớp tập source đã ghi;
3. content hash của từng source còn khớp;
4. nếu status là `modeled`, mọi output đã ghi vẫn tồn tại.

Dùng `git hash-object -- <path>` hoặc cơ chế content hash tương đương để fingerprint nội dung working tree. Với source dạng thư mục như `contracts/`, source set gồm các file hiện hành liên quan trong thư mục; thêm/xóa file làm gate stale.

### Source set mặc định

- `spec`: `spec.md`.
- `plan`: `plan.md` và technical design artifact hiện hành như `research.md`, `data-model.md`, `quickstart.md`, `contracts/**` khi tồn tại.
- `tasks`: `tasks.md`.
- `implementation:phase-XX`: `tasks.md` + các source/code/config file được phase đó thực sự tạo/chỉnh và được modeling dùng để mô tả current state.
- `converge`: `tasks.md` + current-state source/code/config file thực sự được converge modeling dùng.

### ensure-model

Command phase sau thực hiện `ensure-model(<gate>)`:

1. đọc `.modeling-state.json`;
2. nếu gate pass + fresh → tiếp tục ngay, không gọi modeling;
3. nếu thiếu, stale, output mất hoặc state legacy chưa tồn tại → tự invoke `$speckit-system-modeling-vi` đúng mode/scope;
4. modeling chạy Diagram Check, chỉ redraw khi cần, rồi cập nhật state kể cả khi kết quả là `no-diagram-needed`;
5. command gọi lại freshness check; nếu gate vẫn `blocked` hoặc không hợp lệ thì không được tiếp tục phase sau.

Diagram/file tồn tại **không đủ** để suy ra gate fresh. Với feature cũ có diagram nhưng chưa có state, chạy một modeling validation pass để bootstrap state; nếu diagram đúng thì không regenerate vô ích.

### Implementation phase key

Với implementation nhiều phase, dùng key ổn định theo số phase trong `tasks.md`, ví dụ:

- `implementation:phase-01`
- `implementation:phase-02`
- `implementation:phase-03`

Trước khi bắt đầu phase N > 1, implementation MUST ensure gate `implementation:phase-(N-1)`. Khi resume giữa chừng, resolve phase hoàn tất gần nhất từ `tasks.md` và trạng thái code/task thực tế, không dựa riêng vào checkbox nếu có bằng chứng mâu thuẫn.

## Diagram Atlas và Feature Ledger

Repo này dùng **Diagram Atlas** làm navigation graph cho toàn bộ living diagram.

Canonical navigation artifacts:

- `docs/diagrams/index.html` — Repo Diagram Atlas, root ledger;
- `docs/diagrams/diagram-index.json` — graph registry;
- `FEATURE_DIR/diagrams.html` — Feature Diagram Ledger khi feature có diagram;
- mỗi diagram giữ navigation chrome tới Atlas / Feature Ledger / Parent / Source / Children / Related.

Chi tiết contract nằm tại `references/diagram-atlas.md`.

Sau mỗi modeling run có tạo/xóa/rename/thay relation diagram, MUST cập nhật registry + ledger + Atlas/backlinks liên quan **trước khi** ghi gate pass. Khi có checkout local, MUST chạy `python scripts/verify-diagram-atlas.py`.

Atlas/ledger/registry là derived navigation artifacts, không được thêm requirement/decision mới.

## Hai lớp diagram và hai loại truth

- **Feature-level diagram** nằm trong `FEATURE_DIR/<phase>-diagram/`.
  - `spec-diagram/`, `plan-diagram/`, `tasks-diagram/` là **planned truth**: mô tả requirement/intended design/kế hoạch thực thi của feature và MAY đi trước code.
  - `implementation-diagram/` là **implemented truth ở phạm vi feature phase**: chỉ được tạo/cập nhật từ code/config/runtime của phase đã hoàn tất và đã qua verification.
  - `converge-diagram/` là current-state/gap view cuối, không tự tạo implemented capability mới.
- **Project-level diagram** là visual companion của project-level Markdown và chỉ giữ **implemented truth đã được promote**. Project-level diagram đặt tại `docs/diagrams/<topic>/<name>.html`; inventory nằm tại `docs/diagrams/README.md`.
- Modeling ở mode `spec`, `plan` hoặc `tasks` MUST NOT tạo/cập nhật semantics trong project-level diagram. Các mode này chỉ được ghi candidate **Project Docs Impact / Promotion Plan**.
- Chỉ modeling `implementation:phase-XX` sau khi phase implementation + test/QA/validation đã hoàn tất mới MAY đề xuất promotion sang project-level docs/diagram.
- Promotion MUST dựa trên current implemented state đã verify, nhưng nếu current state lệch intended design thì phải cập nhật/chấp nhận artifact Spec Kit có thẩm quyền trước; không dùng code để âm thầm rewrite intended design.
- Không mặc định mỗi project doc có diagram. Chỉ tạo khi Diagram Check dương; các tài liệu glossary/convention/text contract có thể là text-only.
- Project doc có visual companion phải link tới diagram; diagram phải ghi canonical source về project Markdown tương ứng.
- Không tạo hai diagram giống nhau chỉ vì một bản thuộc `docs/` và một bản thuộc `specs/`. Chỉ giữ cả hai khi mức chi tiết, audience hoặc mục đích khác nhau rõ ràng.
- Báo cáo modeling phải nêu rõ `scope=feature|project`, `truth=planned|implemented`, phase nguồn và candidate/promoted project diagram liên quan.


## Runtime-sensitive modeling

`runtime-verification` là knowledge/checking layer, không phải source semantics cho diagram.

- Mode `spec`: chỉ visualize behavior/acceptance/edge-case đã materialize trong `spec.md`; không đọc Risk ID rồi tự thêm flow.
- Mode `plan`: MAY dùng `Runtime Risk Design` để làm nổi bật architecture/integration/failure-recovery boundary nếu Diagram Check dương.
- Mode `tasks`: MAY visualize critical dependency/verification path từ `Runtime Risk Coverage` khi text khó quan sát.
- Mode `implementation`: chỉ đưa prevention/evidence vào implemented truth sau evidence hợp lệ; `BLOCKED/STALE/CONTAMINATED` không được vẽ như verified.
- Mode `converge`: MAY thể hiện intended-vs-current runtime gap đã được converge finding xác định.
- Modeling không re-evaluate toàn catalog và không tạo Risk ID/status mới. Nếu source artifact thiếu/contradict runtime-sensitive semantics, báo upstream artifact cần sửa.


## Thẩm quyền artifact

```text
constitution
  > spec.md
    > plan.md + technical design artifacts
      > tasks.md
        > implementation state
```

Diagram là **derived visual artifact**, không đứng trong authority chain.

Quy tắc:

- diagram không được tạo requirement, quyết định hay business rule mới;
- code không được âm thầm sửa intended-design diagram;
- nếu implementation buộc thay đổi intended semantics/design, cập nhật artifact nguồn có thẩm quyền trước rồi mới đồng bộ diagram;
- current-state implementation diagram được phép cho thấy code hiện tại khác intended design, nhưng phải ghi rõ đây là current state.

## Diagram Check

Không mặc định vẽ.

Tạo/cập nhật diagram khi visual giúp hiểu rõ hơn một trong các yếu tố:

- system boundary hoặc containment;
- actor/role/capability relationship;
- flow, handoff, branching hoặc sequence;
- state/lifecycle;
- domain/data relationship;
- component/dependency/integration;
- architecture/data flow/deployment;
- task dependency/critical path;
- implemented current state;
- intended-vs-current gap.

Không tạo diagram khi bảng hoặc đoạn text ngắn truyền đạt tương đương.

## Phân vai với diagram-design-vi

`speckit-system-modeling-vi` quyết định:

- **WHAT** cần mô hình hóa;
- semantics nào được phép xuất hiện;
- nguồn nào có thẩm quyền;
- diagram nào cần tạo/cập nhật;
- placement, naming, traceability và sync;
- Atlas registry, Feature Ledger, parent/child/related relation và navigation backlinks.

`diagram-design-vi` quyết định:

- **HOW IT LOOKS**;
- visual type/layout;
- geometry;
- typography/theme;
- HTML/SVG rendering và accessibility.

Renderer không được tự thêm/bớt semantics để làm hình đẹp hơn.

## Output contract

- HTML là living diagram canonical.
- Không tạo `.mmd` hoặc `.puml` làm source trung gian.
- SVG/PNG chỉ là export derivative khi người dùng yêu cầu.
- Tên file nên mô tả model, ví dụ `system-context.html`, `architecture.html`, `phase-01-runtime-flow.html`.
- Không bắt buộc đánh số diagram nếu tên phase/model đã đủ rõ.
- Với implementation nhiều phase, ưu tiên prefix `phase-XX-`.

## Ngôn ngữ

Mọi text người đọc nhìn thấy trong diagram của repo này mặc định dùng **tiếng Việt tự nhiên, đầy đủ dấu**.

Giữ nguyên proper noun, acronym, path, command, ID như `US1`, `FR-001`, code identifier hoặc canonical technical term khi cần truy vết/chính xác.

Khi viết tiếng Việt, tham khảo `.agents/skills/natural-vietnamese-writing`.

## Ghi state sau modeling

Sau mỗi lần Diagram Check feature-scoped:

1. xác định gate key đúng mode/scope;
2. tính lại source set + content hashes;
3. ghi `status` là `modeled`, `no-diagram-needed` hoặc `blocked`;
4. ghi đúng output hiện hành; xóa output stale khỏi entry;
5. nếu feature có diagram, bảo đảm `FEATURE_DIR/diagrams.html` và `docs/diagrams/diagram-index.json` đã fresh; registry entry MUST phân biệt `scope`, `truth` và `phase`;
6. cập nhật Repo Atlas/navigation backlinks nếu inventory hoặc relation thay đổi; planned feature diagram được phép xuất hiện trong Atlas nhưng MUST NOT được trình bày như current project state;
7. với mode implementation đã verify, chạy Project Docs Promotion Check và chỉ cập nhật project-level docs/diagram cho semantics đã thực sự tồn tại;
8. **chạy QA trước khi ghi gate pass**:
   - mọi diagram vừa tạo/sửa MUST pass `.agents/skills/diagram-design-vi/scripts/self_check.py`;
   - khi có checkout local MUST pass `python scripts/verify-diagram-atlas.py` và `python scripts/verify-diagram-layout.py`;
   - khi có browser/screenshot MUST render ở 100% zoom và áp dụng `references/visual-qa.md`; nếu browser thật sự không khả dụng thì ghi rõ `browser_visual=unavailable` và không được tuyên bố đã visual-pass;
9. lưu QA evidence ngay trong gate entry để lần sau phân biệt “đã chạy” với “chỉ có checklist”, ví dụ:
   ```json
   "qa": {
     "self_check": "passed",
     "atlas": "passed",
     "layout": "passed",
     "browser_visual": "passed"
   }
   ```
10. chỉ sau khi QA đạt mới cập nhật `FEATURE_DIR/.modeling-state.json` atomically nếu môi trường cho phép.

Gate `modeled` có diagram nhưng thiếu QA evidence được xem là **legacy/incomplete** và MUST chạy validation bootstrap ở lần ensure-model tiếp theo. Không ghi gate pass nếu modeling phát hiện conflict/ambiguity, QA failure, output mất hoặc navigation/registry drift chưa được xử lý.

## Báo cáo hoàn tất

Báo cáo ngắn:

- phase/source artifact đã mô hình hóa;
- Diagram Check dương hay âm;
- diagram đã tạo/cập nhật và vị trí;
- diagram nào được bỏ qua vì không có giá trị;
- conflict/drift/open issue nếu có;
- artifact upstream nào cần sửa nếu modeling phát hiện vấn đề.
- candidate project-level diagram nào có thể cần promotion (planned mode), hoặc project-level diagram nào đã được promote từ implementation đã verify (implementation mode).

## Optional companion skill

Đọc protocol tại `../companion-skills.md`.

Companion skill **không phải modeling source of truth**:
- không tạo node/flow/state chỉ vì một guardrail tồn tại trong companion;
- chỉ visualize stack/runtime semantics đã được materialize trong spec/plan/tasks/current implementation có thẩm quyền;
- MAY dùng companion để hiểu thuật ngữ kỹ thuật hoặc kiểm xem diagram có diễn đạt sai boundary đã chốt hay không;
- nếu companion và artifact authoritative mâu thuẫn, sửa/quay lại artifact có thẩm quyền; không dùng diagram để giải quyết conflict.


## Hoàn tất khi

- [ ] đã resolve đúng source artifact/phase
- [ ] đã đọc reference tương ứng
- [ ] không tạo semantics mới ngoài source of truth
- [ ] Diagram Check đã chạy
- [ ] feature-scoped modeling đã cập nhật `.modeling-state.json` với source hash/status/output đúng
- [ ] chỉ tạo số diagram tối thiểu cần thiết
- [ ] diagram dùng `diagram-design-vi`
- [ ] mọi diagram đã pass Visual QA Gate của `diagram-design-vi` (không overflow, collision, orphan connector/label hoặc endpoint sai)
- [ ] placement đúng `docs/diagrams/<topic>/` với project-level hoặc `<phase>-diagram/` với feature-level
- [ ] link/traceability đủ để quay về artifact nguồn
- [ ] link hai chiều giữa project Markdown và visual companion khi modeling ở project-level
- [ ] không có diagram duplicate cùng một model
- [ ] drift giữa diagram và source đã được xử lý hoặc báo rõ
- [ ] planned feature diagram không làm project-level docs/diagram đi trước implementation
- [ ] nếu có promotion, source là implementation phase đã hoàn tất + verification pass + implementation modeling fresh
- [ ] đã kiểm tra duplicate/promotion giữa project-level và feature-level diagram khi có tác động xuyên repo
- [ ] mọi living diagram đã đăng ký trong `docs/diagrams/diagram-index.json`
- [ ] feature có diagram đã có `FEATURE_DIR/diagrams.html`
- [ ] diagram có navigation chrome tới Atlas/ledger/source/relations phù hợp
- [ ] Repo Atlas/Feature Ledger đã fresh sau thay đổi inventory/relation
- [ ] `python scripts/verify-diagram-atlas.py` pass khi có checkout local
- [ ] `python scripts/verify-diagram-layout.py` pass khi có checkout local
