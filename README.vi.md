# Product Pro Max Skills

<p align="center"><strong>From vibe to viable.</strong></p>

<p align="center">Hệ thống sản phẩm mã nguồn mở, dựa trên bằng chứng, dành cho những người xây sản phẩm bằng AI.</p>

## Tại sao

AI có thể biến ý tưởng thành phần mềm rất nhanh. Nhưng "chạy được" không đồng nghĩa với giải quyết đúng vấn đề, đủ an toàn, có UX tốt, có người dùng hay tạo được doanh thu.

Product Pro Max Skills giúp chuyển từ:

**Ý tưởng → Bằng chứng → Quyết định → Sản phẩm → Xác minh → Phân phối → Người dùng → Doanh thu → Học hỏi**

thay vì:

**Ý tưởng → Prompt → Code → Deploy**

Nguyên tắc chính:

- có bằng chứng rồi mới tăng mức độ tin cậy;
- chưa xác minh thì chưa được gọi là hoàn tất;
- người dùng quan trọng hơn số lượng tính năng;
- distribution là một phần của sản phẩm;
- STOP, PIVOT và DEFER đều là kết quả hợp lệ.

## MVP

MVP gồm 13 skill:

`idea-pressure-test`, `problem-validation`, `customer-research`, `market-landscape`, `icp-positioning`, `mvp-scope`, `ux-flow`, `architecture-plan`, `engineering-readiness`, `runtime-verification`, `launch-readiness`, `distribution-plan`, `pricing-experiment`.

Ba workflow:

- `workflows/idea-to-mvp`
- `workflows/pre-launch-audit`
- `workflows/idea-to-first-users`

## Mô hình lõi

```text
SKILL
  ↓
ARTIFACT
  ↓
EVIDENCE
  ↓
GATE
  ↓
DECISION
```

Tạo ra tài liệu chưa phải là tiến bộ. Tiến bộ xảy ra khi artifact giúp đưa ra quyết định tốt hơn và bằng chứng phía sau quyết định có thể kiểm tra được.

## Cài đặt

```bash
git clone https://github.com/sonhoang23/product-pro-max-skills.git
cd product-pro-max-skills
python scripts/install.py --target /duong-dan/project/.agents/skills --all
```

Logic skill dùng English làm canonical để tránh translation drift. Output cho người dùng phải theo ngôn ngữ người dùng yêu cầu.

## Trạng thái

**MVP / nền tảng v0.1.** Useful > Large.

## License

MIT.
