# Semantic patterns

Semantic pattern mô tả **một hệ thống làm gì**; 39 visual type mô tả **thông tin được sắp xếp như thế nào**. Khi behavior, state, enforcement hoặc risk là phần mang nghĩa chính, hãy chọn pattern trước, sau đó dùng visual type gần nhất làm layout grammar. Nếu không pattern nào khớp, chọn visual type trực tiếp.

Mỗi figure dùng một primary pattern. Pattern thứ hai chỉ được cung cấp tối đa một supporting primitive; nếu cả hai đều cần treatment đầy đủ, hãy split thành overview và detail. Label và outcome phải luôn đầy đủ trong static frame.

## Routing table

| Người đọc cần hiểu… | Semantic pattern | Visual type gần nhất |
|---|---|---|
| Nhiều arrival cạnh tranh finite service capacity | **Fan-in queue / bottleneck** | Data flow |
| Question / Input / Governance / Output lặp qua nhiều stage | **Stage framework with semantic slots** | Process |
| Conversation hoặc input lỏng lẻo trở thành durable structured record | **Unstructured input → structured artifact** | Data flow |
| Vì sao hai policy decision khác nhau và chúng lệch nhau lần đầu ở đâu | **Paired policy-evaluation traces** | Flowchart |
| Route nào vượt trust boundary và route nào bị block | **Secure paved road** | Architecture |
| Control nào áp dụng tại từng enforcement surface | **Governance / control catalog** | Layer stack |
| Defense giảm risk thế nào và risk nào còn lại | **Compensating security layers** | Layer stack |

## 1. Fan-in queue / bottleneck

**Trigger để chọn:** Nhiều producer hội tụ vào một reviewer, service, gate hoặc constrained resource; story phụ thuộc arrival rate, queue depth, wait, capacity hoặc backpressure.

**Primitive bắt buộc:** Các source tách biệt; ingress được fan; ordered queue có slot và count nhìn thấy; capacity/service-rate label; một constrained service point; admitted outcome và deferred/rejected outcome. Label phải có unit (`8/hour`, `3 slots`), không chỉ ghi “high”.

**Complexity budget:** ≤5 source, ≤5 queue slot, một bottleneck, hai outcome và ≤9 primary node. Aggregate source vượt mức thành một named cohort.

**Anti-pattern:** Equal-width pipeline làm biến mất contention; arrow bị merge trước khi còn trace được; capacity chỉ được ngụ ý bằng box size; pile-up trang trí; animation đổi thứ tự item; chỉ dùng red để biểu đạt overloaded.

**Static fallback:** Hiển thị representative final queue, numeric count/capacity, bottleneck label và cả hai outcome path. Một still frame phải cho thấy **vì sao** work phải chờ.

**Visual type gần nhất:** mặc định **Data flow**; dùng **Process** khi service stages, không phải sources, mới là trục chính.

## 2. Stage framework with semantic slots

**Trigger để chọn:** Lifecycle hoặc operating model lặp cùng các semantic question qua nhiều stage, thường là Question, Input, Governance và Output. Khả năng so sánh giữa các stage quan trọng hơn message timing.

**Primitive bắt buộc:** Ordered stage header; consistent slot grid; explicit empty/not-applicable slot; stage-to-stage handoff; stable slot label; một primary output cho mỗi stage. Giữ nguyên slot order ở mọi stage.

**Complexity budget:** 3–6 stage, 3–4 slot kind, ≤20 populated cell, ≤2 line mỗi cell. Split detail khi một cell cần prose dài.

**Anti-pattern:** Mỗi stage tự invent internal layout khác nhau; slot meaning chỉ được encode bằng position mà không label; fake precision từ hàng chục cell; nhầm stage order với ownership lane; thu nhỏ text để giữ mọi thứ trên một canvas.

**Static fallback:** Render full stage × slot matrix với handoff và entry `—` hoặc `Not applicable` rõ ràng. Không phụ thuộc staged reveal để dạy schema.

**Visual type gần nhất:** **Process**; chỉ dùng **Swimlane** khi các row lặp đại diện owner thay vì semantic slot.

## 3. Unstructured input → structured artifact

**Trigger để chọn:** Dialogue, note, prompt hoặc một request dài dòng được elicited, normalized và ghi thành durable brief, ticket, record, schema hoặc structured artifact khác.

**Primitive bắt buộc:** Source utterance; clarifying question; extracted field/value pair; named transformation; durable artifact boundary; provenance link từ representative statement tới field; missing/unknown state.

**Complexity budget:** ≤4 exchange, ≤6 artifact field, một transformation và ≤3 provenance link. Hiển thị representative content, không phải transcript đầy đủ.

**Anti-pattern:** “AI magic” sparkle giữa hai box; artifact được vẽ như một chat bubble khác; field xuất hiện mà không có source; invent certainty cho missing fact; typing animation là cách duy nhất để đọc copy.

**Static fallback:** Hiển thị short source excerpt cạnh completed labeled artifact, có ít nhất một provenance mapping và mọi unknown field nhìn thấy được.

**Visual type gần nhất:** **Data flow**; dùng **Process** khi elicitation có nhiều ordered gate.

## 4. Paired policy-evaluation traces

**Trigger để chọn:** Hai request gần như giống nhau đi tới outcome khác nhau; người đọc cần thấy state `PASS`, `FAIL`, `SKIPPED` hoặc `NOT REACHED` theo từng rule và first divergence.

