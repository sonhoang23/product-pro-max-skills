# Product Pro Max Skills

<p align="center"><strong>From vibe to viable.</strong></p>

<p align="center">Hệ thống sản phẩm mã nguồn mở, dựa trên bằng chứng, dành cho những người xây sản phẩm bằng AI.</p>

<p align="center">
  <a href="./PRODUCT-MODEL.md">Product Model (English canonical)</a> ·
  <a href="./README.md">English</a>
</p>

## Tại sao

AI có thể biến ý tưởng thành phần mềm rất nhanh. Nhưng "chạy được" không đồng nghĩa với giải quyết đúng vấn đề, đủ an toàn, có UX tốt, có người dùng hay tạo được doanh thu.

Product Pro Max Skills giúp chuyển từ:

**Ý tưởng → Bằng chứng → Quyết định → Sản phẩm → Xác minh → Phân phối → Người dùng → Doanh thu → Học hỏi**

thay vì:

**Ý tưởng → Prompt → Code → Deploy**

## Product Model canonical

Toàn bộ lifecycle dùng một nguồn machine-readable duy nhất:

`model/product-model.json`

Giải thích dành cho con người nằm tại [`PRODUCT-MODEL.md`](./PRODUCT-MODEL.md).

README, schema, workflow, example, diagram và bản dịch chỉ là các view dẫn xuất; không được tự tạo định nghĩa lifecycle cạnh tranh.

Các machine ID luôn giữ nguyên tiếng Anh, ví dụ:

`opportunity`, `go-to-market`, `ppmax-runtime-verification`, `pass`, `pivot`.

Nhãn hiển thị cho người dùng có thể được dịch.

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

Gate và decision là hai khái niệm khác nhau:

- gate đánh giá mức độ đủ của bằng chứng/readiness: `pass`, `warn`, `fail`;
- decision quyết định bước tiếp theo, ví dụ `continue`, `research`, `revise`, `pivot`, `defer`, `stop`.

## MVP

MVP gồm 13 skill:

`ppmax-idea-pressure-test`, `ppmax-problem-validation`, `ppmax-customer-research`, `ppmax-market-landscape`, `ppmax-icp-positioning`, `ppmax-mvp-scope`, `ppmax-ux-flow`, `ppmax-architecture-plan`, `ppmax-engineering-readiness`, `ppmax-runtime-verification`, `ppmax-launch-readiness`, `ppmax-distribution-plan`, `ppmax-pricing-experiment`.

Ba workflow:

- `workflows/idea-to-mvp`
- `workflows/pre-launch-audit`
- `workflows/idea-to-first-users`

## Cài đặt

```bash
git clone https://github.com/sonhoang23/product-pro-max-skills.git
cd product-pro-max-skills
python scripts/install.py --target /duong-dan/project/.agents/skills --all
```

## Project state

Project state canonical dùng:

- `cycle`
- `phase`
- `status`

Giá trị hợp lệ lấy từ `model/product-model.json`, không lấy từ bản dịch.

## Ngôn ngữ

English là canonical cho logic skill, shared product semantics và machine identifier. Output gửi người dùng theo ngôn ngữ người dùng yêu cầu.

## Trạng thái

**MVP / nền tảng v0.1.**

Các foundation tiếp theo được quản lý trong `specs/ROADMAP-foundation.md`.

## License

MIT.
