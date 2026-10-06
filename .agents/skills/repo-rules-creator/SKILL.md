---
name: repo-rules-creator
description: >-
  Phân tích một repository bất kỳ và tạo một skill rules ngắn gọn, đặc thù cho repo đó để model hiểu các quy tắc chung khi vibe coding. Dùng khi người dùng muốn tạo repo rules, project rules, coding rules hoặc một skill dạng repo-name-rules; khi cần chuẩn hóa kiến trúc, folder, tech stack, business invariants, design system, documentation discipline, change discipline, validation và Git safety thành hướng dẫn ngắn để tái sử dụng trong nhiều cuộc hội thoại.
---

# Repo Rules Creator

Tạo một skill `<repo-name>-rules` giúp model hiểu các quy tắc quan trọng của repository mà không tiêu tốn nhiều context.

Mục tiêu: **ngắn, đặc thù repo, có tác động trực tiếp đến quyết định khi code**.

## Workflow

### 1. Đọc repo trước khi viết rules

Ưu tiên kiểm tra các nguồn sau nếu tồn tại:

- `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`;
- `package.json`, workspace config, lockfile;
- config framework, lint, formatter, test, CI;
- `development_specs/`, `docs/`, `architecture/`, ADR, design-system docs;
- cấu trúc `apps/`, `packages/`, `src/`, `components/`, `modules/`;
- design system, theme, token, shared UI;
- migration/schema/database config;
- các pattern lặp lại trong code hiện có.

Không suy diễn rule quan trọng chỉ từ tên file. Xác minh bằng code hoặc tài liệu thực tế khi có thể.

### 2. Xác định canonical development docs

Tìm nơi repo đang lưu tài liệu phát triển tổng hợp, ví dụ:

- `development_specs/`;
- `docs/` hoặc `docs/development/`;
- `architecture/`;
- ADR/design-system docs nếu đó là nguồn chuẩn thực tế.

Nếu đã có một nơi rõ ràng và đủ vai trò, **dùng nơi đó**, không tạo folder mới trùng chức năng.

Nếu repo không có nơi phù hợp, tạo:

```text
development_specs/
```

và dùng nó làm nơi tổng hợp architecture, business rules, design system và conventions quan trọng của repo.

Rules sinh ra phải nêu rõ canonical docs path.

### 3. Trích xuất 10 nhóm rules

Chỉ giữ nhóm có ý nghĩa với repo:

1. **Repo Purpose** — mục tiêu, phạm vi, đối tượng sử dụng.
2. **Architecture** — frontend/backend/database, module boundary, dependency direction.
3. **Folder Structure** — code nào thuộc đâu, folder nào không nên sửa tùy tiện.
4. **Tech Stack & Coding Convention** — framework, package manager, naming, pattern bắt buộc.
5. **Business Rules** — invariant nghiệp vụ không được phá.
6. **Design System & Frontend** — reuse component, token, styling convention, UI consistency.
7. **Change Rules** — reuse trước, tránh duplicate, không sửa unrelated code, giữ compatibility.
8. **Validation Rules** — lint, typecheck, test, build, migration hoặc check cần chạy.
9. **Git & Safety** — secret, generated files, destructive changes, commit hygiene.
10. **Documentation Rules** — canonical docs, docs-before-code cho thay đổi lớn, xử lý docs/code conflict và nghĩa vụ cập nhật docs.

Chi tiết từng nhóm: đọc `references/rule-categories.md` khi cần.

### 4. Documentation rules phải đủ rõ

Repo rules sinh ra nên nói ngắn gọn:

- canonical development docs nằm ở đâu;
- trước khi thay đổi architecture, business logic, API contract lớn hoặc design system, phải đọc tài liệu liên quan;
- trong câu trả lời nên nêu file tài liệu chính đã tham chiếu nếu có;
- nếu docs và code mâu thuẫn, chỉ ra mâu thuẫn; mặc định coi docs là intended design, nhưng nếu có bằng chứng docs đã stale thì không âm thầm ép code theo docs — phải báo rõ và cập nhật docs/code nhất quán;
- thay đổi lớn về architecture, business invariant, data model quan trọng, API contract hoặc design system phải cập nhật tài liệu tương ứng;
- thay đổi tài liệu phải ngắn gọn, ghi rõ **cái gì đổi** và **vì sao**;
- không bắt update docs cho bugfix hoặc chỉnh sửa nhỏ không thay đổi behavior/system contract.

