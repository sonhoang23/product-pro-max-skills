# UML Class Diagram

**Phù hợp nhất cho:** cấu trúc static của object model — class, chúng sở hữu gì, inherit gì và chỉ depend vào gì. Nội dung phân biệt type này là **operations compartment** và **typed relationship vocabulary** — arrowhead mang meaning. ER không thể biểu đạt hai thứ đó; chỉ dùng type này khi operation hoặc vocabulary inheritance/composition là trọng tâm, còn khi câu chuyện là entity + cardinality thì dùng `type-er.md`.

**Các UML diagram khác — route sang type khác.** UML là một family; chỉ class diagram có grammar riêng ở đây:

| UML diagram | Dùng thay thế |
|---|---|
| Sequence | [type-sequence.md](type-sequence.md) |
| State machine | [type-state.md](type-state.md) |
| Component | [type-architecture.md](type-architecture.md) |
| Deployment | [type-architecture.md](type-architecture.md) |
| Activity | [type-swimlane.md](type-swimlane.md) hoặc [type-flowchart.md](type-flowchart.md) |
| Conceptual / domain ER | [type-er.md](type-er.md) |

## Quy ước layout

- Mỗi class là một **single box** (`rx=6`), chia bằng hairline full-width thành tối đa ba compartment. Chiều cao compartment theo content — không pad đồng đều cho bằng chiều cao.
  1. **Name** — class name dùng Geist sans 12px, weight 600, **centered**. Interface có thêm stereotype line Geist Mono 8px `«interface»` phía trên name. Abstract class dùng name *italic*.
  2. **Attributes** — mỗi line Geist Mono 9px, left-aligned: `+ name: Type`. Visibility marker: `+` public, `-` private, `#` protected.
  3. **Operations** — mỗi line Geist Mono 9px, left-aligned: `+ method(arg): Return`.
  Bỏ hẳn compartment nếu class không có member loại đó — interface không attribute thì không tạo attribute compartment rỗng.
- Attribute/operation line là một combined string, không phải layout field/type hai cột như ER — khác biệt visual này giữ hai type không đọc giống nhau.
- Coral — accent — dành cho class đang được implement/extend, tức focal type: accent-tint fill, accent stroke. Các inbound inheritance/realization edge của nó tính **gộp thành một** accent element bổ sung, tổng cộng 2 accent element mỗi diagram.

## Relationship vocabulary

Define mọi marker dùng trong `<defs>` và hiển thị đủ cả sáu loại trong legend, kể cả loại không xuất hiện trong body — legend là grammar reference đầy đủ của type này.

| Relationship | Line | Ending — tại target/owner end |
|---|---|---|
| Inheritance (`extends`) | solid | **hollow triangle** lớn — fill `paper`, stroke `ink` |
| Realization (`implements`) | dashed `5,4` | cùng hollow triangle |
| Composition — owns, cascades | solid | **filled diamond** ở OWNER end, fill `ink` |
| Aggregation — has, independent | solid | **hollow diamond** ở OWNER end |
| Association | solid | open arrowhead thường, multiplicity ở CẢ HAI end |
| Dependency — uses | dashed `4,3` | open arrowhead thường |

Multiplicity như `1`, `0..*`, `1..*` dùng Geist Mono 8px, cách box edge 10–12px, nằm trên opaque mask phủ line — cùng convention với ER cardinality label.

## Quy tắc connector

Cả sáu SKILL.md §6 connector rule áp dụng đầy đủ — orthogonal rounded elbow (`r=8`), không diagonal, bridge/hop cho crossing không tránh được, fan attach point cách nhau ≥12px khi nhiều relationship cùng chia một edge, masked label với gap 6–10px, connector vẽ trước box. Ưu tiên layout class sao cho relationship resolve thành straight line hoặc single-elbow route; class diagram mà edge nào cũng bridge là over budget — split theo package.

## Complexity budget

Tối đa 7 class, 8 relationship, 5 member mỗi compartment — overflow thành một line Geist Mono `…` — và 2 accent element. Vượt budget → split theo package.

Bảy là ceiling chứ không phải target. Ba compartment mỗi box làm class diagram nhanh trở nên dense, nên 4–5 class là normal size; shipped example dùng đủ bảy vì đồng thời làm legend cho toàn relationship vocabulary.

## Anti-pattern

- Liệt kê getter/setter như operation — noise; chỉ show behavior có meaning.
- Dump mọi attribute và method — class diagram là một argument, không phải header file.
- Dùng composition và aggregation như nhau — filled diamond nghĩa là part chết cùng whole. Nếu không đúng, dùng hollow diamond.
- Association arrow không multiplicity.
- Vẽ class diagram khi không có inheritance và operation — trường hợp đó là ER.
- Stereotype guillemet trên mọi thứ, thay vì chỉ interface/abstract cần nó.
- Pad box cho bằng chiều cao.

## Ví dụ

- `assets/example-uml-class.html` — minimal light
- `assets/example-uml-class-dark.html` — minimal dark
- `assets/example-uml-class-full.html` — full editorial
