# Product Pro Max Skills

<p align="center">
  <img src="./assets/brand/hero-process.webp" width="1200" alt="Product Pro Max Skills — From vibe to viable. An illustrative product cycle: Discover, Define, Build, Verify, Launch and Improve, with continuous learning.">
</p>

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


### Thứ tự điều hướng lifecycle

Số thứ tự chỉ dùng để hiển thị trong README, theo thứ tự cycle ở `model/product-model.json`. Không thay đổi canonical ID, tên thư mục hay đường dẫn registry.

| STT | Cycle |
| --- | --- |
| 01 | `opportunity` |
| 02 | `product-strategy` |
| 03 | `product-definition` |
| 04 | `delivery` |
| 05 | `verification` |
| 06 | `go-to-market` |
| 07 | `growth` |
| 08 | `operations` |
| 09 | `learning-evolution` |
| 10 | `end-of-life` |

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

## Catalog hiện tại — chỉ có nền tảng

**0 skill được phát hành.** 13 skill khởi tạo mang tính demo đã được gỡ khỏi `skills/` để xây dựng lại theo từng cycle và phase. Có thể tham khảo phiên bản cũ trong Git history và hồ sơ migration lịch sử của Spec 002; không được coi các skill này còn khả dụng.

Giữ đủ 10 thư mục cycle, chưa chốt số lượng skill cuối cùng. Skill mới cần phân tích khoảng trống năng lực, tuân thủ contract, có evidence và được đánh giá trước khi phát hành.

Ba workflow `idea-to-mvp`, `pre-launch-audit`, `idea-to-first-users` được **tạm ngừng**: chỉ giữ README làm tài liệu tham khảo, không còn `workflow.yaml` để chạy.

Xem [quyết định dọn catalog](./docs/CATALOG-RESET.md).

## Khám phá skill canonical

Khi được phát hành, các skill phân phối được nhóm tại `skills/<primary-cycle>/ppmax-<slug>/`. Mỗi skill có `SKILL.md` chứa hành vi và `manifest.yaml` chứa metadata khám phá. Các cycle bổ sung được khai báo trong manifest, không suy ra chỉ từ thư mục.

`registry/skills.json` được sinh từ manifest và không chỉnh thủ công. Chạy `python scripts/generate_skill_registry.py check` để phát hiện drift; `.agents/` chỉ chứa công cụ phát triển repo, không thuộc catalog phân phối.

## Cài đặt

Installer vẫn được giữ để sử dụng về sau. Hiện không có skill chính thức để cài; `--all` trả về trạng thái không có skill, không tạo dữ liệu.

```bash
git clone https://github.com/sonhoang23/product-pro-max-skills.git
cd product-pro-max-skills
python scripts/install.py --target /duong-dan/project/.agents/skills --all --dry-run
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

**Đang hoàn thiện nền tảng và xây lại catalog.** Product Model, manifest registry, design system và công cụ kiểm tra được giữ nguyên. Hiện có **0 skill phân phối / 0 workflow thực thi**. Báo cáo nghiệm thu 13 skill trong Spec 002 là dữ liệu lịch sử.

Các foundation tiếp theo được quản lý trong `specs/ROADMAP-foundation.md`.

## License

MIT.