Nguyên tắc nhớ nhanh:

**Docs before architecture. Code follows intended docs. Big changes update docs.**

### 5. Ưu tiên rule đặc thù repo

Không nhét best practice chung chung mà model vốn đã biết.

Giữ rule khi nó trả lời được một câu như:

- "Ở repo này phải dùng gì?"
- "Không được làm gì?"
- "Code này nên đặt ở đâu?"
- "Có pattern nào phải reuse?"
- "Business invariant nào không được phá?"
- "Tài liệu chuẩn nằm ở đâu?"
- "Trước khi hoàn thành phải chạy check gì?"

Nếu một rule không thay đổi quyết định khi code, bỏ nó.

### 6. Frontend phải kiểm tra design system trước

Khi repo có frontend, tìm trước:

- `components/ui/`, shared components;
- `components.json`, Storybook;
- theme, design tokens, Tailwind config;
- CSS variables, typography, spacing, radius, color system;
- các page/component tương tự.

Rules sinh ra nên phản ánh nguyên tắc:

- **Reuse before create.**
- **Token before hard-code.**
- **System before custom.**

Không tự tạo component mới nếu component hiện có có thể reuse hoặc compose.
Không dùng inline CSS hay hard-code style nếu design system đã có abstraction tương ứng.
Không tạo UI pattern mới chỉ vì nhanh hơn trong một task đơn lẻ.

### 7. Giữ output ngắn để tiết kiệm token

`SKILL.md` của repo rules là tài liệu được nạp thường xuyên, nên ưu tiên context efficiency.

Mặc định:

- khoảng 80–150 dòng hoặc ngắn hơn nếu đủ;
- mỗi rule 1–3 dòng;
- không copy nguyên README/docs;
- không giải thích dài nếu rule đã rõ;
- chi tiết hiếm dùng đưa sang `references/`;
- không tạo reference nếu repo đơn giản và không cần.

### 8. Naming và vị trí output

Tên mặc định:

```text
<repo-name>-rules
```

Chuẩn hóa repo name thành `kebab-case` và tránh hậu tố lặp `-rules-rules`.

Nếu repo đã có convention riêng cho skill, tuân theo convention đó. Nếu không có, ưu tiên:

```text
skills/<repo-name>-rules/SKILL.md
```

### 9. Format output

Ưu tiên cấu trúc ngắn:

```markdown
---
name: <repo-name>-rules
description: ...
---

# <Repo Name> Rules

## Purpose
- ...

## Documentation
- Canonical docs: `development_specs/` hoặc path thực tế của repo.
- Đọc docs liên quan trước thay đổi lớn; thay đổi lớn phải cập nhật docs.

## Architecture
- ...

## Design System
- ...

## Change Rules
- ...

## Validation
- ...
```

Không bắt buộc đủ cả 10 heading. Chỉ giữ phần có rule đáng nhớ.

### 10. Không bịa rule

Phân biệt rõ:

- **Observed**: được xác nhận từ repo;
- **Inferred**: suy ra mạnh từ pattern lặp lại;
- **Proposed**: đề xuất mới chưa phải convention hiện có.

Skill rules cuối cùng mặc định chỉ chứa **Observed** và các **Inferred** có độ tin cậy cao.
Nếu muốn thêm Proposed rule, nêu rõ cho người dùng trước hoặc đánh dấu riêng để họ quyết định.

Riêng việc tạo `development_specs/` khi repo chưa có canonical development docs là hành vi mặc định của skill, không phải suy diễn convention cũ.

### 11. Kiểm tra trước khi hoàn thành

Dùng checklist trong `references/repo-analysis-checklist.md` để rà lại:

- rules có đặc thù repo không;
- đã xác định canonical development docs chưa;
- có bỏ sót design system/business invariant quan trọng không;
- có rule chung chung hoặc trùng lặp không;
- output có đủ ngắn để load thường xuyên không;
- frontmatter/path/reference có hợp lệ không.

Nếu repo có validator cho skill, chạy validator đó trước khi coi task hoàn thành.

## Tiêu chí chất lượng

Một repo rules tốt phải đạt bốn điều:

1. **Model đọc nhanh** — ít token.
2. **Model quyết định đúng** — rule đủ cụ thể để định hướng code.
3. **Model không phá system** — đặc biệt architecture, business invariant và design system.
4. **Model giữ docs và code đồng bộ** — thay đổi lớn không để tài liệu bị stale.
