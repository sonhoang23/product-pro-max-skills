# Quy tắc mô hình hóa dùng chung

## 1. Evidence trước suy diễn

Dùng ba trạng thái nội bộ:

- **[FACT]**: được hỗ trợ bởi artifact có thẩm quyền hoặc code/current state có thể kiểm chứng.
- **[PROPOSAL]**: cách biểu diễn/mô hình hóa được đề xuất, chưa phải requirement/decision.
- **[OPEN]**: thiếu thông tin hoặc có conflict cần xử lý upstream.

Không biến best practice thành requirement.

## 2. Phân biệt intended và current state

- Spec/plan/tasks mô tả **planned/intended state** và MAY đi trước code.
- Code/config/runtime đã qua verification mô tả **current implemented state**.
- `docs/` và project-level diagrams chỉ được mô tả implemented state đã được promote.
- Implementation/converge diagram có thể đặt planned và current cạnh nhau nhưng không được âm thầm hợp nhất.
- Khi current state khác intended state, ghi rõ drift; không tự sửa intended artifact từ code.

## 3. Functional / Structural / Behavioral

Khi phù hợp, kiểm tra cân bằng:

- Functional: actor, use case, capability, flow.
- Structural: domain concept, component, data relationship, ownership.
- Behavioral: sequence, state, lifecycle, runtime interaction.

Không cần đủ cả ba cho mọi artifact. Chỉ dùng model giúp làm rõ phase hiện tại.

## 4. Progressive disclosure

Không nạp toàn repo mặc định.

Đọc theo thứ tự:

1. artifact nguồn của phase;
2. constitution;
3. upstream artifact trực tiếp;
4. downstream/current-state evidence chỉ khi cần;
5. code/docs bổ sung khi cần kiểm chứng.

## 5. Không tạo lớp semantics song song

Không tạo `analysis/`, `system-model.md` hoặc bộ Markdown trung gian chỉ để phục vụ diagram.

Nếu modeling phát hiện source artifact thiếu:

- spec thiếu product semantics → quay lại spec/clarify;
- plan thiếu technical design → cập nhật plan;
- tasks thiếu dependency → cập nhật tasks;
- implementation lệch intended → cập nhật upstream hoặc tạo task fix;
- converge phát hiện gap → append task theo converge workflow.
