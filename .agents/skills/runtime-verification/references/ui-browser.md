# UI / Browser Runtime Failure Patterns

Prefix chính: `UI-*`, `BROWSER-*`

Dùng cho failure pattern liên quan hydration, browser console/runtime error, rendering, interaction, viewport hoặc browser-only behavior.

---

## UI-001 — Polymorphic component làm sai semantic element của navigation/action

**Applies when**

Design system/component library hỗ trợ polymorphic composition như `asChild`, `render`, slot hoặc wrapper để render Button bằng Link/anchor hay ngược lại.

**Symptom**

UI nhìn đúng và click được nhưng DOM/accessibility tree sai, ví dụ anchor có `role="button"`, navigation action không còn role `link`, keyboard/focus behavior lệch, hoặc test accessibility/query theo role fail.

**General root cause**

Styling/interaction primitive giữ semantics mặc định của Button khi underlying element thực tế là Link/anchor; abstraction che mất khác biệt giữa navigation và state-changing action.

**Why tests miss it**

Snapshot/visual test chỉ thấy giao diện; click test có thể vẫn pass. Lỗi thường chỉ lộ qua role-based test, accessibility warning, keyboard navigation hoặc browser audit.

**Task-generation rule**

Khi pattern áp dụng:
1. navigation phải dùng semantic `<a>/<Link>` thật;
2. state-changing action phải dùng semantic `<button>`;
3. nếu muốn style giống button cho link, dùng styling primitive/variant class thay vì ép Button semantics lên anchor;
4. test primary actions bằng accessible role + href/keyboard behavior, không chỉ click callback;
5. với pagination, disabled/read-only control hoặc polymorphic primitive khác, xác định semantic intent trước khi đổi test expectation; expose native `disabled` hoặc `aria-disabled` phù hợp và không dùng CSS/data attribute như proof accessibility duy nhất;
6. không sửa test để chấp nhận role sai nếu contract UX là navigation/action khác với DOM hiện tại.

**Required evidence**

DOM/accessibility tree có đúng role theo intent; navigation giữ `href`; action/pagination/disabled control có role và disabled semantics đúng; focus/keyboard hoạt động, không có semantic/accessibility warning liên quan và role-based frontend test pass.


---

## BROWSER-001 — Browser test package đã cài nhưng browser executable/payload chưa sẵn sàng

**Applies when**

E2E/browser automation dùng Playwright/Puppeteer/Selenium hoặc tool tương tự mà package JavaScript và browser binary/payload được cài/materialize riêng.

**Symptom**

Test suite fail trước interaction đầu tiên với lỗi executable/browser revision không tồn tại, missing headless shell hoặc yêu cầu chạy browser-install command dù package dependency đã hiện diện.

**General root cause**

Dependency graph chỉ bảo đảm test library tồn tại; browser runtime payload là artifact riêng theo OS/version/cache và chưa được materialize hoặc đã bị xóa/không tương thích.

**Why tests miss it**

Typecheck/import package và package-manager install có thể pass mà chưa launch browser binary thật.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định browser project/version mà config sẽ launch;
2. materialize/install browser payload theo toolchain chính thức trên target OS;
3. chạy browser launch smoke trước khi quy lỗi cho app;
4. phân loại missing executable/payload là environment BLOCKED, không phải UI product FAIL;
5. sau khi browser launch được mới chạy app journey.

**Required evidence**

Test package version và browser project được xác định, browser install/materialization command thành công khi cần, launch smoke pass trên target environment và app test chỉ được đánh giá sau khi browser runtime thực sự khởi động.

---

## BROWSER-002 — Selective browser smoke bị báo cáo như full critical journey coverage

**Applies when**

Browser suite có nhiều project/locale/viewport hoặc một số smoke test ngắn, trong khi acceptance yêu cầu chuỗi business journey nhiều bước/screen/entity.

**Symptom**

