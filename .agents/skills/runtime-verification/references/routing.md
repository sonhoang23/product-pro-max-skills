# Routing / Entrypoint Failure Patterns

Prefix chính: `WEB-ROUTE-*`

Đọc file này khi feature tạo hoặc thay đổi frontend route tree, base URL, redirect, entry flow hoặc deep link.

---

## WEB-ROUTE-001 — Deployable frontend không có usable entrypoint

**Applies when**

Feature tạo hoặc thay đổi một frontend/app deployable có base URL, route tree hoặc entry flow cho người dùng.

**Symptom**

Process/dev server chạy bình thường nhưng URL người dùng mở đầu tiên trả `404/500`, hoặc base URL không dẫn tới route sử dụng được khiến hệ thống bị hiểu nhầm là hỏng.

**General root cause**

Route chức năng tồn tại nhưng entrypoint không được khai báo/implement/redirect nhất quán với cách app được khởi chạy và tài liệu sử dụng.

**Why tests miss it**

Component test hoặc route-specific test thường mở trực tiếp route hợp lệ như `/projects` nên không bao giờ probe base URL/entry URL mà người dùng thực tế mở.

**Task-generation rule**

Khi pattern áp dụng, task plan phải:
1. xác định expected entry behavior của app: base route render, redirect, hoặc một explicit entry URL được công bố;
2. implement route/redirect/config tương ứng;
3. thêm smoke/runtime check cho entry URL và critical deep link để unexpected `404/500` bị phát hiện;
4. đặt task trong phase tạo frontend/router, không chờ phase polish cuối.

**Required evidence**

App/process được start theo command dự kiến và entry URL thực tế trả behavior đã định nghĩa; critical route truy cập được mà không có unexpected `404/500`.
