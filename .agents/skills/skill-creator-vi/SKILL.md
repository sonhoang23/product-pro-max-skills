---
name: skill-creator-vi
description: >-
  Tạo skill mới, chỉnh sửa và cải thiện skill hiện có, đồng thời đo hiệu quả của skill. Dùng khi người dùng muốn tạo skill từ đầu, chỉnh hoặc tối ưu một skill, chạy eval để kiểm thử, benchmark hiệu năng với phân tích độ biến thiên, hoặc tối ưu description để skill trigger chính xác hơn. Skill này hướng dẫn toàn bộ vòng lặp từ làm rõ ý định, viết bản nháp, tạo test case, chạy bản có skill và baseline, chấm kết quả, lấy phản hồi rồi lặp lại cho đến khi đạt yêu cầu.
---

# Skill Creator VI

Skill dùng để tạo skill mới và cải thiện skill theo vòng lặp.

Ở mức tổng quát, quy trình là:

- xác định skill cần làm gì và cách nó nên hoạt động;
- viết bản nháp;
- tạo một vài test prompt rồi chạy tác vụ với skill;
- giúp người dùng đánh giá kết quả cả định tính lẫn định lượng;
  - trong khi các lần chạy đang thực hiện, soạn eval định lượng nếu chưa có; nếu đã có thì dùng lại hoặc chỉnh khi thật sự cần;
  - dùng `eval-viewer/generate_review.py` để người dùng xem output và metric;
- viết lại skill dựa trên phản hồi và các vấn đề rõ ràng từ benchmark;
- lặp lại cho đến khi đạt yêu cầu;
- mở rộng test set và thử ở quy mô lớn hơn.

Nhiệm vụ khi dùng skill này là xác định người dùng đang ở đâu trong quy trình rồi tiếp tục từ đó. Nếu họ mới nói “tôi muốn tạo skill cho X”, hãy giúp làm rõ mục tiêu, viết bản nháp, tạo test case, xác định tiêu chí đánh giá, chạy thử và lặp. Nếu họ đã có bản nháp, có thể đi thẳng vào phần eval và cải thiện.

Quy trình linh hoạt. Nếu người dùng nói họ không cần một vòng benchmark đầy đủ và chỉ muốn làm nhanh theo kiểu “vibe”, có thể bỏ bớt phần eval theo mong muốn của họ.

Sau khi skill đã ổn, có thể dùng script cải thiện description để tối ưu khả năng trigger.

## Giao tiếp với người dùng

Người dùng skill-creator có mức độ quen thuộc kỹ thuật rất khác nhau. Điều chỉnh cách diễn đạt theo tín hiệu trong ngữ cảnh.

Mặc định:

- `evaluation` và `benchmark` có thể dùng, nhưng nên giải thích ngắn nếu cần;
- với `JSON` hoặc `assertion`, chỉ dùng như thuật ngữ hiển nhiên khi người dùng cho thấy họ hiểu; nếu không, giải thích bằng một câu ngắn.

Không biến quy trình kỹ thuật thành rào cản. Mục tiêu là giúp người dùng hiểu họ cần quyết định gì và bước tiếp theo là gì.

---

## Tạo một skill

### Thu thập ý định

Bắt đầu bằng việc hiểu chính xác người dùng muốn gì. Nếu cuộc trò chuyện hiện tại đã chứa workflow cần đóng gói thành skill, hãy trích xuất thông tin từ lịch sử trước: tool đã dùng, thứ tự bước, các lần người dùng sửa yêu cầu, input/output format đã xuất hiện. Chỉ hỏi phần còn thiếu và để người dùng xác nhận trước khi chuyển sang bước tiếp theo khi việc xác nhận thực sự cần thiết.

Làm rõ bốn điểm:

1. Skill cần giúp agent làm được gì?
2. Khi nào skill nên trigger — cụm từ, ngữ cảnh hay loại yêu cầu nào?
3. Output format mong đợi là gì?
4. Có nên tạo test case để xác minh skill không?

Skill có output khách quan, dễ kiểm chứng như chuyển đổi file, trích xuất dữ liệu, sinh code hoặc workflow cố định thường có lợi từ test case. Skill thiên về chủ quan như phong cách viết hoặc nghệ thuật thường không cần ép thành bài test định lượng. Đề xuất mặc định phù hợp với loại skill, nhưng để người dùng quyết định.

