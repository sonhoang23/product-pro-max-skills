# API / Service Integration Failure Patterns

Prefix chính: `API-*`, `INTEGRATION-*`

Dùng cho failure pattern tại boundary frontend↔API hoặc service↔service như transport, base URL, CORS, serialization, generated contract hoặc runtime schema.

---

## API-001 — Generated API contract stale, lấy từ sai runtime revision hoặc chưa được lưu canonical

**Applies when**

Frontend/consumer dùng generated types/SDK/schema lấy từ API đang chạy hoặc OpenAPI endpoint.

**Symptom**

Consumer typecheck xuất hiện hàng loạt lỗi không khớp endpoint/field mới; generator báo success nhưng output vẫn schema cũ; local typecheck pass sau generation nhưng CI/repo khác vẫn thấy contract cũ vì artifact chưa commit.

**General root cause**

Generated artifact không cùng revision với source API: runtime stale/wrong process, generation chưa chạy sau API change, hoặc artifact mới chỉ tồn tại local.

**Why tests miss it**

Backend tests có thể pass độc lập; generator chỉ chứng minh endpoint reachable, không chứng minh đúng revision; local generated file có thể che việc source control vẫn stale.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. snapshot revision + working-tree state và start/verify đúng API revision/readiness;
2. probe một schema/endpoint mới đại diện;
3. xác minh revision/working-tree vẫn ổn định ngay trước generation; nếu watcher/concurrent workflow đã sửa source thì dừng và đánh dấu run contaminated;
4. generate artifact;
5. review diff theo capability mong đợi và phát hiện field ngoài scope;
6. chạy consumer typecheck/test;
7. commit/save generated artifact nếu repo track nó;
8. xác minh revision + working-tree state sau generation và final HEAD thực sự chứa artifact mới, không còn generated diff local chưa lưu.

**Required evidence**

Runtime đúng revision, working tree ổn định xuyên suốt probe/generation, generated diff chỉ chứa capability hợp lệ mong đợi, consumer verification pass, canonical source-control state chứa artifact mới, và final revision/HEAD được đối chiếu lại sau commit. Source đổi giữa run hoặc artifact lẫn field từ concurrent feature phải bị coi CONTAMINATED/STALE. Generator success một mình không phải PASS.

---

## API-002 — OpenAPI/component schema name collision làm consumer nhận nhầm type

**Applies when**

Nhiều module/context export DTO/class khác nhau nhưng có cùng component/schema name trong OpenAPI/serialization metadata.

**Symptom**

Generator cảnh báo duplicate schema hoặc endpoint A sinh type của DTO thuộc endpoint/context B dù JSON runtime khác.

**General root cause**

Schema registry dùng tên class/component toàn cục; hai DTO khác semantics dùng cùng tên nên definition bị overwrite/resolve nhầm.

**Why tests miss it**

Controller/E2E kiểm JSON runtime vẫn pass; lỗi nằm ở metadata/generated consumer contract.

**Task-generation rule**

Khi pattern áp dụng, task plan phải bảo đảm schema component names unique theo bounded context/capability khi semantics khác; generation phải fail/review khi có duplicate warning.

**Required evidence**

OpenAPI không còn duplicate component warning; generated endpoint reference đúng component; consumer typecheck/test pass không cần cast workaround.

---

## API-003 — Metadata nullable/union primitive không đủ làm generated type bị méo

**Applies when**

DTO/OpenAPI metadata mô tả field nullable/optional/union primitive và framework không suy type chính xác chỉ từ TypeScript.

**Symptom**

Field runtime là `string | null` nhưng generated type thành object rỗng, `Record<string, never>`, unknown hoặc union sai.

**General root cause**

Runtime reflection mất thông tin TypeScript union/nullability; decorator/schema thiếu explicit primitive `type`/format.

**Why tests miss it**

Backend runtime serialize đúng giá trị và E2E pass; lỗi chỉ xuất hiện sau OpenAPI generation/consumer compilation.

**Task-generation rule**

Khi pattern áp dụng, task plan phải explicit primitive type/format cho nullable/union field mà reflection không bảo toàn; regenerate contract và kiểm generated shape cụ thể.

**Required evidence**

Generated schema/type của field đúng primitive + nullability mong đợi và consumer typecheck pass không cần manual cast.

---

## API-004 — Framework default HTTP status lệch contract

**Applies when**

Endpoint dùng method/framework có default status khác status được contract/consumer/test yêu cầu, ví dụ command POST nhưng semantic response phải là 200.

**Symptom**

Business operation thành công nhưng E2E/client fail vì nhận 201 thay vì 200 hoặc status mặc định khác contract.

**General root cause**

Controller dựa vào framework default thay vì khai báo explicit status theo API contract.

**Why tests miss it**

Service/unit test không đi qua HTTP adapter; manual testing thường chỉ nhìn body/success.

**Task-generation rule**

Khi contract có status cụ thể khác framework default, task phải khai báo status explicit và E2E assert status + response body.

**Required evidence**

