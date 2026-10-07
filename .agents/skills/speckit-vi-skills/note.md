------------------ SPECKIT ------------------------------

1. Bạn đã ở đúng thư mục dự án.

2. Khởi động Codex ngay trong thư mục dự án này.
   Các skill của Spec Kit đã được cài tại:

   `.agents/skills`

3. Quy trình chính:

   3.1 `$speckit-constitution`
   Thiết lập nguyên tắc và quy ước nền tảng.

   3.2 `$speckit-specify`
   Tạo/cập nhật `spec.md`. Đây là nguồn requirement chính.

   3.3 `$speckit-clarify`
   Làm rõ ambiguity quan trọng trong spec khi cần.

   3.4 `$speckit-system-modeling-vi` — mode `spec`
   Chạy Diagram Check và mô hình hóa spec. Output visual nằm trong `spec-diagram/`. Không tạo lớp `analysis/`.

   3.5 `$speckit-plan`
   Tạo technical implementation design từ constitution + spec.

   3.6 `$speckit-system-modeling-vi` — mode `plan`
   Mô hình hóa architecture/data flow/technical sequence/data model/deployment khi có giá trị. Output trong `plan-diagram/`.

   3.7 `$speckit-checklist`
   Tạo checklist kiểm tra chất lượng sau plan khi cần.

   3.8 `$speckit-tasks`
   Chuyển plan thành task có thể thực hiện.

   3.9 `$speckit-system-modeling-vi` — mode `tasks`
   Chỉ tạo dependency/critical-path/parallelization diagram khi text khó quan sát. Output trong `tasks-diagram/`.

   3.10 `$speckit-analyze`
   Kiểm tra consistency giữa constitution, spec, plan, tasks và diagram dẫn xuất khi cần.

   3.11 `$speckit-implement`
   Thực hiện task. Sau mỗi phase/milestone làm thay đổi mental model đáng kể, chạy `$speckit-system-modeling-vi` mode `implementation` để cập nhật `implementation-diagram/`.

   3.12 `$speckit-converge`
   Đánh giá intended state so với current implementation, append task gap khi cần.

   3.13 `$speckit-system-modeling-vi` — mode `converge`
   Tạo current-state/gap diagram khi có giá trị. Output trong `converge-diagram/`.


## Optional Companion Skills

SpecKit hỗ trợ skill guardrail theo stack/template mà không hard-code framework vào core workflow.

Protocol canonical: `companion-skills.md`.

Nếu repo có `.agents/skills/next-nest-template-guardrails/SKILL.md` hoặc một companion `*-template-guardrails` phù hợp:

- `plan`: MUST discover/load và materialize stack-specific prevention design.
- `tasks`: MUST map guardrail thành task + required evidence cụ thể.
- `implement`: MUST đọc reference liên quan trước khi sửa boundary tương ứng.
- `analyze`: MUST audit coverage/drift của companion obligations.
- `converge`: MUST audit deferred debt, stale evidence, generated artifact/toolchain drift.
- `constitution/specify/clarify/checklist`: không kéo technical detail xuống requirement/governance ngoài authority.
- `system-modeling`: companion không phải source of truth; chỉ visualize semantics đã materialize.
- `taskstoissues`: preserve traceability, không re-evaluate companion.

Quan hệ:

```text
runtime-verification
  = reusable generic failure semantics + Risk ID

*-template-guardrails
  = stack/template-specific application rules
```

Nếu repo không cài companion, SpecKit tiếp tục workflow bình thường.

## Pipeline khuyến nghị

```text
constitution                    # runtime policy nhẹ, không quét catalog
→ specify                       # runtime-verification: requirements
→ clarify (khi cần)             # requirements, ưu tiên known ambiguity
→ system-modeling(spec)
→ plan                          # runtime-verification: design (authoritative inventory)
→ system-modeling(plan)
→ checklist (khi cần)           # runtime-derived requirement-quality checks
→ tasks                         # runtime-verification: tasks/coverage
→ system-modeling(tasks, khi cần)
→ analyze (khi cần)             # independent runtime trace audit
→ implement                     # runtime-verification: implementation/evidence
→ system-modeling(implementation, theo phase/mốc)
→ converge                      # runtime-verification: audit + learning
→ system-modeling(converge)
```

Runtime prevention chạy như cross-cutting layer với traceability mục tiêu:
`Risk → Requirement → Design → Task → Evidence`. Không biến runtime catalog thành source of truth mới và không quét toàn catalog ở mọi phase.

Nếu `clarify` làm thay đổi mental model của spec, chạy lại `system-modeling(spec)`.

## Artifact flow

```text
spec.md
├── spec-diagram/
│
plan.md + research.md + data-model.md + contracts/
├── plan-diagram/
│
tasks.md
├── tasks-diagram/        # chỉ khi cần
│
implementation
├── implementation-diagram/
│
converge
└── converge-diagram/
```

## Thẩm quyền

```text
constitution
  > spec.md
    > plan.md + technical design artifacts
      > tasks.md
        > implementation state
```

- Diagram là **derived visual artifact**, không nằm trong authority chain.
- Không tạo `analysis/` làm một lớp source of truth trung gian.
- Nếu modeling phát hiện ambiguity/conflict, quay lại artifact có thẩm quyền để sửa.
- Code/current state không được âm thầm thay đổi intended design.
- `diagram-design-vi` chỉ render visual; `speckit-system-modeling-vi` quyết định semantics, placement, traceability và sync.

## Convention folder diagram

```text
FEATURE_DIR/
  spec-diagram/
  plan-diagram/
  tasks-diagram/
  implementation-diagram/
  converge-diagram/
```

Không bắt buộc mọi folder phải tồn tại. Chỉ tạo khi Diagram Check dương tính.

## Phạm vi theo phase

### Spec modeling

Tập trung vào:
- system context/boundary;
- actors/roles/capabilities;
- use case/core flow;
- conceptual domain;
- lifecycle/state.

Không đi vào architecture/API/database/deployment.

### Plan modeling

Tập trung vào:
- architecture/component;
- data flow;
- technical sequence;
- integration;
- data model/ER;
- deployment/security boundary khi plan đã quyết định.

### Tasks modeling

Chỉ dependency/critical path/parallelization khi thật sự giúp đọc task list.

### Implementation modeling

Mô tả **current implemented state** theo phase/milestone và phân biệt rõ với intended design.

### Converge modeling

Mô tả intended-vs-current, gap và remaining dependency khi có giá trị.

## Diagram governance

- HTML là living diagram canonical.
- Không dùng `.mmd/.puml` làm source trung gian.
- SVG/PNG chỉ là export derivative khi được yêu cầu.
- Diagram phải link về artifact nguồn.
- Giữ ID truy vết như `US*`, `FR-*`, `T*`, entity/component name.
- Không tạo diagram cho mọi Markdown.
- Không duplicate cùng một model.
- Không regenerate chỉ vì sửa câu chữ.
- Khi source model đổi đáng kể, cập nhật diagram tương ứng.
