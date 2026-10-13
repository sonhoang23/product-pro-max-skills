# Runtime Lifecycle Profile

File này là phase-aware router cho từng Risk ID. Nó không thay thế category detail.

Stage order: `requirements → design → tasks → implementation`.

| Risk ID | Earliest detectable stage | Requirement implication | Design prevention |
|---|---|---|---|
| WEB-ROUTE-001 | requirements | Định nghĩa usable entry/deep-link behavior cho user-facing surface. | Map route tree/base path/redirect/deploy entry và verification entrypoint. |
| AUTH-INTEGRATION-001 | design | Auth propagation là technical; spec chỉ cần actor/permission behavior. | Chốt principal/session/token propagation tới protected API và authenticated proof. |
| AUTH-002 | requirements | Phân biệt unauthenticated, unauthorized và missing-resource behavior khi user-visible. | Map guard/fail-closed semantics theo principal/permission. |
| UI-001 | design | Spec chỉ cần accessibility/navigation semantics. | Giữ native semantic element/accessible role khi compose primitive. |
| BROWSER-001 | tasks | Không đưa browser payload/executable vào requirement. | Materialize và launch browser runtime trước product QA. |
| BROWSER-002 | requirements | Acceptance journey phải liệt kê đủ business steps. | Map từng step tới browser evidence; tách device/locale matrix khỏi journey coverage. |
| BROWSER-003 | requirements | Chốt operating-timezone/civil-date semantics khi user-visible. | Chốt timezone authority, conversion boundary, cross-timezone proof. |
| UI-002 | requirements | Mô tả sequential typing/editing behavior nếu live formatting là UX contract. | Bảo toàn caret/selection, canonical form state và submit payload. |
| UI-003 | requirements | Không lộ raw internal ID ở selected state. | Giữ stable human-readable label/optimistic option trong async lifecycle. |
| UI-004 | design | Spec chỉ định empty/optional behavior; schema compatibility thuộc design. | Thống nhất controlled blank value, schema và serialized payload. |
| UI-005 | requirements | Closed selector phải hiển thị user-facing label. | Tách canonical value khỏi display label; label không phụ thuộc current page. |
| UI-006 | requirements | Định nghĩa empty/partial/complete và không mất partial input âm thầm. | Validate/transform để partial input bị chặn rõ hoặc persist đúng contract. |
| UI-007 | requirements | Định nghĩa dependent surfaces phải hội tụ sau confirmed write và recovery nếu chưa hội tụ. | Dependency family, convergence window, invalidation/refetch, syncing/retry semantics. |
| UI-008 | requirements | Phân biệt write result với post-write read-sync result và retry. | Tách mutation state khỏi read-sync; retry read không resend confirmed write. |
| UI-009 | requirements | Chốt latest server-confirmed truth khi completion lệch thứ tự. | Request/version/cancellation/cache strategy chống older response overwrite. |
| UI-010 | requirements | Định nghĩa editable vs locked, lý do khóa và race/history behavior. | Capability→affordance/editability + recovery giữ draft phần còn hợp lệ. |
| UI-011 | requirements | Định nghĩa discoverability khi collection vượt page size. | Pagination/load-more/server search/order/selected-label strategy. |
| UI-012 | requirements | Định nghĩa confirm completion, focus recovery, accessible feedback. | Giải phóng modal/focus/inert boundary đúng lifecycle. |
| BROWSER-004 | requirements | Chốt viewport/device flow bắt buộc nếu mobile là operational surface. | Verify cùng business outcome trên target viewport, scroll/overflow/touch/actions. |
| API-001 | design | Generated artifact mechanics không thuộc spec. | Chốt canonical source, runtime revision, stable generation window, consumer verification. |
| API-002 | design | Spec giữ public contract semantics. | Đảm bảo generated schema identity duy nhất và consumer type đúng. |
| API-003 | design | Spec chỉ giữ nullable/union business semantics nếu domain-visible. | Schema metadata đủ để generator không làm méo type. |
| API-004 | design | Spec chỉ giữ externally observable status semantics. | Override framework default để status khớp contract. |
| INTEGRATION-001 | requirements | Structured field error phải quay về đúng editable control và giữ input. | Bảo toàn field identity/code/path qua transport/adaptor. |
| API-005 | requirements | Domain rule phải định nghĩa semantic-valid date khi calendar validity có ý nghĩa. | Validate semantic date và proof create→read-back→consumer render. |
| API-006 | design | Spec giữ canonical error behavior. | Map có chủ đích domain/business error; không catch-all system error thành 4xx. |
| API-007 | design | Spec giữ transport requirement như header/idempotency nếu user/domain-visible; generated client mechanics không thuộc spec. | Dùng generated operation signature làm authority cho path/query/header/body; không hand-edit generated artifact. |
| API-008 | design | Spec chỉ cần phân biệt omitted/null/value khi semantics user/domain-visible. | Bảo toàn field-presence semantics qua DTO transform và verify omitted/null/value qua transport pipeline. |
| DB-001 | design | DB runtime config không thuộc spec. | Chốt config authority giữa app/migration/test/runtime. |
| DB-002 | design | Spec chỉ giữ migration behavior nếu domain-visible. | Chốt journal/snapshot/SQL chain, ordering và freshness. |
| DB-003 | tasks | Test DB isolation không thuộc spec. | Isolate/serialize mutable DB; full-suite deterministic rerun. |
| ENV-001 | tasks | Setup script mechanics không thuộc requirement. | Treat install/setup as mutating; snapshot env và smoke dependency. |
| ENV-002 | design | Spec chỉ giữ supported-platform requirement. | Kiểm native dependency tương thích runtime/OS/arch. |
| ENV-003 | design | Spec chỉ giữ supported-platform behavior. | Tránh path-separator assumption; verify supported platform semantics. |
| ENV-004 | tasks | Relink/install side effect không thuộc spec. | Snapshot manifest/lock/bin/env trước-sau và rerun canonical verification. |
| ENV-005 | implementation | Không tạo requirement từ OS file-lock incident. | Phân loại file-lock/environment cleanup trước product regression. |
| STARTUP-001 | tasks | Port/process identity không thuộc spec. | Start/bind target, xác minh process/revision và capability-specific probe. |
| VERIFY-001 | tasks | Package-script forwarding không thuộc spec. | Resolve canonical command/wrapper args/binary/mode/target/final exit. |
| VERIFY-002 | implementation | Orchestrator cancellation không tạo product requirement. | Tách primary failure, collateral cancellation, independent failure. |
| VERIFY-003 | implementation | Evidence freshness không thuộc spec. | Invalidate affected PASS sau source/config/artifact mutation. |
| VERIFY-004 | implementation | Warning classification thuộc verification. | Unexpected warning phải được phân loại; exit 0 chưa đủ clean PASS. |
| VERIFY-005 | tasks | jsdom/test-library mechanics không thuộc spec. | Interaction/query phản ánh accessible/runtime behavior + browser proof khi cần. |
| VERIFY-006 | tasks | Provider-rerender mechanics không thuộc requirement. | Rerender giữ provider/store identity theo test contract. |
| VERIFY-007 | tasks | jsdom responsive limitation không thuộc requirement. | Scope DOM assertion; browser viewport proof cho visibility. |
| VERIFY-008 | tasks | Fixture/helper mechanics không thuộc spec. | Assert setup/precondition fail-fast trước downstream behavior. |
| VERIFY-009 | tasks | Mock lifecycle không thuộc spec. | Mirror consumed exports, reset mock state, full-file order-dependence proof. |
| VERIFY-010 | tasks | Runner capacity/parallelism không thuộc spec. | Phân loại OOM/allocator failure là verification infrastructure, rerun bounded concurrency và pin canonical command khi cần. |

## Quy tắc sử dụng

- Stage là thời điểm sớm nhất có đủ authority/evidence để xử lý pattern, không phải phase duy nhất pattern được dùng.
- Caller stage sớm hơn MUST defer pattern stage sau.
- Requirement implication không được dùng để invent behavior; chỉ kiểm xem spec có cần quy định consequence đã được feature signal hỗ trợ hay không.
- Design prevention chỉ có authority khi đã materialize vào `plan.md`/technical artifacts.
