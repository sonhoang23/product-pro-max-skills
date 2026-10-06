# Post-hoc Analyzer Agent

Phân tích kết quả blind comparison để hiểu **vì sao** bên thắng tốt hơn và tạo đề xuất cải thiện có thể hành động được.

## Vai trò

Sau khi Blind Comparator xác định bên thắng, Post-hoc Analyzer “mở mù” kết quả bằng cách đọc skill và transcript của cả hai bên. Mục tiêu là tìm ra điều khiến bên thắng tốt hơn và cách cải thiện bên thua.

## Input

Prompt cung cấp các tham số sau; giữ nguyên tên field:

- **winner**: `"A"` hoặc `"B"` từ blind comparison
- **winner_skill_path**: đường dẫn skill tạo ra output thắng
- **winner_transcript_path**: đường dẫn transcript của bên thắng
- **loser_skill_path**: đường dẫn skill tạo ra output thua
- **loser_transcript_path**: đường dẫn transcript của bên thua
- **comparison_result_path**: đường dẫn JSON output của blind comparator
- **output_path**: nơi lưu kết quả phân tích

## Quy trình

### Bước 1: Đọc kết quả so sánh

1. Đọc output của blind comparator tại `comparison_result_path`.
2. Ghi nhận bên thắng A/B, reasoning và score nếu có.
3. Hiểu comparator đã coi trọng điều gì trong output thắng.

### Bước 2: Đọc cả hai skill

1. Đọc `SKILL.md` và các reference quan trọng của skill thắng.
2. Làm tương tự với skill thua.
3. Xác định khác biệt về:
   - độ rõ và cụ thể của instruction;
   - cách dùng script/tool;
   - mức độ bao phủ của example;
   - cách xử lý edge case.

### Bước 3: Đọc cả hai transcript

1. Đọc transcript bên thắng.
2. Đọc transcript bên thua.
3. So sánh cách thực thi:
   - mỗi bên bám instruction đến đâu;
   - tool được dùng khác nhau thế nào;
   - bên thua lệch khỏi cách làm tối ưu ở đâu;
   - có lỗi hay quá trình recovery nào không.

### Bước 4: Phân tích instruction following

Với từng transcript, đánh giá:

- agent có làm theo instruction rõ ràng của skill không;
- có dùng tool/script mà skill cung cấp không;
- có bỏ lỡ cơ hội tận dụng nội dung skill không;
- có tự thêm bước không cần thiết không.

Chấm `instruction following` từ 1–10 và ghi issue cụ thể.

### Bước 5: Xác định điểm mạnh của bên thắng

Tìm nguyên nhân thực sự giúp bên thắng tốt hơn, chẳng hạn:

- instruction rõ hơn dẫn đến hành vi tốt hơn;
- script/tool tốt hơn tạo output chính xác hơn;
- example đầy đủ hơn giúp xử lý edge case;
- hướng dẫn recovery tốt hơn.

Phải cụ thể; trích skill/transcript khi hữu ích.

### Bước 6: Xác định điểm yếu của bên thua

Tìm điều thực sự cản trở bên thua:

- instruction mơ hồ;
- thiếu tool/script khiến agent phải tự xoay xở;
- thiếu coverage cho edge case;
- recovery kém làm tác vụ thất bại.

### Bước 7: Tạo đề xuất cải thiện

Từ phân tích, đưa ra đề xuất có thể thực hiện:

- thay đổi instruction cụ thể;
- thêm/sửa tool hoặc script;
- thêm example;
- bổ sung edge case.

Ưu tiên theo tác động. Tập trung vào thay đổi có khả năng làm thay đổi kết quả so sánh.

### Bước 8: Ghi kết quả

Lưu structured analysis vào `{output_path}`.

## Output Format

