# JSON Schemas

Tài liệu này định nghĩa các JSON schema mà `skill-creator` sử dụng. **Tên key, cấu trúc nesting, enum và configuration value là contract kỹ thuật; không được Việt hóa hoặc đổi tên.** Phần mô tả dành cho người đọc được Việt hóa bên dưới.

---

## `evals.json`

Định nghĩa eval cho một skill. File nằm tại `evals/evals.json` trong thư mục skill.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

**Field:**

- `skill_name`: phải khớp `name` trong frontmatter của skill.
- `evals[].id`: integer duy nhất cho từng eval.
- `evals[].prompt`: task/prompt cần thực thi.
- `evals[].expected_output`: mô tả dễ đọc về kết quả thành công.
- `evals[].files`: danh sách input file tùy chọn, path tương đối từ skill root.
- `evals[].expectations`: các phát biểu có thể kiểm chứng.

---

## `history.json`

Theo dõi tiến trình các version trong Improve mode. File nằm ở workspace root.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**Field:**

- `started_at`: ISO timestamp khi bắt đầu improvement.
- `skill_name`: tên skill.
- `current_best`: version hiện được coi là tốt nhất.
- `iterations[].version`: định danh version như `v0`, `v1`.
- `iterations[].parent`: version cha.
- `iterations[].expectation_pass_rate`: tỷ lệ expectation pass.
- `iterations[].grading_result`: chỉ dùng `"baseline"`, `"won"`, `"lost"` hoặc `"tie"`.
- `iterations[].is_current_best`: boolean cho biết đây có phải version tốt nhất hiện tại không.

---

## `grading.json`

Output của grader agent. File nằm tại `<run-dir>/grading.json`.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith, Sarah Johnson'"
    },
    {
      "text": "The spreadsheet has a SUM formula in cell B10",
      "passed": false,
      "evidence": "No spreadsheet was created. The output was a text file."
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.5
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "The form has 12 fillable fields",
      "type": "factual",
      "verified": true,
      "evidence": "Counted 12 fields in field_info.json"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["Used 2023 data, may be stale"],
    "needs_review": [],
    "workarounds": []
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "The output includes the name 'John Smith'",
        "reason": "A hallucinated document that mentions the name would also pass"
      }
    ],
    "overall": "Assertions check presence but not correctness."
  }
}
```

**Field:**

- `expectations[]`: kết quả từng expectation, **bắt buộc** dùng `text`, `passed`, `evidence`.
- `summary`: số lượng pass/fail và `pass_rate`.
- `execution_metrics`: dữ liệu tool/output lấy từ `metrics.json` nếu có.
- `timing`: timing của executor/grader nếu có.
- `claims`: claim được trích xuất và xác minh.
- `user_notes_summary`: issue executor tự ghi nhận.
- `eval_feedback`: đề xuất cải thiện eval, chỉ cần khi grader thấy gap đáng kể.

---

## `metrics.json`

Output metric của executor agent. File nằm tại `<run-dir>/outputs/metrics.json`.

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**Field:**

- `tool_calls`: số lần gọi theo từng tool type.
- `total_tool_calls`: tổng số tool call.
- `total_steps`: số major step.
- `files_created`: file được tạo.
- `errors_encountered`: số lỗi gặp phải.
- `output_chars`: tổng số ký tự output, dùng như proxy gần đúng cho lượng output.
- `transcript_chars`: số ký tự transcript.

---

## `timing.json`

Timing cho một run. File nằm tại `<run-dir>/timing.json`.

Thông tin `total_tokens` và `duration_ms` từ notification khi subagent hoàn tất phải được lưu ngay vì không có nguồn khác bảo đảm truy hồi lại về sau.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

## `benchmark.json`

Output của Benchmark mode, thường nằm tại `benchmarks/<timestamp>/benchmark.json`.

```json
{
  "metadata": {
    "skill_name": "pdf",
    "skill_path": "/path/to/pdf",
    "executor_model": "claude-sonnet-4-20250514",
    "analyzer_model": "most-capable-model",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "Ocean",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.8, "max": 0.9},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },
  "notes": []
}
```

**Contract quan trọng:**

- `metadata.skill_name`: tên skill.
- `metadata.timestamp`: thời điểm benchmark.
- `metadata.evals_run`: eval ID/name được chạy.
- `metadata.runs_per_configuration`: số run mỗi configuration.
- `runs[].eval_id`: ID eval.
- `runs[].eval_name`: tên dễ đọc dùng làm heading trong viewer.
- `runs[].configuration`: **phải** là `"with_skill"` hoặc `"without_skill"`; viewer dựa chính xác vào string này để group và render.
- `runs[].run_number`: số thứ tự run.
- `runs[].result`: chứa `pass_rate`, `passed`, `failed`, `total`, `time_seconds`, `tokens`, `tool_calls`, `errors`.
- `run_summary`: aggregate theo configuration.
- `delta`: chênh lệch dạng string.
- `notes`: quan sát tự do từ analyzer.

Viewer đọc các field name này chính xác. Dùng `config` thay cho `configuration`, hoặc đặt `pass_rate` ở top level của run thay vì trong `result`, có thể khiến viewer hiển thị dữ liệu rỗng/0. Khi tạo `benchmark.json` thủ công, luôn bám schema này.

---

## `comparison.json`

Output của Blind Comparator. File thường nằm tại `<grading-dir>/comparison-N.json`.

```json
{
  "winner": "A",
  "reasoning": "Output A provides a complete solution with proper formatting and all required fields.",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {
        "correctness": 3,
        "completeness": 2,
        "accuracy": 3
      },
      "structure": {
        "organization": 3,
        "formatting": 2,
        "usability": 3
      },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["Complete solution"],
      "weaknesses": []
    },
    "B": {
      "score": 5,
      "strengths": ["Readable output"],
      "weaknesses": ["Missing date field"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.8,
      "details": [
        {"text": "Output includes name", "passed": true}
      ]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.6,
      "details": [
        {"text": "Output includes name", "passed": true}
      ]
    }
  }
}
```

Nếu input không có expectation, `expectation_results` có thể bị lược bỏ theo contract của comparator.

---

## `analysis.json`

Output của post-hoc analyzer. File nằm tại `<grading-dir>/analysis.json`.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary of why comparator chose winner"
  },
  "winner_strengths": [
    "Clear step-by-step instructions for handling multi-page documents",
    "Included validation script that caught formatting errors"
  ],
  "loser_weaknesses": [
    "Vague instruction led to inconsistent behavior",
    "No validation script"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": []
    },
    "loser": {
      "score": 6,
      "issues": ["Did not use the skill's formatting template"]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace vague instruction with explicit steps",
      "expected_impact": "Reduce ambiguity"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed process -> Used validation",
    "loser_execution_pattern": "Read skill -> Unclear approach -> No validation"
  }
}
```

Giữ nguyên các key vì analyzer và viewer downstream phụ thuộc vào schema này.