Summary như "8 passed" nghe đầy đủ vì cùng hai test chạy trên bốn browser projects, nhưng thực tế chỉ cover entry page, auth probe, một validation hoặc mobile overflow; các bước create/update/drill-down còn lại chưa hề được thực thi.

**General root cause**

Coverage được suy từ test count/project matrix thay vì mapping acceptance journey → test steps/assertions. Cùng một smoke case chạy nhiều configurations bị nhầm thành nhiều business scenarios khác nhau.

**Why tests miss it**

Runner chỉ biết test case đã khai báo pass; nó không biết acceptance/quickstart còn các bước ngoài suite nếu không có traceability mapping.

**Task-generation rule**

Khi pattern áp dụng:
1. lập mapping từng bước của critical journey/acceptance scenario tới browser test cụ thể;
2. ghi route/domain state và mutation/request evidence cho bước ghi dữ liệu quan trọng;
3. tách coverage dimension (locale/device/timezone) khỏi business-step coverage;
4. bước chưa chạy phải giữ `NOT_COVERED/unavailable`, không suy từ smoke khác;
5. chỉ gọi full journey PASS khi toàn bộ required step mapping đã có runtime evidence.

**Required evidence**

Có traceability từ acceptance/quickstart step tới test case/assertion, số test theo project được giải thích, mutation/navigation quan trọng có evidence và mọi bước bắt buộc đều được thực thi. Selective smoke pass chỉ được báo cáo đúng scope smoke của nó.

---

## BROWSER-003 — Device timezone che giấu lỗi operating-timezone presentation/conversion

**Applies when**

Product có business/operating timezone riêng, frontend hiển thị instant hoặc dùng `datetime-local`, và browser/device timezone có thể khác timezone vận hành.

**Symptom**

Date/time nhìn đúng trên máy developer vì device timezone trùng operating timezone, nhưng bị shift ngày/giờ hoặc submit sai ISO instant ở timezone khác; locale switch có thể che hoặc làm lỗi khó nhận ra hơn. Framework/i18n có thể chỉ phát warning kiểu timezone/environment fallback nên command vẫn exit 0 dù server/client có nguy cơ format khác nhau.

**General root cause**

Formatter/converter vô tình dùng browser/device timezone mặc định thay vì timezone authority của domain; verification chỉ chạy trong một timezone nên không tạo độ lệch đủ để lộ bug.

**Why tests miss it**

Unit test formatter có thể mock giá trị hẹp; browser trên máy local mặc định trùng timezone vận hành nên cùng instant vẫn hiển thị "đúng" tình cờ.

**Task-generation rule**

Khi pattern áp dụng:
1. lấy operating timezone từ authority thật của feature/config/API thay vì hard-code theo device;
2. chạy cùng một business instant trên ít nhất một browser timezone khác operating timezone;
3. kiểm cả presentation và `datetime-local → ISO instant` submit conversion khi có editable instant;
4. nếu locale là requirement, chạy locale matrix nhưng không dùng locale như proxy cho timezone;
5. date-only civil value phải được kiểm riêng để không bị shift vì instant conversion;
6. framework/i18n timezone fallback warning thuộc runtime boundary phải được phân loại và cấu hình global operating timezone rõ ràng khi product có authority cố định; không bỏ qua chỉ vì page vẫn render.

**Required evidence**

Cùng business instant cho kết quả presentation đúng theo operating timezone trên browser/device timezone khác nhau; submit từ local datetime tạo đúng ISO instant theo operating timezone; timezone authority được probe từ source runtime/config thật khi contract yêu cầu.


---

## UI-002 — Live formatting làm hỏng caret và chuỗi nhập bàn phím

**Applies when**

Controlled input format giá trị ngay trong lúc gõ như tiền tệ, số có separator, phone/card number hoặc mask khác; mỗi keystroke có thể thay đổi độ dài/position của displayed string.

**Symptom**