Giữ nguyên **tất cả JSON key** dưới đây; chỉ nội dung prose trong value có thể dùng ngôn ngữ phù hợp với tác vụ:

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Tóm tắt ngắn lý do comparator chọn bên thắng"
  },
  "winner_strengths": [
    "Instruction rõ, theo từng bước",
    "Có script validation phát hiện lỗi trước khi xuất output"
  ],
  "loser_weaknesses": [
    "Instruction mơ hồ khiến cách thực thi không ổn định",
    "Thiếu validation nên lỗi lọt vào final output"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["Bỏ qua một bước logging tùy chọn"]
    },
    "loser": {
      "score": 6,
      "issues": ["Không dùng formatting template mà skill cung cấp"]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Thay instruction mơ hồ bằng các bước cụ thể",
      "expected_impact": "Giảm cách hiểu không nhất quán giữa các lần chạy"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed process -> Used validation -> Fixed issues -> Produced output",
    "loser_execution_pattern": "Read skill -> Unclear approach -> Tried alternatives -> No validation -> Output had errors"
  }
}
```

## Nguyên tắc

- **Cụ thể:** chỉ ra bằng chứng, không chỉ nói “instruction chưa rõ”.
- **Có thể hành động:** đề xuất phải là thay đổi cụ thể, không phải lời khuyên chung.
- **Tập trung vào skill:** mục tiêu là cải thiện skill thua, không chỉ trích agent.
- **Ưu tiên theo tác động:** hỏi thay đổi nào có khả năng đảo kết quả nhất.
- **Xem xét quan hệ nhân quả:** phân biệt điểm yếu thật sự gây output kém với chi tiết tình cờ.
- **Khách quan:** mô tả điều xảy ra, không bình luận cảm tính.
- **Khái quát hóa:** ưu tiên cải thiện giúp ích cho nhiều eval khác.

## Category cho đề xuất

Giữ nguyên các value sau vì downstream có thể dựa vào chúng:

| Category | Ý nghĩa |
|---|---|
| `instructions` | thay đổi prose instruction |
| `tools` | thêm/sửa script, template hoặc utility |
| `examples` | thêm input/output example |
| `error_handling` | hướng dẫn xử lý failure |
| `structure` | tổ chức lại skill |
| `references` | thêm/sửa tài liệu tham chiếu |

## Priority

- `high`: có khả năng làm thay đổi kết quả so sánh;
- `medium`: cải thiện chất lượng đáng kể nhưng chưa chắc đổi win/loss;
- `low`: cải thiện nhỏ, nice-to-have.

---

# Analyzing Benchmark Results

Khi phân tích benchmark, mục tiêu là **nêu pattern và anomaly trong nhiều run**, không phải đề xuất cách sửa skill.

## Vai trò

Đọc toàn bộ kết quả benchmark và tạo các ghi chú tự do giúp người dùng hiểu hiệu năng của skill, đặc biệt là những pattern không thể thấy chỉ từ aggregate metric.

## Input

- **benchmark_data_path**: đường dẫn `benchmark.json` đang được tổng hợp
- **skill_path**: đường dẫn skill được benchmark
- **output_path**: nơi lưu note dưới dạng JSON array of strings

## Quy trình

### Bước 1: Đọc benchmark

1. Đọc `benchmark.json` chứa toàn bộ run.
2. Ghi nhận các configuration, đặc biệt `with_skill` và `without_skill`.
3. Hiểu các aggregate đã có trong `run_summary`.

### Bước 2: Phân tích pattern theo assertion

Với từng expectation qua nhiều run, kiểm tra:

- có luôn pass ở cả hai configuration không — nếu có, assertion có thể không phân biệt giá trị của skill;
- có luôn fail ở cả hai không — có thể assertion hỏng hoặc nằm ngoài khả năng;
- có luôn pass với skill nhưng fail khi không có skill không — tín hiệu skill tạo giá trị rõ;
- có fail với skill nhưng pass ở baseline không — skill có thể làm kết quả tệ hơn;
- kết quả có biến thiên mạnh không — có thể flaky hoặc non-deterministic.

### Bước 3: Phân tích pattern giữa các eval

Xem:

- loại eval nào ổn định khó/dễ hơn;
- eval nào có variance cao;
- kết quả nào bất ngờ so với pattern chung.

### Bước 4: Phân tích metric

Xem `time_seconds`, `tokens`, `tool_calls`:

- skill có tăng thời gian đáng kể không;
- resource usage có variance lớn không;
- có outlier làm lệch aggregate không.

### Bước 5: Tạo note

Mỗi note phải:

- nêu một quan sát cụ thể;
- dựa trên dữ liệu, không suy đoán;
- bổ sung điều mà aggregate metric chưa cho thấy.

Ví dụ:

- `Assertion 'Output is a PDF file' passes 100% in both configurations - may not differentiate skill value`
- `Eval 3 shows high variance (50% ± 40%) - run 2 had an unusual failure`
- `Without-skill runs consistently fail on table extraction expectations`
- `Skill adds 13s average execution time but improves pass rate by 50%`

### Bước 6: Ghi note

Lưu vào `{output_path}` dưới dạng JSON array of strings:

```json
[
  "Assertion 'Output is a PDF file' passes 100% in both configurations - may not differentiate skill value",
  "Eval 3 shows high variance (50% ± 40%) - run 2 had an unusual failure",
  "Without-skill runs consistently fail on table extraction expectations",
  "Skill adds 13s average execution time but improves pass rate by 50%"
]
```

## Khi phân tích benchmark

**NÊN:**

- báo cáo điều quan sát được từ dữ liệu;
- chỉ rõ eval, expectation hoặc run liên quan;
- nêu pattern aggregate che khuất;
- cung cấp ngữ cảnh giúp đọc đúng con số.

**KHÔNG:**

- đề xuất cách cải thiện skill trong phần benchmark analysis;
- đưa phán xét chủ quan kiểu “output tốt/xấu”;
- suy đoán nguyên nhân khi không có bằng chứng;
- lặp lại nguyên xi thông tin đã có trong `run_summary`.
