# Diagram governance

## Diagram Check

Tạo diagram khi có relation/flow/state/dependency/boundary/structure mà người đọc khó ghép nhanh từ text.

Không vẽ chỉ để đủ bộ.

## Placement

Mặc định theo source artifact:

```text
FEATURE_DIR/
  spec.md
  spec-diagram/

  plan.md
  data-model.md
  contracts/
  plan-diagram/

  tasks.md
  tasks-diagram/

  implementation-diagram/
  converge-diagram/
```

Research/product-direction ngoài feature dùng folder `research-diagram/` hoặc `<artifact>-diagram/` cạnh tài liệu nguồn.

## Naming

Tên file theo model, ví dụ:

- `system-context.html`
- `core-flow.html`
- `domain-model.html`
- `lifecycle.html`
- `architecture.html`
- `data-flow.html`
- `deployment.html`
- `dependency.html`
- `phase-01-runtime-flow.html`
- `gap-map.html`

## Source of truth

Diagram chỉ là derived view.

Nếu diagram và source text mâu thuẫn:

1. không tự chọn diagram;
2. xác định source có thẩm quyền;
3. nếu source đúng, re-render diagram;
4. nếu source cần đổi, cập nhật source có chủ đích trước.

## Link hai chiều

Artifact nguồn có diagram nên có link ngắn tới diagram.

Diagram phải có reference/link về artifact nguồn bằng relative path.

## Duplicate control

Trước khi tạo diagram mới:

1. kiểm tra model tương đương đã tồn tại chưa;
2. nếu có, cập nhật diagram đó;
3. chỉ tạo diagram mới khi viewpoint khác có giá trị rõ.

## Sync

Không regenerate vì sửa chính tả/câu chữ.

Cập nhật khi thay đổi:

- node/thành phần quan trọng;
- flow/handoff;
- state;
- dependency;
- boundary;
- architecture;
- domain/data relation;
- current-state implementation;
- gap/convergence state.

## Render

Dùng `diagram-design-vi`.

HTML là canonical living artifact; SVG/PNG chỉ export khi cần.