Parser/formatter riêng đều đúng và paste có thể đúng, nhưng gõ từng phím tạo kết quả sai như `55000 → 5.500` hoặc `130000 → 1.300`; caret nhảy vào giữa chuỗi sau khi formatter chèn separator, khiến ký tự tiếp theo được insert sai vị trí.

**General root cause**

Component replace displayed value sau mỗi change nhưng không bảo toàn semantic caret position theo dữ liệu canonical; browser/userEvent tiếp tục gõ tại caret cũ/new DOM position không tương ứng với số digit người dùng vừa nhập.

**Why tests miss it**

Unit test formatter thường chỉ assert `format("55000") === "55.000"`; paste/change một lần cũng có thể pass. Bug chỉ lộ với sequential keyboard typing và caret movement thật.

**Task-generation rule**

Khi live-format input áp dụng:
1. test phải dùng sequential keyboard typing, không chỉ paste hoặc một `change` event;
2. component phải map caret theo semantic token/digit position khi displayed string được reformat;
3. kiểm cả append, selection replacement và invalid input nếu scope hỗ trợ;
4. assert displayed value, canonical form state và submitted payload cùng đúng;
5. giữ browser smoke cho critical money/masked input vì caret/selection là browser-sensitive.

**Required evidence**

Sequential typing cho giá trị mong muốn, caret/selection không làm mất hoặc đổi thứ tự ký tự, canonical state đúng và submit payload giữ semantics. Parser-only hoặc paste-only PASS không đủ.

---

## UI-003 — Async Select lộ raw ID khi selected option tạm thời không có trong option data

**Applies when**

Select/Combobox lưu canonical ID nhưng label đến từ async query/cache; flow có create-new-option, optimistic update, refetch/invalidation, selected value có thể tồn tại trước khi option list mới được hydrate, hoặc selected entity đã chọn không còn eligible cho selection mới nhưng vẫn thuộc business history hiện tại.

**Symptom**

Sau khi tạo/chọn entity mới, trigger hiển thị internal value như `subject-2` thay vì human-readable label `MATH · Toán`; lỗi có thể chỉ xuất hiện trong cửa sổ refetch pending/failure rồi tự biến mất khi options về.

**General root cause**

Display label được resolve hoàn toàn từ current option collection của primitive; selected ID được set trước nhưng option label chưa hiện diện/ổn định trong data source, nên primitive fallback sang raw value.

**Why tests miss it**

Happy-path test chờ refetch hoàn tất trước assertion; API/unit test chỉ kiểm selected ID; visual smoke không chạy đúng race create → select → refetch pending/failure.

**Task-generation rule**

Khi async select có contextual create/refetch:
1. giữ stable selected label snapshot hoặc optimistic option cùng canonical ID ngay khi create thành công;
2. selected display không được phụ thuộc hoàn toàn vào refetch hoàn tất nếu user đã có entity label từ create response;
3. test các trạng thái create success → refetch pending, refetch success và refetch failure;
4. internal ID không được leak ra user-facing trigger;
5. nếu selected entity trở thành ineligible/CLOSED nhưng vẫn là current/historical selection, giữ business label + trạng thái nhận biết được và chặn selection mới theo policy; không fallback raw ID;
6. canonical submitted value vẫn phải là ID, không đổi contract chỉ để giữ label.

**Required evidence**

Sau create/select, trigger luôn hiển thị human-readable label trong cả pending/success/failure window; selected entity không còn eligible vẫn giữ label/status có ý nghĩa; submitted form state giữ canonical ID; refetch không làm mất draft/selection và không leak raw identifier ra UI.


---

## UI-004 — Dynamic controlled field có blank value không tương thích validation schema

**Applies when**

Form dùng controlled/dynamic field như React Hook Form `Controller`, field array, record/map field hoặc form library tương tự; field có thể được render theo dữ liệu runtime và business flow cho phép người dùng để trống, trong khi validation schema/resolver yêu cầu một kiểu cụ thể như `string`, `number` hoặc object.

**Symptom**

