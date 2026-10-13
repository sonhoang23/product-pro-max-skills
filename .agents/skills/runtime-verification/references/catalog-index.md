# Runtime Failure Catalog Index

File này chỉ làm **router/index**. Không lưu failure pattern chi tiết ở đây.

## Cách dùng

1. Xác định lifecycle mode của caller.
2. Đọc `lifecycle-profile.md` và lọc Risk ID có earliest stage phù hợp; pattern stage sau được defer.
3. Xác định runtime surface từ spec/plan/architecture.
4. Match surface với category bên dưới.
5. Chỉ mở category file liên quan và đúng Risk ID cần đánh giá.
6. Chỉ mở thêm category khác khi feature thực sự có boundary tương ứng.

## Category map

| Category | Prefix chính | File | Khi nào đọc |
|---|---|---|---|
| Routing / entrypoint | `WEB-ROUTE-*` | `routing.md` | Frontend route tree, base URL, redirect, deep link |
| Authentication | `AUTH-*` | `auth.md` | Login/session/JWT/cookie/protected API |
| UI / browser runtime | `UI-*`, `BROWSER-*` | `ui-browser.md` | Hydration, browser console, rendering, interaction |
| API / service integration | `API-*`, `INTEGRATION-*` | `api-integration.md` | Frontend↔API, service↔service, CORS/contract transport |
| Database runtime | `DB-*` | `database.md` | Migration, schema, seed, connection, transaction runtime |
| Environment / startup | `ENV-*`, `STARTUP-*` | `environment.md` | Env var, port, base URL, startup/readiness/config |
| Worker / queue | `WORKER-*`, `QUEUE-*` | `worker-queue.md` | Background job, claim, retry, scheduler, consumer |
| Storage / assets | `STORAGE-*`, `ASSET-*` | `storage-assets.md` | File/object storage, asset path, upload/download/runtime asset |
| External services | `EXTERNAL-*` | `external-services.md` | Third-party API/service/dependency runtime |
| Verification / tooling | `VERIFY-*` | `verification-tooling.md` | Test runner, package-script wrapper, monorepo orchestrator, evidence provenance/cancellation |

## Quy tắc chung

- Risk ID phải ổn định, không renumber sau khi đã xuất hiện trong `tasks.md`.
- Mỗi pattern detail phải có: **Applies when**, **Symptom**, **General root cause**, **Why tests miss it**, **Task-generation rule**, **Required evidence**.
- Metadata phase-aware theo từng Risk ID nằm trong `lifecycle-profile.md`: **Earliest detectable stage**, **Requirement implication**, **Design prevention**.
- Không coi pattern stage sau là N/A chỉ vì artifact stage hiện tại chưa có technical detail.
- Không tạo category mới chỉ vì một bug đơn lẻ; ưu tiên boundary kỹ thuật ổn định, dùng được xuyên project.
- Không coi file category trống là risk áp dụng. Chỉ pattern đã được định nghĩa mới tham gia Runtime Risk Inventory.


## Ownership

Catalog trong thư mục này thuộc canonical skill tại `sonhoang23/oh-my-skill@main:skills/runtime-verification`.

Bản copy ở các repo consumer không được trở thành fork tri thức lâu dài. Pattern reusable phát hiện ở repo consumer phải được promote về canonical trước, sau đó sync canonical xuống các repo cần dùng.
