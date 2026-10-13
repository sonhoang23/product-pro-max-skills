# Database Runtime Failure Patterns

Prefix chính: `DB-*`

Dùng cho failure pattern liên quan connection, migration, schema drift, seed, transaction hoặc dữ liệu runtime bắt buộc.

---

## DB-001 — Database runtime config khác config mà verification giả định

**Applies when**

App/migration/E2E dùng database URL/credential từ `.env`, secret hoặc nhiều package-local env file.

**Symptom**

Migration/test fail authentication/connection dù database đang chạy; hoặc một command database pass nhưng app/E2E dùng credential/database khác và fail.

**General root cause**

Nhiều nguồn config bị lệch, env bị reset, hoặc verification kiểm một package nhưng runtime khác đọc file/env khác.

**Why tests miss it**

Static checks không xác minh credential; test có thể dùng mock/in-memory DB hoặc một config source khác.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. xác định canonical runtime DB config cho từng deployable/package;
2. kiểm các env source có cùng target mong muốn;
3. chạy connection/migration smoke bằng chính config runtime;
4. sau setup/install có khả năng mutate env, re-check DB config trước E2E.

**Required evidence**

Migration/connection và app/E2E cùng kết nối đúng database target với config đã xác định; không dựa vào việc “database process đang chạy” như bằng chứng đủ.

---

## DB-002 — Migration journal/snapshot/SQL chain bị drift

**Applies when**

Migration tool duy trì journal/metadata/snapshot cùng các migration SQL/file tuần tự.

**Symptom**

Migrate báo thiếu migration file; generator nhảy số bất thường; journal tham chiếu file không tồn tại; snapshot/SQL không khớp; tiếp tục generate tạo thêm migration dựa trên chain đã hỏng.

**General root cause**

Migration metadata và filesystem/source control không còn cùng một lịch sử canonical do file bị xóa, artifact local chưa commit, restore không đầy đủ hoặc generate tiếp trên journal lỗi.

**Why tests miss it**

Schema source/typecheck vẫn hợp lệ; lỗi chỉ lộ khi migration tool đọc toàn chain hoặc apply vào DB thật.

**Task-generation rule**

Trước khi generate migration, task plan phải:
1. kiểm working tree migration và journal/snapshot chain;
2. xác minh mọi journal entry có artifact tương ứng theo contract tool;
3. nếu chain hỏng, khôi phục baseline canonical trước; không generate tiếp để “đi qua” số lỗi;
4. generate một lần từ baseline sạch;
5. review destructive SQL/constraint ngoài authority;
6. apply migration vào DB thật;
7. chạy migrate lần hai hoặc equivalent để kiểm idempotent/no-pending state.

**Required evidence**

Journal/snapshot/SQL chain nhất quán và tracked; generated migration được review; apply thành công; rerun không tạo/apply thay đổi ngoài dự kiến.

---

## DB-003 — Shared mutable E2E database gây cross-test contamination

**Applies when**

Nhiều E2E file/worker hoặc nhiều test case tuần tự dùng chung một PostgreSQL/schema/database hay cùng mutable fixture state. Pattern đặc biệt nguy hiểm khi một test đọc aggregate toàn hệ thống trong lúc test khác mutate cùng nguồn dữ liệu, hoặc test sau ngầm dựa vào baseline mà test trước đã thay đổi.

**Symptom**

Cùng một commit nhưng E2E lúc pass lúc fail; count/aggregate lệch nhỏ không ổn định; rerun riêng file thường pass trong khi chạy full suite có thể fail; hoặc một test case chỉ fail khi chạy sau case trước vì default/config/fixture đã bị mutate và không được restore.

**General root cause**

Test isolation chỉ đảm bảo dữ liệu fixture có tên/id khác nhau nhưng không cô lập shared database state. Read model/aggregate toàn hệ thống vẫn nhìn thấy mutation từ suite khác; với case tuần tự, prerequisite/baseline bị dùng như state ngầm của test file thay vì được seed/reset rõ ràng cho từng case.

**Why tests miss it**

Unit test/repository test không tái hiện shared mutable state giống E2E; một lần rerun xanh có thể che race hoặc order-dependence. Fixture prefix không đủ nếu assertion phụ thuộc global count, shared source set hoặc default/config bị test trước thay đổi.

**Task-generation rule**

Khi pattern áp dụng, task plan phải chọn và ghi rõ một chiến lược isolation:
1. database/schema riêng cho mỗi worker/test file; hoặc
2. transaction rollback/savepoint đủ cô lập; hoặc
3. fixture/query scope không phụ thuộc global mutable state; hoặc
4. serialize các E2E file dùng shared database khi read model aggregate toàn hệ thống; hoặc
5. với test tuần tự reuse cùng entity/config, seed/reset prerequisite trong `beforeEach`/setup của chính case hoặc tạo fixture riêng thay vì phụ thuộc state case trước.

Không sửa assertion thành khoảng/loose match chỉ để né race/order-dependence nếu contract yêu cầu kết quả deterministic.

**Required evidence**

Full E2E suite chạy với chiến lược isolation đã chọn và pass deterministic; rerun ít nhất một lần hoặc có equivalent evidence chứng minh không còn cross-file contamination. Với sequential shared-fixture case, test phải pass khi chạy riêng, chạy full file và khi thay đổi order/rerun nhóm stateful liên quan. Nếu serialize file, log/config phải cho thấy file parallelism thực sự bị tắt cho suite liên quan.