Các field người dùng nhìn thấy đều hợp lệ nhưng submit không gọi mutation/request; callback `onSubmit` hoặc mutation spy có call count bằng 0; form không hiện nguyên nhân rõ ràng hoặc lỗi nằm ở một dynamic field người dùng chưa tương tác. Trường hợp điển hình: một allocation/input động tồn tại trong form state dưới dạng `undefined`, nhưng schema yêu cầu `string`; blank business state lẽ ra hợp lệ nhưng resolver chặn trước API.

**General root cause**

Dynamic controlled field được mount mà không có initial/default value tương thích schema. Form library giữ `undefined` cho field chưa tương tác, trong khi schema coi field đã tồn tại thì phải có canonical blank representation khác như `""`, `null`, `[]` hoặc object hợp lệ.

**Why tests miss it**

Happy-path thường nhập mọi field hoặc mock submit trực tiếp; API/E2E backend không thấy request vì failure xảy ra trước transport. Test có thể tập trung vào field chính như amount/date/method và bỏ qua dynamic child field không nhập.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định canonical blank state của từng dynamic controlled field theo business rule và schema;
2. cung cấp `defaultValue`/initial value tương thích schema thay vì để `undefined` ngẫu nhiên, trừ khi schema chủ động cho phép optional/undefined;
3. test case phải cover field động được render nhưng người dùng không nhập khi business rule cho phép để trống;
4. khi submit không gọi mutation/request, kiểm resolver/form-state errors và registration/default state trước khi quy lỗi cho API, mutation hook hoặc network;
5. payload builder phải loại bỏ hoặc chuyển blank state theo contract, không đổi business semantics chỉ để làm schema pass;
6. test thêm case field có nhập để bảo đảm validation/payload vẫn đúng.

**Required evidence**

Blank dynamic field hợp lệ đi qua resolver và submit/mutation được gọi đúng khi business rule cho phép; field có nhập vẫn validate đúng; payload giữ canonical semantics và không gửi giá trị rỗng sai contract; không còn hidden `undefined` chặn submit trước transport.

---

## UI-005 — Select/Combobox closed state lộ raw canonical value thay vì user-facing label

**Applies when**

Select/Combobox lưu canonical value như enum/code/id/number nhưng option có label user-facing khác, đặc biệt khi dùng third-party primitive như Base UI/Radix/custom Select và trigger/closed state được primitive tự render. Pattern cũng áp dụng khi selected entity đã chọn không còn eligible cho selection mới nhưng vẫn thuộc lịch sử/current relationship.

**Symptom**

Danh sách option mở hiển thị label đúng nhưng sau khi chọn hoặc ở initial/default state, trigger đóng hiển thị raw value như `2`, `SESSION_PRICE`, `NONE` hoặc internal code thay vì label như `Thứ Ba`, `Theo giá buổi học`. Lỗi có thể xuất hiện dù option data đã đầy đủ và không có async race.

**General root cause**

Implementation giả định primitive sẽ tự map selected value sang option label trong closed state; thực tế primitive/value renderer fallback sang raw canonical value hoặc cần explicit label/value rendering contract.

**Why tests miss it**

Test thường chỉ kiểm option list, selected canonical value hoặc payload; unit test có thể click option rồi không assert text của closed trigger. API/domain tests đúng vì canonical enum/id vẫn chính xác nên presentation defect không lộ.

**Task-generation rule**

Khi Select có canonical value khác display label:
1. test cả option-open state và closed trigger state;
2. kiểm initial/default selection và selection sau interaction;
3. closed trigger phải render localized/user-facing label, không raw enum/id/code;
4. canonical form/API value vẫn giữ nguyên; không đổi domain enum/id chỉ để sửa presentation;
5. nếu primitive không bảo đảm label mapping, app-level trigger phải resolve/render label explicit mà không hand-edit shared library ngoài scope;
6. nếu selected entity không còn eligible, closed state vẫn phải giữ business label/status và disabled/read-only explanation phù hợp thay vì raw value;
7. với primitive có portal/focus/keyboard behavior, giữ browser smoke/E2E để kiểm closed/open semantics và accessibility.

