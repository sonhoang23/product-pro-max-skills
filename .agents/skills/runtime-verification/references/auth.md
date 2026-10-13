# Authentication Failure Patterns

Prefix chính: `AUTH-*`

Đọc file này khi feature có login/session/JWT/cookie, protected API hoặc auth handoff giữa các app/service.

---

## AUTH-INTEGRATION-001 — Frontend gọi protected API nhưng thiếu authentication context

**Applies when**

Frontend/user flow gọi API được bảo vệ bởi JWT/session/cookie/auth guard, đặc biệt khi login surface và consuming frontend là hai app/port/origin khác nhau.

**Symptom**

API route tồn tại và backend test pass nhưng runtime request từ frontend trả `401 Unauthorized` vì credential không được tạo, lưu, scope hoặc gửi đúng.

**General root cause**

Backend auth và frontend feature được kiểm thử riêng lẻ nhưng không có contract/task chứng minh auth handoff xuyên boundary từ login/session tới request thật của consuming app.

**Why tests miss it**

API E2E thường tự inject token/session; frontend test thường mock API. Hai tầng đều pass dù browser/client runtime chưa có credential hợp lệ.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. xác định unauthenticated behavior và auth entry/handoff mà user flow sử dụng;
2. xác minh cookie/token/session scope, credential transport và API client behavior phù hợp với architecture đã chọn;
3. thêm integration/runtime flow từ authentication → consuming frontend → protected request;
4. chứng minh authenticated happy path không thất bại vì thiếu credential;
5. không dùng việc tắt/bypass auth guard như cách mặc định để làm test/runtime xanh.

**Required evidence**

Một auth context được tạo theo flow dự kiến và consuming frontend/client thực hiện protected request thành công với credential thật của flow đó; unauthenticated request vẫn bị xử lý đúng policy.


---

## AUTH-002 — Xác thực hợp lệ nhưng thiếu quyền bị chẩn đoán nhầm thành route không tồn tại

**Applies when**

Frontend có role/permission guard hoặc fail-closed policy có thể dùng `404/notFound` để che tài nguyên khỏi user đã đăng nhập nhưng không đủ quyền; backend có thể dùng 403 cho cùng authorization boundary.

**Symptom**

Login/token/session hợp lệ nhưng user thấy trang 404 hoặc "not found"; cùng URL mở được với principal có role phù hợp. Agent dễ sửa router/path vì tưởng route không tồn tại dù root cause là authorization context.

**General root cause**

Authentication và authorization bị gộp thành một khái niệm; UI cố tình che permission failure bằng 404 nên symptom routing không phản ánh root cause quyền truy cập.

**Why tests miss it**

Auth test thường chỉ chứng minh login thành công; route smoke thường dùng admin fixture; router/component test có thể không chạy đủ principal matrix để phân biệt missing route với insufficient permission.

**Task-generation rule**

Khi pattern áp dụng:
1. ghi role/permission/claims của principal dùng cho browser/runtime proof, không chỉ trạng thái "đã login";
2. test route với ít nhất một authorized principal và một authenticated-but-unauthorized principal khi policy có ý nghĩa;
3. phân biệt unauthenticated behavior, authorization-denied behavior và route thật sự không tồn tại;
4. đối chiếu UI fail-closed status/copy với backend authorization semantics khi hai tầng dùng status khác nhau;
5. không sửa route hoặc bypass guard chỉ để biến 404 thành 200 trước khi xác minh principal.

**Required evidence**

Authorized principal truy cập route thành công; authenticated-but-unauthorized principal nhận đúng fail-closed behavior theo policy; unauthenticated behavior vẫn đúng; evidence ghi rõ role/permission context để một 404 do authorization không bị phân loại thành routing failure.