**Primitive bắt buộc:** Cùng ordered rule trên cả hai trace; explicit status text cộng symbol/shape; input khác nhau; final outcome; labeled first-divergence marker; phân biệt `SKIPPED` — applicable flow chủ động bỏ qua — với `NOT REACHED` — evaluation đã dừng trước đó.

**Complexity budget:** Chính xác 2 trace, 3–6 rule, một first divergence, ≤12 status cell và một outcome mỗi trace. Đưa rule prose sang note nếu label vượt một dòng.

**Anti-pattern:** So sánh hai independently ordered flow; green/red dot không kèm chữ; coi skipped và not-reached là synonym; highlight mọi difference; tiếp tục denied trace như thể downstream rule vẫn chạy.

**Static fallback:** Hiển thị mọi rule state và cả hai outcome cùng lúc; dùng persistent bracket/line + label cho first divergence.

**Visual type gần nhất:** **Flowchart** cho ordered decision logic; chỉ dùng **Sequence** khi message giữa actor và time cũng là load-bearing.

## 5. Secure paved road

**Trigger để chọn:** Supported architecture tạo bounded route từ intake/build đến deployment; trust boundary, privileged moment, permitted ingress, forbidden ingress, approved deploy path và blocked deploy path là nội dung chính.

**Primitive bắt buộc:** Labeled trust boundary; actor và identity; permitted ingress có positive text label; forbidden ingress dừng tại boundary; approved deployment path; blocked bypass path; privileged gate; isolated runtime; audit destination. Dùng line style và stop symbol khác nhau **ngoài** color.

**Complexity budget:** ≤3 trust zone, ≤8 component, ≤10 path, ≤2 forbidden path và một privileged gate. Split control detail sang catalog figure.

**Anti-pattern:** Dashed box chỉ ghi “security” mà không route semantics; forbidden arrow vẫn đi xuyên protected zone; secret/identity chỉ được ngụ ý không label; mọi component đều styled như trusted; bypass path nhìn như nhập lại approved route.

**Static fallback:** Render mọi boundary và cả permitted/forbidden route. Blocked path phải nhìn thấy rõ là dừng **trước** entry/deployment.

**Visual type gần nhất:** **Architecture**.

## 6. Governance / control catalog

**Trigger để chọn:** Control inventory phải được hiểu theo nơi enforcement: authoring, workspace, merge/CI, deploy/runtime hoặc surface được đặt tên khác. Một checklist duy nhất sẽ che các enforcement point này.

**Primitive bắt buộc:** Enforcement-surface group; named control; enforcement actor (`code`, `platform`, `human`); timing (`write`, `merge`, `deploy`, `run`); bypassability hoặc exception route; coverage/gap notation.

**Complexity budget:** 3–5 surface, 3–7 control mỗi surface, ≤24 control tổng, ≤3 attribute mỗi control. Chỉ summarize count khi item list tồn tại ở nơi khác.

**Anti-pattern:** 35 tiny pill; group theo vague theme thay vì enforcement point; trộn aspiration với enforced control; icon không có control name; claim defense-in-depth mà không show surface coverage.

**Static fallback:** Hiển thị full grouped catalog với surface header và text label cho actor + enforcement timing; giữ gap và exception.

**Visual type gần nhất:** **Layer stack**; dùng **DP security matrix** khi role permission, không phải enforcement surface, là comparison chính.

## 7. Compensating security layers

**Trigger để chọn:** Không layer nào hoàn hảo; mỗi defense cover một failure bị layer trước bỏ lại, và residual risk phải nhìn thấy là đang hẹp lại, chuyển tiếp hoặc còn tồn tại qua stack.

**Primitive bắt buộc:** Ordered threat/risk input; named defensive layer; mitigation của mỗi layer; explicit limitation hoặc escape; residual-risk carrier giữa layer; final residual risk và consequence/response. Dùng label hoặc decreasing measure, không chỉ area.

**Complexity budget:** 3–5 layer, một primary risk thread, ≤2 mitigation mỗi layer, và một final residual-risk statement. Split threat không liên quan thành figure riêng.

**Anti-pattern:** Ngụ ý layer cuối làm risk về zero; equal opaque slab không propagation; coi audit như prevention; shrink shape không có numeric/verbal meaning; đảo prevention/detection/recovery order mà không giải thích.

**Static fallback:** Hiển thị complete propagation chain: initial risk → mitigation → escaped risk ở mọi layer → final residual risk và response.

**Visual type gần nhất:** **Layer stack**; dùng **Nested** khi containment boundary, không phải ordered compensation, mang meaning.

## Composition rules

- Semantic pattern có thể specialize status, boundary, queue hoặc propagation primitive; selected type vẫn sở hữu page axis, connector grammar, spacing và type-specific limit.
- Áp dụng budget **chặt hơn** giữa pattern budget và visual-type budget. Semantic cell/status không cho phép vượt nine-node overview target.
- Dùng stable text cho state và outcome. Color, motion và position chỉ reinforcement, không bao giờ là encoding duy nhất.
- Optional animation là presentation layer, không phải một pattern khác. Chỉ load [`animation.md`](animation.md) khi motion được yêu cầu hoặc thực sự làm rõ ordered change.
