# Traceability

## Nguyên tắc

Diagram phải truy vết được về source artifact và các ID ổn định khi có.

Ưu tiên giữ:

- `US*`
- `FR-*`
- `SC-*`
- task ID như `T001`
- phase ID/tên
- domain/entity/component name
- contract/interface identifier

## Theo phase

### Spec

`Requirement/User Story → actor/use case/capability → flow/domain/state → spec diagram`

### Plan

`Requirement/Spec concept → technical decision/component/data/contract → plan diagram`

### Tasks

`Plan decision/User Story → task group/dependency → tasks diagram`

### Implementation

`Task/Plan decision → implemented module/component/runtime flow → implementation diagram`

### Converge

`Requirement/Plan/Task → current state → gap → convergence task → converge diagram`

## Fidelity

Nếu diagram phải collapse/drop chi tiết do complexity:

- không bỏ requirement/actor/entity/state làm thay đổi nghĩa;
- ghi rõ phần đã collapse trong caption/footer hoặc báo cáo;
- chi tiết đầy đủ vẫn nằm trong artifact nguồn.

## Drift check

Trước khi kết thúc, kiểm tra:

- ID trên diagram còn tồn tại trong source không;
- relation/flow/state trên diagram còn đúng không;
- source có thay đổi đáng kể chưa phản ánh lên diagram không;
- diagram có chứa semantics không có nguồn không.