### Phỏng vấn và nghiên cứu

Chủ động làm rõ edge case, input/output format, file ví dụ, tiêu chí thành công và dependency.

Chưa viết test prompt cho đến khi phần này đủ rõ.

Kiểm tra các MCP/tool đang có. Nếu chúng hữu ích để tìm tài liệu, skill tương tự hoặc best practice, hãy nghiên cứu song song bằng subagent khi môi trường hỗ trợ; nếu không thì làm trực tiếp. Mục tiêu là chuẩn bị đủ ngữ cảnh để giảm số câu hỏi người dùng phải trả lời.

### Viết `SKILL.md`

Từ phần phỏng vấn, tạo các thành phần:

- **name**: định danh skill;
- **description**: skill làm gì và khi nào trigger. Đây là cơ chế trigger chính, vì vậy toàn bộ thông tin “khi nào dùng” phải nằm trong description chứ không chỉ trong body. Model có xu hướng under-trigger skill, nên description cần đủ chủ động: bao gồm cả chức năng và các ngữ cảnh/cụm từ liên quan, kể cả khi người dùng không gọi đúng tên skill;
- **compatibility**: tool hoặc dependency bắt buộc nếu có; đây là trường tùy chọn và hiếm khi cần;
- phần hướng dẫn còn lại của skill.

### Hướng dẫn viết skill

#### Cấu trúc một skill

```text
skill-name/
├── SKILL.md (bắt buộc)
│   ├── YAML frontmatter (bắt buộc name, description)
│   └── Markdown instructions
└── Bundled Resources (tùy chọn)
    ├── scripts/    - code thực thi cho tác vụ lặp lại hoặc cần tính quyết định
    ├── references/ - tài liệu được nạp khi cần
    └── assets/     - file dùng trong output như template, icon, font
```

#### Progressive Disclosure

Skill dùng ba tầng nạp nội dung:

1. **Metadata** (`name` + `description`) — luôn có trong context, khoảng 100 từ.
2. **Body của `SKILL.md`** — được nạp khi skill trigger; lý tưởng dưới 500 dòng.
3. **Bundled resources** — chỉ đọc khi cần; script có thể chạy mà không phải đưa toàn bộ nội dung vào context.

Các con số chỉ là gần đúng. Có thể dài hơn khi cần.

Mẫu nên dùng:

- nếu `SKILL.md` gần 500 dòng, tách thêm tầng tài liệu và chỉ dẫn rõ khi nào cần đọc file nào;
- tham chiếu resource rõ ràng từ `SKILL.md`;
- reference lớn hơn khoảng 300 dòng nên có mục lục;
- nếu skill hỗ trợ nhiều domain/framework, tổ chức theo variant để agent chỉ đọc phần cần thiết.

Ví dụ:

```text
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

#### Nguyên tắc không gây bất ngờ

Skill không được chứa malware, exploit code hoặc nội dung có thể làm tổn hại bảo mật. Nội dung skill không được đi ngược với mục đích mà người dùng được thông báo. Không tạo skill gây hiểu nhầm hoặc phục vụ truy cập trái phép, exfiltration dữ liệu hay hành vi độc hại. Roleplay vô hại vẫn có thể chấp nhận.

#### Mẫu viết hướng dẫn

Ưu tiên câu mệnh lệnh rõ ràng.

Khi output format phải cố định, có thể định nghĩa trực tiếp:

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

Khi ví dụ giúp làm rõ hành vi, dùng input/output cụ thể:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Phong cách viết

Cố gắng giải thích **vì sao** một quy tắc quan trọng thay vì chỉ chất nhiều `MUST`. Model hiện đại có thể suy luận tốt khi hiểu mục tiêu phía sau. Viết hướng dẫn đủ tổng quát để dùng cho nhiều tình huống, không tối ưu quá mức cho một ví dụ cụ thể.

Viết bản nháp, sau đó đọc lại như một người mới và cải thiện trước khi coi là xong.

### Test case

Sau bản nháp, tạo 2–3 test prompt thực tế — loại câu người dùng thật sự có thể viết. Cho người dùng xem và để họ sửa hoặc bổ sung nếu muốn, rồi mới chạy.

Lưu test case tại `evals/evals.json`. Ở bước đầu **chưa cần viết assertion**; chỉ lưu prompt. Assertion sẽ được thêm khi các lần chạy đang thực hiện.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Xem `references/schemas.md` để biết schema đầy đủ.

## Chạy và đánh giá test case

Phần này là một chuỗi liên tục; đừng dừng giữa chừng. **Không dùng `/skill-test` hoặc một testing skill khác để thay thế quy trình này.**

Đặt kết quả ở `<skill-name>-workspace/`, cùng cấp với thư mục skill. Bên trong workspace, chia theo iteration rồi theo test case:

```text
<skill-name>-workspace/
└── iteration-N/
    ├── eval-0/
    ├── eval-1/
    └── ...
