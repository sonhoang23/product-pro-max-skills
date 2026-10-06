# Rule Categories

Dùng tài liệu này khi cần phân tích sâu hơn trước khi rút gọn thành repo rules.

## 1. Repo Purpose

Tìm:
- repo phục vụ ai;
- use case chính;
- phạm vi sản phẩm;
- điều nằm ngoài scope.

Chỉ giữ thông tin ảnh hưởng đến quyết định triển khai.

## 2. Architecture

Tìm:
- monorepo hay single app;
- frontend/backend/database;
- module boundary;
- dependency direction;
- shared package;
- API boundary;
- event/queue/job nếu có.

Rule tốt phải chỉ ra dependency nào được phép và boundary nào không nên phá.

## 3. Folder Structure

Tìm:
- feature/module đặt ở đâu;
- shared code đặt ở đâu;
- generated/vendor/migration folder;
- file nào là source of truth;
- folder nào không nên sửa tùy tiện.

## 4. Tech Stack & Coding Convention

Tìm:
- framework và version quan trọng;
- package manager;
- ORM/query layer;
- state management;
- naming convention;
- import/path alias;
- error handling;
- test framework;
- pattern code lặp lại rõ ràng.

Không biến danh sách dependency thành rules nếu dependency không ảnh hưởng cách code.

## 5. Business Rules

Tìm invariant như:
- state transition;
- permission/role;
- uniqueness;
- ordering;
- idempotency;
- visibility;
- retention;
- save/ignore/archive behavior;
- calculation/domain constraint.

Ưu tiên rule mà nếu phá sẽ làm sản phẩm chạy sai dù code vẫn build được.

## 6. Design System & Frontend

Tìm:
- shared UI/component library;
- `components/ui`;
- design token;
- theme/CSS variables;
- Tailwind convention;
- typography/spacing/radius/color;
- form/table/modal/layout pattern;
- responsive/accessibility convention.

Mặc định sinh rule theo thứ tự ưu tiên:

1. reuse component hiện có;
2. compose component trước khi tạo abstraction mới;
3. dùng token/theme trước hard-code;
4. theo styling convention hiện có;
5. tránh inline CSS nếu repo không dùng pattern đó;
6. giữ consistency với màn hình/component tương tự.

## 7. Change Rules

Tìm các quy ước về cách sửa code:
- reuse trước khi create;
- tránh duplicate;
- không sửa unrelated files;
- giữ backward compatibility khi cần;
- migration discipline;
- không đổi public API ngoài scope;
- không refactor lớn trong bugfix nhỏ nếu không cần.

## 8. Validation Rules

Tìm command thật từ repo:
- lint;
- typecheck;
- unit/integration/e2e test;
- build;
- migration/schema check;
- format;
- generated code check.

Chỉ ghi command tồn tại thật. Nếu có nhiều mức validation, ưu tiên minimum set phù hợp với thay đổi.

## 9. Git & Safety

Tìm:
- generated files có được commit không;
- secret/env rule;
- commit convention;
- destructive migration/data operation;
- branch/release rule;
- file lock hoặc artifact cần tránh.

Không thêm policy Git tưởng tượng nếu repo chưa có convention và người dùng chưa yêu cầu.

## 10. Documentation

Tìm canonical development docs theo thứ tự bằng chứng thực tế, ví dụ:
- `development_specs/`;
- `docs/`, `docs/development/`;
- `architecture/`;
- ADR;
- design-system docs;
- tài liệu business/convention được repo dùng làm source of truth.

Nếu một nơi đã rõ ràng và đủ vai trò, dùng nơi đó. Không tạo thêm folder trùng chức năng.

Nếu không có canonical development docs, tạo `development_specs/` và dùng nó làm nơi lưu tài liệu tổng hợp quan trọng.

Rules nên quy định:
- đọc docs liên quan trước thay đổi architecture/business/API contract lớn/design system;
- nêu file tham chiếu chính trong câu trả lời khi có;
- khi docs và code mâu thuẫn, chỉ ra mâu thuẫn;
- mặc định xem docs là intended design, nhưng nếu docs stale thì phải nói rõ và làm docs/code nhất quán;
- thay đổi lớn phải cập nhật đúng tài liệu liên quan;
- docs update ngắn gọn: cái gì đổi + vì sao;
- không bắt update docs cho thay đổi nhỏ không đổi system contract.

## Bộ lọc cuối

Với từng candidate rule, hỏi:

1. Rule này có đặc thù cho repo không?
2. Nó có thay đổi quyết định khi code không?
3. Model có dễ vi phạm nó khi vibe coding không?
4. Vi phạm có gây inconsistency, bug hoặc maintenance cost rõ ràng không?

Nếu phần lớn câu trả lời là "không", bỏ rule.