HTTP E2E trên route thật trả đúng status đã contract hóa.

---

## INTEGRATION-001 — Structured server field error bị mất mapping khi đi từ API về form

**Applies when**

API trả validation/business error có cấu trúc như Problem Details, error code, field path hoặc danh sách field errors và frontend có form/editable controls tương ứng.

**Symptom**

Server đã chỉ rõ field hoặc path sai nhưng UI chỉ hiện generic toast/form error như “Có lỗi xảy ra”, gắn lỗi nhầm field, hoặc làm mất chi tiết cần thiết để người dùng sửa. Input đã nhập có thể bị reset dù request thất bại.

**General root cause**

Transport/adaptor/mutation layer flatten structured server error thành một message chung, đổi/làm mất field path, hoặc form layer không có mapping ổn định từ API field identity sang editable control identity.

**Why tests miss it**

Backend E2E chỉ chứng minh structured error được trả đúng; frontend unit test thường mock generic reject; happy-path không exercise server-side validation. Vì vậy từng tầng đều có thể pass riêng nhưng end-to-end recovery UX vẫn hỏng.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định error contract có cấu trúc và canonical field path/code tại API boundary;
2. giữ nguyên semantic field identity qua client/adaptor/mutation layer, chỉ translate presentation message ở lớp UI;
3. map field-specific error về đúng editable field/group; generic form-level error chỉ dùng cho lỗi không thể map;
4. không reset user input khi mutation fail; pending/error state phải cho phép sửa và retry;
5. nested/array/dynamic field path phải có mapping deterministic, không dựa vào rendered label hoặc index dễ drift nếu identity domain đã có;
6. integration test phải inject ít nhất một structured server field error thật hoặc faithful contract fixture và assert đúng field nhận lỗi;
7. thêm retry-success path để chứng minh error state được clear đúng sau khi người dùng sửa.

**Required evidence**

Structured server error đi qua transport/client mà không mất code/path cần thiết; đúng editable control/group nhận semantic error state và message; form-level generic error chỉ xuất hiện khi không có field mapping; user input được giữ sau failure; sửa field và retry thành công mà không cần reload.
---

## API-005 — Shape-valid date được ghi vào database nhưng làm consumer crash

**Applies when**

Date-only value dùng dạng `YYYY-MM-DD` đi qua frontend → API DTO → service → database → API response → UI formatter, đặc biệt khi DTO chỉ dùng regex để kiểm tra format.

**Symptom**

Mutation tạo/cập nhật báo thành công, nhưng redirect sang trang chi tiết làm UI crash khi render date. Ví dụ response chứa `0002-09-08`; frontend formatter ném `Operating date is not a valid calendar date`.

**General root cause**

Shape validation nhận chuỗi đúng dạng nhưng không kiểm tra semantic calendar date và business year policy. Database vì thế nhận dữ liệu sai. Consumer tin response đã hợp lệ và crash khi format/render. JavaScript date APIs có edge case riêng, như xử lý năm `0–99` của `Date.UTC`, làm symptom khó truy nguyên hơn.

**Why tests miss it**

Fixture thường chỉ dùng ngày hợp lệ; DTO test chỉ cover regex; backend và frontend test chạy tách rời; không có round-trip browser flow `create → redirect → GET detail → render`. POST status thành công có thể làm verification dừng quá sớm.

**Task-generation rule**

Khi pattern áp dụng:
1. validate cả syntax và semantic calendar date ở DTO boundary;
2. validate lại ở service trước khi ghi database;
3. chốt business year range nếu domain không cho phép năm quá thấp;
4. kiểm database invariant nếu có nhiều write path;
5. test `2026-02-30`, `2026-13-01`, năm ngoài policy và ngày hợp lệ;
6. verify flow thật `write → database read-back → GET response → browser render`;
7. không coi redirect/routing là primary failure nếu request đã ghi domain data không hợp lệ;
8. sau khi source/config/data thay đổi, đánh dấu runtime evidence cũ là `STALE` và rerun gate liên quan.

**Required evidence**

Invalid date bị API từ chối trước database write; valid date được read-back đúng; không có row invalid trong database; browser smoke create → redirect → detail render pass; evidence ghi rõ API process/port, database target, command, revision, exit result và primary/collateral failure causality.


---

## API-006 — Domain/application exception leak làm transport error contract sai

**Applies when**

Application/service gọi domain value object/parser/validator có thể ném domain-specific exception, trong khi API boundary đã có canonical validation/business error contract như BadRequest/Problem Details/error code.

**Symptom**

Input invalid đúng nghĩa business nhưng request/unit test nhận raw domain exception/class/message, HTTP 500 hoặc error shape khác contract; frontend không map được field/form error ổn định.

**General root cause**

Boundary service không normalize domain exception sang application/transport error contract; implementation giả định mọi invalid input đã bị DTO chặn dù domain validator vẫn là authority cuối.

**Why tests miss it**