```

Không cần tạo toàn bộ cây thư mục từ đầu; tạo dần khi chạy.

### Bước 1: Khởi chạy bản có skill và baseline trong cùng lượt

Với mỗi test case, khởi chạy hai subagent trong **cùng một lượt**: một bản có skill và một baseline. Không chạy hết bản có skill trước rồi mới quay lại baseline; chạy cùng lúc giúp các kết quả hoàn thành gần nhau và dễ so sánh hơn.

**Bản có skill:**

```text
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline:**

- Khi **tạo skill mới**: baseline không dùng skill. Giữ nguyên prompt và lưu tại `without_skill/outputs/`.
- Khi **cải thiện skill hiện có**: baseline là phiên bản cũ. Trước khi sửa, snapshot skill, ví dụ:

```bash
cp -r <skill-path> <workspace>/skill-snapshot/
```

Sau đó cho baseline dùng snapshot và lưu output tại `old_skill/outputs/`.

Tạo `eval_metadata.json` cho mỗi test case. Dùng `eval_name` có ý nghĩa mô tả điều đang kiểm thử, không chỉ `eval-0`. Nếu iteration dùng prompt mới hoặc đã chỉnh, tạo metadata tương ứng thay vì giả định file cũ vẫn đúng.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Bước 2: Trong khi các lần chạy đang thực hiện, soạn assertion

Đừng chỉ chờ. Dùng thời gian này để viết assertion định lượng cho từng test case và giải thích chúng cho người dùng. Nếu `evals/evals.json` đã có assertion, rà lại và giải thích chúng kiểm tra điều gì.

Assertion tốt phải kiểm chứng được khách quan và có tên/mô tả đủ rõ để người đọc benchmark hiểu ngay. Với chất lượng mang tính chủ quan như phong cách viết hoặc thiết kế, ưu tiên đánh giá định tính; không ép mọi thứ thành assertion giả-khách-quan.

Sau khi soạn xong, cập nhật `eval_metadata.json` và `evals/evals.json`. Đồng thời nói rõ cho người dùng rằng viewer có cả output định tính và benchmark định lượng.

### Bước 3: Ghi timing ngay khi từng run hoàn tất

Khi subagent hoàn tất, notification cung cấp `total_tokens` và `duration_ms`. Lưu ngay dữ liệu này vào `timing.json` của run:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Đây là thời điểm duy nhất dữ liệu notification này có sẵn; không trì hoãn rồi cố truy hồi sau.

### Bước 4: Chấm, tổng hợp và mở viewer

Khi toàn bộ run đã xong:

1. **Chấm từng run.** Dùng grader theo `agents/grader.md` hoặc chấm inline. Lưu `grading.json` trong từng run. Mảng `expectations` trong `grading.json` phải dùng chính xác các field `text`, `passed`, `evidence`; không thay bằng `name`, `met`, `details` hay tên khác. Với assertion kiểm tra được bằng chương trình, viết/chạy script thay vì nhìn thủ công khi điều đó đáng tin cậy hơn.

2. **Tổng hợp benchmark.** Chạy:

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

Script tạo `benchmark.json` và `benchmark.md` với pass rate, thời gian và token cho từng configuration, gồm mean ± stddev và delta. Nếu phải tạo `benchmark.json` thủ công, xem schema chính xác trong `references/schemas.md`. Đặt từng phiên bản `with_skill` trước baseline tương ứng.

3. **Phân tích benchmark.** Đọc dữ liệu benchmark và tìm pattern mà số tổng hợp có thể che khuất. Xem phần `Analyzing Benchmark Results` trong `agents/analyzer.md`: assertion luôn pass ở cả hai configuration, eval có variance cao, time/token tradeoff, v.v.

