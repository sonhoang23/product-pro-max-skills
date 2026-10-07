# Visual QA Gate

Gate này chạy **sau khi render HTML/SVG và trước khi coi diagram là hoàn tất**. Mục tiêu là bắt các lỗi hình học mà source code hợp lệ vẫn có thể tạo ra khi mở thật trong browser.

## 1. Lỗi fail ngay

Diagram **MUST NOT pass** nếu còn bất kỳ lỗi nào sau:

- text tràn ra ngoài node/container;
- text chạm hoặc quá sát stroke tới mức khó đọc;
- connector không có source/target rõ ràng hoặc arrowhead dừng trong khoảng trắng;
- connector đi xuyên qua node không phải endpoint;
- connector đi xuyên qua text;
- connector/label đè lên nhau làm mất khả năng đọc;
- nhiều connector dùng chung một đoạn path khiến không còn phân biệt được luồng;
- branch label đứng xa nhánh hoặc không rõ thuộc nhánh nào;
- loop/back-edge nhìn như đường treo, không quay về một target rõ;
- node/label bị crop bởi viewBox hoặc viewport mục tiêu.

## 2. Text-fit

Với mọi node có text:

1. giữ padding nhìn thấy được ở cả bốn cạnh;
2. ưu tiên wrap thành 2–3 dòng trước khi giảm font;
3. nếu vẫn chật, tăng width/height node;
4. chỉ rút wording khi không làm mất semantics;
5. không dùng font nhỏ để ép nội dung vào node.

Kiểm tra ở **100% zoom** trong viewport mục tiêu, không chỉ bằng tọa độ SVG.

## 3. Endpoint và routing

Mỗi connector phải thỏa tất cả:

- source attach point nằm trên perimeter của source node;
- target attach point nằm trên perimeter của target node;
- arrowhead chạm target perimeter, không dừng trước node và không chui vào giữa node;
- connector lệch trục dùng elbow vuông góc, không diagonal;
- khi nhiều connector vào cùng một edge, mỗi connector có attach point riêng, cách nhau đủ nhìn thấy;
- path không được đi xuyên vùng bounding box của node khác;
- loop/back-edge phải dùng corridor riêng ngoài vùng node chính.

Nếu connector không thể route sạch trong layout hiện tại, **đổi layout hoặc tăng canvas**, không cố nhét thêm bend.

## 4. Branch label

- Label phải nằm sát nhánh mà nó mô tả.
- Không đặt label tại giao điểm nhiều đường.
- Label trên line phải có opaque mask/background.
- Khoảng hở giữa text và stroke phải nhìn thấy rõ.
- Label không được nằm trong node trừ khi nó là nội dung của node đó.

## 5. Phân bố không gian

Trước khi kết thúc:

- không để một vùng quá chật trong khi vùng khác trống lớn vô cớ;
- nhóm node theo flow/cụm logic trước khi route connector;
- ưu tiên flow chính đọc theo một hướng nhất quán;
- nếu loop/back-edge chiếm nhiều diện tích hơn flow chính, cân nhắc bố trí lại hoặc tách diagram.

## 6. Browser visual pass

Khi môi trường cho phép render browser/screenshot, MUST kiểm tra hình render thật. Tối thiểu kiểm tra:

- overflow;
- clipping;
- node-text collision;
- line-node collision;
- line-text collision;
- connector overlap;
- orphan label;
- arrowhead/endpoint anchoring;
- readability ở 100% zoom.

Static source inspection **không thay thế** browser visual pass khi browser/screenshot có sẵn.

## 7. Checklist pass/fail

### Text
- [ ] Không text nào tràn viền.
- [ ] Không text nào quá sát stroke.
- [ ] Nội dung đọc rõ ở 100% zoom.

### Connector
- [ ] Mọi connector có source/target rõ.
- [ ] Arrowhead chạm đúng target perimeter.
- [ ] Không connector nào xuyên node.
- [ ] Không connector nào xuyên text.
- [ ] Không có path treo hoặc dừng giữa khoảng trắng.
- [ ] Không có overlap làm mất khả năng phân biệt luồng.

### Branch label
- [ ] Mỗi label gắn rõ với đúng branch.
- [ ] Label không đè node/text/connector khác.
- [ ] Label trên connector có mask và khoảng hở.

### Layout
- [ ] Flow chính đọc tự nhiên.
- [ ] Loop/back-edge có corridor riêng.
- [ ] Không có vùng quá chật/quá trống bất hợp lý.
- [ ] Không nội dung nào bị crop khỏi viewBox.

Chỉ khi toàn bộ mục bắt buộc pass mới được báo diagram hoàn tất.