**Required evidence**

Closed trigger hiển thị đúng user-facing/localized label cho initial value, sau selection và khi selected entity trở thành ineligible; canonical form state/request payload vẫn là value chuẩn; option list và keyboard/focus behavior không regress; không leak raw enum/id/code ra primary UI.

---

## UI-006 — Conditional payload transformation âm thầm làm mất dữ liệu người dùng

**Applies when**

Form hoặc mutation payload có field phụ thuộc/nhóm optional/nested object và frontend dùng điều kiện, `.filter()`, `.map()`, normalization hoặc payload builder để quyết định dữ liệu nào được gửi; người dùng có thể nhập một phần dữ liệu trước khi nhóm đó trở thành hoàn chỉnh theo business rule.

**Symptom**

UI có thể báo lưu thành công hoặc request vẫn thành công, nhưng một phần dữ liệu người dùng vừa nhập biến mất sau refetch/reload vì payload builder đã bỏ field/row/group không hoàn chỉnh. Ví dụ tổng quát: nested contact chỉ có một field được nhập nên cả object bị đổi thành mảng rỗng, hoặc một row có note nhưng thiếu status nên row bị filter khỏi payload.

**General root cause**

Frontend trộn hai khái niệm khác nhau: “dữ liệu chưa hợp lệ để persist” và “người dùng chưa nhập dữ liệu”. Conditional transformation coi partial user input như empty state rồi loại bỏ im lặng thay vì giữ draft hoặc chặn submit với lỗi có thể sửa.

**Why tests miss it**

Happy-path thường chỉ cover empty hoàn toàn và complete hoàn toàn; request test có thể chỉ assert status success mà không kiểm payload hoặc round-trip state. Backend không thể phát hiện dữ liệu đã bị frontend bỏ trước transport.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định rõ canonical state cho empty, partial và complete của từng dependent group/row;
2. mọi non-empty user input phải hoặc được persist hợp lệ, hoặc submit bị chặn với field/group error rõ ràng; không được silently drop;
3. payload builder không được dùng filter/normalization để biến partial input thành “không tồn tại” nếu business rule yêu cầu người dùng sửa;
4. nếu business rule chưa cho phép persist, giữ draft người dùng hoặc giải thích rõ dữ liệu nào chưa thể lưu;
5. test tối thiểu empty + từng partial shape quan trọng + complete;
6. với mutation quan trọng, kiểm payload thực tế và round-trip sau refetch/reload, không chỉ success toast/status;
7. nếu một action khóa/chuyển trạng thái làm dữ liệu draft không còn persist được, phải validate/confirm trước mutation thay vì bỏ dữ liệu sau mutation.

**Required evidence**

Empty state hợp lệ vẫn hoạt động; mọi partial non-empty state hoặc được chặn với lỗi đúng field/group và giữ input, hoặc được persist theo contract; complete state persist đúng. Payload không silently drop dữ liệu người dùng và round-trip/refetch chứng minh dữ liệu đã nhập còn tồn tại sau mutation.


---

## UI-007 — Confirmed write không hội tụ sang dependent read surfaces

**Applies when**

Một create/update/lifecycle mutation làm thay đổi nhiều read model hoặc màn hình phụ thuộc trực tiếp, ví dụ create entity → list/selectors/overview, enrollment → student history + class roster, attendance/payment → tuition/overview.

**Symptom**

Server đã xác nhận write thành công nhưng màn hình khởi phát hoặc màn hình phụ thuộc vẫn hiện dữ liệu cũ; user phải refresh, đổi search/filter hoặc navigation vòng để “đánh thức” dữ liệu mới.

**General root cause**

Mutation chỉ invalidate/refetch một query cục bộ, query-key/dependency family không đầy đủ, HTTP/cache semantics giữ stale representation, hoặc flow không định nghĩa bề mặt nào phải hội tụ sau confirmed write.