4. **Mở viewer:**

```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

Từ iteration 2 trở đi, thêm:

```text
--previous-workspace <workspace>/iteration-<N-1>
```

Trong môi trường headless hoặc không có `webbrowser.open()`, dùng:

```text
--static <output_path>
```

để tạo một file HTML độc lập thay vì mở server. Khi người dùng bấm `Submit All Reviews`, feedback được tải về dưới dạng `feedback.json`; đưa file đó vào workspace để iteration sau đọc lại.

5. Nói cho người dùng biết viewer có hai tab chính: `Outputs` để xem từng test case và để lại feedback; `Benchmark` để xem so sánh định lượng.

### Người dùng thấy gì trong viewer

Tab `Outputs` hiển thị từng test case:

- **Prompt**: tác vụ đã giao;
- **Output**: file kết quả, render inline nếu có thể;
- **Previous Output**: từ iteration 2+, thu gọn mặc định;
- **Formal Grades**: assertion pass/fail nếu đã chấm;
- **Feedback**: ô nhập tự lưu khi người dùng gõ;
- **Previous Feedback**: phản hồi iteration trước.

Tab `Benchmark` hiển thị thống kê tổng hợp theo configuration và từng eval.

Di chuyển bằng nút trước/sau hoặc phím mũi tên. Khi xong, người dùng bấm `Submit All Reviews` để lưu `feedback.json`.

### Bước 5: Đọc feedback

Khi người dùng báo đã review xong, đọc `feedback.json`:

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "the chart is missing axis labels",
      "timestamp": "..."
    }
  ]
}
```

Dùng feedback cho iteration tiếp theo. Feedback trống nghĩa là người dùng không để lại nhận xét cho run đó, không tự diễn giải thành pass hoặc fail.

Nếu viewer được chạy dạng server, dừng process khi không còn cần thiết:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Cải thiện skill

Đây là phần trung tâm của vòng lặp: đã chạy test case, người dùng đã review, bây giờ cải thiện skill theo feedback.

### Cách suy nghĩ về cải thiện

1. **Khái quát hóa từ feedback.** Mục tiêu là skill dùng được cho rất nhiều prompt, không chỉ vài ví dụ đang test. Đừng thêm các chỉnh sửa vụn vặt khiến skill overfit hoặc chồng quá nhiều `MUST`. Nếu một lỗi cứ lặp lại, thử diễn đạt nguyên tắc theo cách tổng quát hơn hoặc đưa ra pattern làm việc tốt hơn.

2. **Giữ prompt gọn.** Bỏ phần không tạo giá trị. Đọc transcript chứ không chỉ final output; nếu skill khiến model tốn thời gian vào bước vô ích, xem lại instruction gây ra hành vi đó.

3. **Giải thích lý do.** Model có khả năng suy luận khi hiểu tại sao một yêu cầu quan trọng. Nếu thấy mình dùng `ALWAYS` hoặc `NEVER` dày đặc, đó là tín hiệu nên xem có thể thay bằng lý do và mục tiêu rõ ràng hơn không. Quy tắc cứng vẫn cần khi hợp đồng đầu ra hoặc an toàn đòi hỏi.

4. **Tìm phần việc lặp lại giữa các test case.** Nếu nhiều subagent độc lập đều phải viết cùng loại helper script như `create_docx.py` hoặc `build_chart.py`, đó là tín hiệu nên đóng gói script đó vào `scripts/` một lần và hướng dẫn skill tái sử dụng.

Sau mỗi bản sửa, đọc lại với góc nhìn mới rồi chạy lại eval phù hợp. Khi các ví dụ quen thuộc đã ổn, mở rộng test set để kiểm tra khả năng tổng quát hóa.

## Tối ưu description và trigger

Khi nội dung skill đã ổn, có thể dùng công cụ cải thiện description đi kèm skill-creator để tối ưu độ chính xác trigger. Không dùng tối ưu description để che một body skill chưa rõ hoặc workflow đang sai.

Giữ nguyên nguyên tắc của frontmatter: `description` phải mô tả cả **skill làm gì** và **khi nào nên dùng**.

## Nguồn Việt hóa

- Skill gốc: `.agents/skills/skill-creator`
- Tên gốc: `skill-creator`
- Chính sách: `faithful`
- Commit nguồn: `3030df714cc44a870c315474ef502acd25e173f6`
