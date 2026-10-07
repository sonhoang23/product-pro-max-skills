# SpecKit Optional Companion Skills

Mục tiêu: cho phép SpecKit tự dùng các skill guardrail theo stack/template khi repo cài chúng, nhưng không hard-code SpecKit thành workflow riêng của một framework.

## Discovery

Trước các stage kỹ thuật, caller SHOULD kiểm tra theo thứ tự:

1. well-known companion hiện tại:
   `.agents/skills/next-nest-template-guardrails/SKILL.md`;
2. nếu không có, tìm đúng một skill local khớp pattern:
   `.agents/skills/*-template-guardrails/SKILL.md`.

Nếu không có companion: tiếp tục SpecKit bình thường.

Nếu có đúng một companion phù hợp stack: nạp `SKILL.md`, sau đó chỉ đọc reference liên quan bằng Progressive Disclosure.

Nếu có nhiều companion có vẻ áp dụng và không thể xác định cái nào authoritative từ repo/config: không tự merge rule; ghi `COMPANION_AMBIGUOUS` và chỉ dùng artifact SpecKit + `runtime-verification` cho đến khi repo chọn rõ companion.

## Authority

Companion skill là **technical guidance layer**, không chen vào authority chain:

```text
constitution
  > spec.md
    > plan.md + technical design artifacts
      > tasks.md
        > implementation state
```

Companion:
- MAY phát hiện stack-specific prevention/verification obligation;
- MUST materialize obligation cần authority vào đúng artifact SpecKit trước khi downstream dùng;
- MUST NOT âm thầm thay đổi business behavior trong code;
- MUST NOT trở thành source of truth cạnh tranh với spec/plan/tasks;
- MUST NOT fork generic Runtime Risk catalog nếu lesson đã thuộc `runtime-verification`.

## Quan hệ với runtime-verification

`runtime-verification` = reusable cross-project failure semantics + Risk ID canonical.

`*-template-guardrails` = cách áp dụng cụ thể cho stack/template của repo.

Khi cùng một vấn đề xuất hiện:
1. dùng Risk ID canonical từ `runtime-verification` nếu có;
2. dùng companion để xác định command/file/library-specific prevention;
3. task/evidence phải trace được cả Risk ID và stack-specific implementation obligation khi hữu ích.

Nếu companion phát hiện lesson đủ tổng quát vượt template, promote về canonical `runtime-verification`; không mở rộng companion thành failure catalog thứ hai.

## Stage contract

| Stage | Cách dùng companion |
|---|---|
| constitution | Không nạp technical detail; chỉ tránh governance mâu thuẫn nếu user đã chốt policy template-wide. |
| specify | Không kéo implementation detail vào spec; requirement implication chỉ đến từ behavior/user consequence có authority. |
| clarify | Chỉ dùng để nhận biết ambiguity có consequence behavior; technical choice defer sang plan. |
| plan | **MUST discover/load nếu có**; materialize stack-specific prevention design vào plan/research/contracts thích hợp. |
| checklist | Không biến thành implementation checklist; chỉ kiểm wording requirement/plan implication đã materialize. |
| tasks | **MUST discover/load nếu có**; map prevention/evidence vào task cụ thể, không dồn mặc định về QA cuối. |
| analyze | **MUST discover/load nếu có**; audit coverage/drift giữa plan/tasks và companion obligations. |
| implement | **MUST discover/load reference liên quan**; thực thi guardrail và thu evidence đúng boundary. |
| converge | **MUST discover/load nếu có**; audit deferred debt, stale evidence, generated artifact/toolchain drift. |
| system-modeling | Companion không phải modeling authority; chỉ visualize semantics đã materialize trong artifact có thẩm quyền. |
| taskstoissues | Không re-evaluate companion; preserve task traceability/evidence obligation đã có. |

## Reporting

Khi companion được dùng, stage SHOULD ghi ngắn:

```text
Companion skill:
- DISCOVERED: <skill-name/path>
- APPLIED: <guardrail groups>
- MATERIALIZED INTO: <plan/tasks/code/evidence>
- DEFERRED/BLOCKED: <obligations>
```

Không cần report nếu repo không có companion.