**Why tests miss it**

Mutation unit test chỉ assert POST/PATCH success; component test thường mock cache ở một màn hình; static review thấy invalidate call nhưng không chứng minh user-visible read model đã đổi. Bug chỉ lộ khi đi xuyên nhiều screen/query thật.

**Task-generation rule**

Khi pattern áp dụng:
1. liệt kê dependency family của từng mutation ngay trong spec/tasks: initiating surface + direct dependent surfaces cần cho bước nghiệp vụ tiếp theo;
2. prime/read các surface trước mutation để tránh false pass do cold cache;
3. sau confirmed write, verify từng dependent surface hội tụ mà không refresh/search workaround;
4. nếu acceptance có convergence window, đo/quan sát window đó; quá ngưỡng phải có syncing/recovery state thay vì stale truth im lặng;
5. navigation quay lại cùng URL/default filter phải revalidate đúng server truth;
6. list/select/aggregate cùng entity phải dùng cùng business identity sau update.

**Required evidence**

Confirmed write có request/response evidence; initiating surface và mọi direct dependent surface quan trọng phản ánh latest server truth trong contract window hoặc hiện syncing/retry rõ; không cần manual refresh/search/filter workaround; revisit cùng URL/default list không resurrect stale state.

---

## UI-008 — Write success bị conflated với dependent read-sync failure

**Applies when**

Mutation write thành công rồi client thực hiện invalidate/refetch/sync nhiều read models và bước read-back có thể fail độc lập với write.

**Symptom**

POST/PATCH đã persist nhưng UI báo “lưu thất bại”, giữ nút Save như thể có thể submit lại, hoặc ngược lại đóng form mà không cho biết dependent data chưa đồng bộ. User có nguy cơ tạo duplicate write vì retry nhầm toàn mutation.

**General root cause**

Frontend gộp write lifecycle và read-sync lifecycle thành một status/error duy nhất; callback/query-sync layer không giữ distinction giữa confirmed mutation và failed dependent refresh.

**Why tests miss it**

Happy-path chỉ cover write+refetch cùng success; error test thường reject mutation trước server confirmation. Ít test case mô phỏng write confirmed rồi một trong các dependent GET fail.

**Task-generation rule**

Khi pattern áp dụng:
1. model riêng write state và sync state;
2. confirmed write không được chuyển ngược thành write failure chỉ vì read-sync fail;
3. read-sync fail phải hiển thị “đã lưu nhưng chưa đồng bộ” hoặc semantics tương đương và Retry chỉ rerun read sync;
4. duplicate submit phải bị chặn khi write đã confirmed;
5. draft/error behavior phải khác giữa write failure và post-write sync failure;
6. test đủ: write fail, write+sync success, write success+sync fail, retry-sync success.

**Required evidence**

Mutation được server xác nhận đúng một lần; read-sync failure tạo recovery state riêng; retry không gửi lại write; dependent surfaces hội tụ sau retry; UI copy/action phân biệt rõ “chưa lưu” với “đã lưu nhưng chưa đồng bộ”.

---

## UI-009 — Older async response ghi đè latest server-confirmed truth

**Applies when**

Hai mutation/refetch/request liên tiếp cùng ảnh hưởng một read model, query/cache có thể hoàn tất out-of-order hoặc người dùng thao tác nhanh trên cùng entity.

**Symptom**

Mutation B đã thành công và UI hiện state mới, nhưng response/refetch từ A hoàn tất muộn rồi ghi đè cache khiến UI quay ngược về state cũ.

**General root cause**

Client áp dụng response theo completion order thay vì logical freshness/version/request identity; không cancel/supersede stale fetch hoặc merge cache thiếu monotonic/latest-write semantics.

**Why tests miss it**

