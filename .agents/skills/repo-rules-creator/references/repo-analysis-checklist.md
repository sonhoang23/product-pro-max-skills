# Repo Analysis Checklist

Dùng checklist này trước khi hoàn tất `<repo-name>-rules`.

## Evidence

- Đã đọc các tài liệu root quan trọng nếu tồn tại.
- Đã xem package/workspace/framework config.
- Đã kiểm tra cấu trúc source thay vì chỉ dựa vào README.
- Đã tìm business invariant trong code/docs liên quan.
- Với frontend, đã tìm design system/shared UI/theme/token.

## Documentation

- Đã tìm canonical development docs của repo.
- Nếu đã có nơi phù hợp như `development_specs/`, `docs/`, `architecture/`, đã dùng nơi đó thay vì tạo folder trùng vai trò.
- Nếu không có canonical development docs, đã tạo `development_specs/`.
- Repo rules nêu rõ canonical docs path.
- Có rule đọc docs trước thay đổi architecture/business/API contract lớn/design system.
- Có rule xử lý rõ docs/code conflict và docs stale.
- Có rule yêu cầu thay đổi lớn cập nhật docs ngắn gọn; không ép update docs cho bugfix nhỏ.

## Rule quality

- Mỗi rule ảnh hưởng trực tiếp đến quyết định khi code.
- Rule đặc thù repo, không phải lời khuyên chung chung.
- Không có hai rule nói cùng một ý.
- Không biến dependency list thành rules.
- Không bịa convention chưa có bằng chứng.

## Frontend

- Có rule reuse component nếu repo có shared UI.
- Có rule dùng token/theme nếu repo có design token.
- Không khuyến khích inline CSS/hard-code style trái convention.
- Không tạo component mới khi có thể reuse hoặc compose component hiện có.
- Rule phản ánh pattern UI thật của repo.

## Context efficiency

- `SKILL.md` ưu tiên khoảng 80–150 dòng hoặc ngắn hơn.
- Rule thường chỉ 1–3 dòng.
- Không copy nguyên README/docs.
- Chi tiết hiếm dùng đã chuyển sang `references/` nếu cần.
- Không tạo reference chỉ để làm cấu trúc trông đầy đủ.

## Output

- Tên skill theo `<repo-name>-rules` và kebab-case.
- `name:` trùng tên folder.
- `description` nói rõ skill làm gì và khi nào trigger.
- Chỉ giữ các heading có giá trị.
- Path/reference không hỏng.
- Chạy validator của repo nếu có.

## Final question

Sau khi model chỉ đọc `SKILL.md`, liệu nó có tránh được những lỗi vibe coding dễ xảy ra nhất của repo này và giữ docs/code đồng bộ sau thay đổi lớn không?

Nếu chưa, bổ sung đúng rule còn thiếu; không kéo dài bằng giải thích chung chung.
