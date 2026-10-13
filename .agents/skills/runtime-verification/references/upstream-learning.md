# Upstream Learning & Sync

## Source of truth

Canonical source:

`sonhoang23/oh-my-skill@main:skills/runtime-verification`

Các repo khác chỉ giữ consumer copy.

## Khi gặp lỗi mới

`runtime bug → root cause → reusable?`

- Không reusable → fix local, không update upstream.
- Đã có pattern → dùng pattern hiện có; update canonical chỉ khi lesson mới cải thiện rule/evidence.
- Pattern reusable mới → update đúng category ở canonical và commit thẳng `main`.

## Direct-to-main workflow

1. Đọc `main` mới nhất.
2. Đọc `catalog-index.md` và category liên quan.
3. Kiểm tra duplicate/overlap.
4. Viết/generalize pattern.
5. Bump version.
6. Xác minh có quyền ghi canonical repo. Nếu không có quyền, trả `BLOCKED`; không sửa consumer copy để thay thế canonical.
7. Commit trực tiếp `main` theo fast-forward; không force-push.
8. Sync canonical skill xuống repo đang làm việc.

## Sync consumer

Không cherry-pick từng file catalog. Thay toàn bộ thư mục skill từ canonical.

Trước khi replace, kiểm tra local-only changes. Nếu đó là reusable lesson chưa upstream thì promote trước.

Repo-specific integration như chỉnh `speckit-tasks-vi`, constitution hoặc hook phải nằm ngoài thư mục canonical skill và không bị sync overwrite.


## Khi không có quyền ghi upstream

Nếu agent/repo consumer không có quyền ghi `sonhoang23/oh-my-skill`:

- giữ kết quả ở trạng thái `BLOCKED` hoặc Runtime Lesson Candidate;
- báo rõ canonical update chưa thực hiện;
- không tạo một catalog local song song;
- không coi consumer copy là source of truth;
- chỉ sync xuống sau khi canonical upstream thực sự được cập nhật.