Test tuần tự chờ request A xong rồi mới chạy B nên không tạo race; mock latency đồng nhất; API đúng ở từng request riêng lẻ.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định authority “latest server-confirmed truth wins” cho read model;
2. dùng request identity/version/cancellation/cache primitive phù hợp để stale response không overwrite newer truth;
3. test out-of-order completion có chủ đích;
4. verify cả success-success và write/refetch race;
5. feedback/sync state không được quay về trạng thái cũ vì stale completion.

**Required evidence**

Trong test có A → B nhưng response A hoàn tất sau B; final UI/cache vẫn là truth của B, không rollback label/status/value; request trace hoặc cache assertion chứng minh stale response bị bỏ qua/supersede đúng semantics.

---

## UI-010 — Backend capability tồn tại nhưng operational UI thiếu affordance hoặc editability semantics

**Applies when**

API/domain có update capability cho master/config/profile entity hoặc field, nhưng UI detail/workspace có thể chỉ read-only; một số field chỉ editable khi lifecycle/history cho phép.

**Symptom**

User nhìn thấy dữ liệu nhưng không biết hoặc không thể sửa dù backend hỗ trợ; ngược lại field bị khóa nhưng không có reason. Trong race, form load lúc editable nhưng dependent history phát sinh trước submit, backend từ chối và UI làm mất toàn draft.

**General root cause**

Capability contract, editability authority và UI affordance được phát triển/verify tách nhau; frontend suy editable từ static form design thay vì server/domain state hiện hành.

**Why tests miss it**

Backend E2E chứng minh PATCH hoạt động; frontend snapshot/detail test chỉ render value. Không có audit “editable hoặc intentionally locked” cho từng field/capability và không test write-time editability race.

**Task-generation rule**

Khi pattern áp dụng:
1. inventory update capability từ spec/API/domain và map từng field thành editable hoặc intentionally locked;
2. editable field phải có affordance, validation và save feedback;
3. locked field phải có disabled/read-only semantics + business reason;
4. history-sensitive editability phải lấy từ authority phù hợp, không chỉ hard-code frontend;
5. với write-time lock race: giữ draft field khác, reload editability/server truth, khóa field nguy hiểm và cho retry phần còn editable;
6. update future config không được rewrite persisted historical snapshots ngoài authority.

**Required evidence**

Mỗi scoped field có trạng thái editable hoặc locked-with-reason rõ; API capability có UI path tương ứng khi được phép; race từ editable → locked giữ draft hợp lệ và retry được; persisted history/snapshot invariant vẫn giữ nguyên.

---

## UI-011 — Fixed-page collection làm record hoặc selector option không discoverable

**Applies when**

List/select/combobox/roster/history có dữ liệu có thể vượt page size và client chỉ fetch một page cố định hoặc pagination/search/filter/order semantics chưa được verify trên dataset lớn.

**Symptom**

Record hợp lệ ngoài page 1 “biến mất”; user chỉ tìm thấy khi nhập search như workaround; selector không chứa entity cần chọn; clear search không khôi phục default list; records nhảy trang do order không deterministic.

**General root cause**

Implementation ngầm giả định dataset nhỏ hoặc current page đại diện toàn collection; pagination/search/filter/reset/order được làm ở nhiều tầng không cùng contract.

**Why tests miss it**

Fixture thường ít hơn pageSize; unit test chỉ assert page 1; search test không tạo dataset vượt page; selector happy-path luôn dùng option ở page đầu.

**Task-generation rule**

Khi pattern áp dụng:
1. test dataset > pageSize;
2. cung cấp pagination/load-more/server search phù hợp để mọi record hợp lệ discoverable;
3. filter/search change phải reset page hợp lý và clear-search khôi phục default state;
4. default ordering phải deterministic với tie-break identity;
5. selected option không được mất label chỉ vì nằm ngoài current page hoặc trở thành ineligible;
6. selector collection lớn không được hard-code fixed small page như toàn universe.

**Required evidence**