Happy-path không ném; DTO test và domain unit test đều đúng riêng lẻ; chỉ service/controller integration với invalid-but-shape-valid input mới lộ exception leak.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định canonical error contract ở application/transport boundary;
2. domain exception có nghĩa validation/business phải được map có chủ đích, không leak stack/type nội bộ;
3. giữ domain validator làm invariant authority, không bỏ validation để làm transport test pass;
4. test invalid input tại service/controller boundary và assert code/status/field mapping;
5. unknown/system exception vẫn phải propagate/500 theo policy, không catch-all thành 400.

**Required evidence**

Invalid domain input trả đúng status/error code/shape theo API contract; raw domain exception không leak ra consumer; frontend/integration mapping hoạt động; invariant domain vẫn được thực thi và unexpected exception không bị nuốt.


---

## API-007 — Generated client contract đúng nhưng consumer gọi sai transport shape

**Applies when**

Frontend/consumer dùng generated client/types từ OpenAPI/SDK có invocation shape riêng cho path/query/header/body, ví dụ header phải nằm trong `params.header` thay vì một field transport tự suy đoán như root `headers`.

**Symptom**

Backend route và generated contract đều đúng nhưng consumer typecheck/build fail tại mutation/request call; hoặc code ép cast để compile rồi request runtime thiếu header/path/query bắt buộc. Developer có thể bị cám dỗ hand-edit generated type vì raw HTTP semantics nhìn đúng nhưng client wrapper schema khác.

**General root cause**

Consumer suy invocation shape từ kiến thức HTTP/framework hoặc API client khác thay vì dùng contract của generated client đang cài. Generated transport abstraction phân tách path/query/header/body theo cấu trúc riêng, nên cùng một HTTP request có representation khác ở call site.

**Why tests miss it**

Backend unit/E2E không compile frontend consumer; mock mutation test có thể chỉ inspect business body và bỏ qua transport metadata; raw curl/Postman vẫn thành công nên dễ kết luận sai rằng generated contract có lỗi.

**Task-generation rule**

Khi pattern áp dụng:
1. đọc generated operation type/client signature hiện tại trước khi viết request call;
2. map path/query/header/body đúng vị trí mà generated client yêu cầu, không suy từ client/library khác;
3. không hand-edit generated artifact để làm consumer compile;
4. frontend typecheck/build phải cover call site;
5. interaction/integration test quan trọng phải assert transport metadata bắt buộc như idempotency/auth/custom headers ở đúng request boundary;
6. nếu generated type có vẻ sai, quay lại API-001/API-002/API-003 để xác minh generation trước khi workaround consumer.

**Required evidence**

Consumer typecheck/build pass không cần cast hoặc hand-edit generated file; request call giữ đúng generated invocation shape; integration/browser/network evidence cho thấy header/path/query/body bắt buộc thực sự đi ra request; generated artifact vẫn canonical và không có manual diff ngoài generation contract.


---

## API-008 — DTO transform làm mất semantics “field omitted” của partial update

**Applies when**

PATCH/partial-update contract phân biệt ít nhất một trong các trạng thái `field omitted`, `field = null` và `field = value`, trong khi framework/DTO/class-transformer có thể materialize optional property với giá trị `undefined` hoặc thay đổi object shape trước khi service xử lý.

**Symptom**

Client không gửi field nhưng backend vẫn coi field “có mặt” và thực hiện validation/update/replay-conflict logic; stale/idempotent replay có thể trả conflict sai, hoặc null/omit bị conflated dù raw request contract khác nhau.

**General root cause**

Application/service suy request-field presence từ property ownership của DTO đã transform (`hasOwnProperty`, enumerable shape hoặc class instance layout) thay vì semantics của transport contract. Sau transform, “property tồn tại với undefined” không còn đồng nghĩa “client đã gửi field”.

**Why tests miss it**

Service/unit test thường gọi plain object trực tiếp nên không đi qua validation/transform pipeline; happy-path API E2E gửi value thật nhưng thiếu matrix omitted/null/value nên không lộ khác biệt field presence.

**Task-generation rule**

Khi pattern áp dụng:
1. chốt contract cho `omitted` / `null` / `value` ở DTO/transport boundary;
2. không dùng property ownership của transformed DTO làm bằng chứng field đã xuất hiện trong raw request nếu transformer có thể materialize optional property;
3. dùng predicate phù hợp với contract (ví dụ `!== undefined` khi omitted map thành undefined), explicit presence metadata, raw-body field set hoặc DTO design bảo toàn presence;
4. service test và API E2E phải cover đủ matrix omitted/null/value cho field ảnh hưởng business/precondition semantics;
5. replay/idempotency/stale branch phải được kiểm riêng khi field presence quyết định “request có thay đổi state hay không”.

**Required evidence**

API E2E qua đúng framework validation/transform pipeline chứng minh: omitted không kích hoạt update ngoài contract, explicit null có semantics riêng nếu được hỗ trợ, explicit value được persist/validate đúng; service/transport tests thống nhất cùng behavior và replay/stale scenario không trả conflict chỉ vì transformed DTO chứa optional property `undefined`.