Record ngoài page 1 truy cập được bằng navigation dự kiến; search/clear-search/page transition đúng; repeated reads cho order ổn định; selector tìm/giữ được business label của entity ngoài current page; không cần workaround nhập search chỉ để dữ liệu tồn tại xuất hiện.

---

## UI-012 — Confirm action không giải phóng modal/focus-inert boundary

**Applies when**

Dialog/AlertDialog/Sheet/headless primitive bọc state-changing confirmation và framework dùng portal, focus trap hoặc inert background.

**Symptom**

Confirm mutation chạy thành công nhưng modal vẫn mở hoặc background vẫn inert; hoặc ngược lại, modal tự đóng ngay khi user bấm confirm dù mutation trả stale/conflict/error và UX cần giữ dialog mở để sửa/reconfirm. Success status/toast phía sau có thể render nhưng user/accessibility tree không truy cập được; focus không trở lại surface hợp lý.

**General root cause**

Confirm control dùng sai lifecycle của dialog library: có thể chỉ style/compose giống close action nhưng không giải phóng portal/focus trap sau success, hoặc dùng chính close/action primitive auto-close dù outcome của mutation chưa được biết. Với controlled dialog, open-state transition có thể chạy trước mutation callback nên error/stale flow mất context cần để retry/reconfirm.

**Why tests miss it**

Mutation spy/assertion pass; snapshot thấy dialog + content hợp lệ; jsdom có thể không phản ánh inert/focus giống browser. Chỉ browser/accessibility query sau confirm mới lộ page vẫn bị khóa.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định rõ close semantics của primitive đang dùng: primitive auto-close chỉ phù hợp khi click đồng nghĩa completion cuối cùng; nếu mutation có thể stale/conflict/error cần giữ context thì dùng non-close action + controlled `open` và chỉ đóng sau confirmed success;
2. không đóng trước khi semantics yêu cầu mutation outcome; stale/conflict/error phải giữ hoặc phục hồi đủ context để retry/reconfirm;
3. sau confirmed success verify dialog removed/closed, background không còn inert và focus recovery hợp lý;
4. success/error feedback phải accessible trong active interaction context;
5. giữ browser smoke cho portal/focus/inert behavior.

**Required evidence**

Sau confirm, modal/focus trap đóng đúng contract; background không còn inert; focus có destination hợp lý; success/error feedback accessible; mutation không bị duplicate khi user thao tác lại.

---

## BROWSER-004 — Desktop verification che giấu mobile-only operational regression

**Applies when**

Critical workflow hỗ trợ mobile/responsive layout, desktop/mobile render khác representation hoặc action/feedback phụ thuộc viewport, hover, dense table, sheet/drawer.

**Symptom**

Desktop journey pass nhưng mobile có horizontal overflow, action bị khuất, touch target khó dùng, hover-only explanation, sheet không scroll/submit được hoặc mobile cards cho business result khác desktop.

**General root cause**

Responsive UI được xem như styling detail thay vì runtime interaction surface; verification chỉ chạy desktop hoặc chỉ kiểm screenshot/overflow mà không chạy cùng business action trên mobile.

**Why tests miss it**

jsdom không có layout engine đầy đủ; desktop browser pass không exercise mobile branch; cùng test count trên nhiều projects có thể vẫn thiếu mobile-relevant steps.

**Task-generation rule**

Khi pattern áp dụng:
1. xác định danh sách flow mobile-relevant từ spec/acceptance;
2. chạy cùng business result trên ít nhất các viewport project được product hỗ trợ;
3. kiểm overflow, scroll, focus, touch/click target, action visibility và feedback semantics;
4. không dùng hover làm cách duy nhất để giải thích state/error;
5. tách business-step coverage khỏi viewport matrix, nhưng mỗi mobile-required step phải có runtime proof.

**Required evidence**

Các mobile-required flow hoàn tất cùng business result như desktop; không horizontal overflow cản thao tác; primary actions/feedback accessible và usable; sheet/dialog/list/pagination hoạt động ở viewport target; không có hover-only critical information.
