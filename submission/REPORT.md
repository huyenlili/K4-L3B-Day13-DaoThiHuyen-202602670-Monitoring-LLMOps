# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

* **Họ và tên:** **Đào Thị Huyền**
* **MSSV:** **202602670**
* **Lớp:** K4-L3B
* **Repository URL:** **https://github.com/huyenlili/K4-L3B-2A20260267-DaoThiHuyen**
* **Commit SHA cuối:** **[CHƯA CÓ — chạy `git rev-parse HEAD`]**
* **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`
* **Tên project Langfuse cá nhân:** `day13-k4-l3b-202602670`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | ![alt text](image.png) |
| Log validator | ![alt text](image-1.png) |
| Dashboard validator | ![alt text](image-2.png) |
| Structured log | ![alt text](image-5.png)|
| PII redaction | ![alt text](image-6.png) |
| Trace list | ![alt text](image-7.png) |
| Trace waterfall | ![alt text](image-8.png) |
| Trace metadata | ![alt text](image-11.png) ![alt text](image-12.png) |
| Prompt versions | submission\evidence\image-13.png |
| Prompt rollback | submission\evidence\image-14.png|
| Dashboard runtime | submission\evidence\image-15.png |
| Incident metric | submission\evidence\image-16.png |
| Incident log | submission\evidence\image-17.png |
| Incident trace | `evidence/14-incident-trace.png` |                                      |

## 3. Kết quả kỹ thuật

| Nội dung                | Baseline                        | Kết quả cuối                     | Nhận xét                                                                                                                                                                                                                      |
| ----------------------- | ------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validate_logs.py`      | Chưa có baseline riêng          | **100/100**                      | 106 log records được phân tích; 0 record thiếu required fields; 0 record thiếu enrichment/context; 47 correlation IDs; 0 PII leak. Basic JSON schema, correlation ID propagation, log enrichment và PII scrubbing đều PASSED. |
| `validate_dashboard.py` | Chưa có baseline riêng          | **HỢP LỆ: 6/6 panel**            | Dashboard contract có đầy đủ 6/6 panel yêu cầu.                                                                                                                                                                               |
| `pytest`                | Chưa có baseline riêng          | **25 passed, 2 subtests passed** | Toàn bộ test cuối đều pass, thời gian chạy 3.98 giây.                                                                                                                                                                         |
| Số traces hợp lệ        | **[CHƯA CÓ]**                   | **[CHƯA CÓ]**                    | Cần lấy từ Langfuse Trace List/validator.                                                                                                                                                                                     |
| Số PII leak             | **[CHƯA CÓ]**                   | **0**                            | `validate_logs.py` xác nhận không phát hiện potential PII leak.                                                                                                                                                               |
| Latency P95 / TTFT P95  | **[CHƯA CÓ] ms / [CHƯA CÓ] ms** | **[CHƯA CÓ] ms / [CHƯA CÓ] ms**  | Cần lấy từ Dashboard runtime.                                                                                                                                                                                                 |
| Retrieval success rate  | **[CHƯA CÓ] %**                 | **[CHƯA CÓ] %**                  | Cần lấy từ Dashboard runtime.                                                                                                                                                                                                 |

### Kết quả validator đã xác nhận

`validate_logs.py`:

* Total log records analyzed: **106**
* Records with missing required fields: **0**
* Records with missing enrichment (context): **0**
* Unique correlation IDs found: **47**
* Potential PII leaks detected: **0**
* Basic JSON schema: **PASSED**
* Correlation ID propagation: **PASSED**
* Log enrichment: **PASSED**
* PII scrubbing: **PASSED**
* Estimated Score: **100/100**

`validate_dashboard.py`:

* **HỢP LỆ: 6/6 panel có trong dashboard contract.**

`pytest`:

* **25 passed**
* **2 subtests passed**
* Thời gian: **3.98s**

## 4. Logging và PII

* **Cách tạo/nhận và truyền correlation ID:** correlation ID được dùng làm định danh xuyên suốt request, log và Langfuse trace. Giá trị correlation ID được truyền vào agent và được đưa vào metadata của trace, giúp liên kết request giữa các lớp observability. **[Cần kiểm tra chính xác middleware/header nếu report yêu cầu mô tả code chi tiết.]**

* **Các metadata được ghi vào structured log:** các trường thực tế cần đối chiếu trực tiếp với `data/logs.jsonl`. Các trường đã được validator kiểm tra về schema/enrichment và correlation ID. **[CẦN CHỤP/ĐỐI CHIẾU STRUCTURED LOG ĐỂ LIỆT KÊ CHÍNH XÁC TÊN FIELD.]**

* **Cách bảo đảm PII được scrub trước khi ghi:** hệ thống có cơ chế PII scrubbing trước khi log được ghi. Kết quả validator xác nhận **0 potential PII leaks** và mục **PII scrubbing = PASSED**.

* **Cách kiểm chứng kết quả:** chạy:

```powershell
python scripts/validate_logs.py
```

Kết quả cuối xác nhận **0 potential PII leaks**, **0 missing required fields** và **0 missing enrichment/context**. Evidence tương ứng: `evidence/04-structured-log.png` và `evidence/05-pii-redaction.png`.

## 5. Tracing và prompt versioning

* **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** trace được kiểm tra trong project Langfuse cá nhân `day13-k4-l3b-202602670`. Việc xác nhận cuối cùng cần đối chiếu trace ID/correlation ID trong Langfuse với log được tạo từ máy của học viên. **[CẦN XÁC NHẬN BẰNG ẢNH TRACE LIST/METADATA.]**

* **Cấu trúc root/retrieval/generation observations:** root `lab-agent-run` (agent) chứa hai observation con: `retrieval` (`@observe` trên `retrieve()` trong `app/mock_rag.py`, type span) và `generation` (`@observe` trên `FakeLLM.generate()` trong `app/mock_llm.py`, type generation, có `model` và `usage_details` input/output). Prompt managed được truyền cho generation qua `propagate_attributes(prompt=...)`.

* **Cách nối trace với log:** `correlation_id` trong structured log được sử dụng để liên kết request với trace tương ứng trong Langfuse. Có thể dùng correlation ID để đối chiếu log của request với metadata/attributes của trace.

* **Prompt name:** **[CHƯA CÓ — cần xác nhận từ Langfuse prompt/evidence]**

* **Version/label baseline:** **[CHƯA CÓ — cần ảnh Prompt Versions]**

* **Version/label candidate:** **[CHƯA CÓ — cần ảnh Prompt Versions]**

* **Trace ID của mỗi version:** baseline **[CHƯA CÓ]**; candidate **[CHƯA CÓ]**

* **Cách promote và rollback `production`:** candidate được promote bằng cách gắn label `production` cho version candidate; rollback thực hiện bằng cách gắn lại label `production` cho version baseline. **[CẦN ĐỐI CHIẾU VỚI THAO TÁC THỰC TẾ/ẢNH PROMPT ROLLBACK.]**

## 6. Dashboard, SLO và alerts

* **Dashboard và sáu panel:** Streamlit (`scripts/dashboard.py`, chạy bằng `streamlit run scripts/dashboard.py`) đọc trực tiếp `data/logs.jsonl`, time range 60 phút, tự refresh 30 giây, đúng sáu panel trong `config/dashboard.yaml`: Latency (P50/P95/P99 + TTFT P95, ms, threshold P95 ≤ 3000), Traffic (request/phút, ≥ 1), Errors (error rate %, breakdown theo `error_type`, retrieval success %, ≤ 2%), Cost (USD, tổng ≤ 2.5), Tokens (in/out, ≤ 50000), Quality (mean, ≥ 0.75). Mỗi panel có đơn vị và đường/nhãn threshold. Phần tính toán tách riêng và có test (`tests/test_dashboard_panels.py`).

* **Kết quả kiểm tra dashboard contract:** `validate_dashboard.py` xác nhận **6/6 panel hợp lệ**.

* **SLO và lý do chọn:** giữ SLO `fast_successful_requests`: 99.5% request `response_sent` có `latency_ms <= 3000` trong 28 ngày. Ngưỡng 3000 ms được sử dụng làm ngưỡng SLO; **P95 baseline thực tế cần lấy từ dashboard runtime: [CHƯA CÓ] ms**.

* **Cách tính error budget:** SLO 99.5% trong 28 ngày nghĩa là error budget 0.5%. Nếu workload có 10,000 request thì tối đa 50 request được phép lỗi hoặc chậm hơn ngưỡng SLO.

* **Ba alert và runbook tương ứng:** `config/alert_rules.yaml` và `docs/alerts.md`, gửi Slack `#k4-l3b-alerts`, owner `student-202602670`:

  1. `HighLatencyP95` — warning, P95 > 3000 ms trong 5 phút.
  2. `HighErrorRate` — critical, error rate > 2% trong 5 phút.
  3. `DailyCostOverBudget` — warning, cost 24 giờ > 2.5 USD trong 15 phút.

Mỗi alert có ảnh hưởng tới người dùng, ba bước kiểm tra Metrics → Logs → Traces và mitigation.

## 7. Điều tra challenge

* **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`

* **Khoảng thời gian điều tra:** **[CHƯA CÓ — cần lấy từ incident evidence/dashboard]**

* **Triệu chứng từ metrics:** **[CHƯA CÓ — cần lấy giá trị thực tế từ `evidence/12-incident-metric.png`]**

* **Log line và correlation ID liên quan:** **[CHƯA CÓ — cần lấy đúng log line từ `evidence/13-incident-log.png`]**

* **Trace ID và span gây ảnh hưởng:** **[CHƯA CÓ — cần lấy từ `evidence/14-incident-trace.png`]**

* **Root cause:** **[CHƯA CÓ — chỉ kết luận sau khi đối chiếu metric → log → trace.]**

* **Fix action:** **[CHƯA CÓ — cần ghi đúng thao tác khôi phục thực tế.]**

* **Preventive measure:** sử dụng các alert/runbook đã định nghĩa trong `config/alert_rules.yaml`, đặc biệt `HighLatencyP95`, `HighErrorRate` và `DailyCostOverBudget` nếu phù hợp với incident thực tế. **[CẦN CHỐT THEO INCIDENT EVIDENCE.]**

## 8. Giải thích và tự đánh giá

* **Một quyết định kỹ thuật quan trọng và lý do:** sử dụng structured logging kết hợp `correlation_id` để có thể liên kết một request xuyên suốt Metrics → Logs → Traces. Cách này giúp quá trình điều tra incident có một định danh chung thay vì phải tìm kiếm thủ công giữa nhiều nguồn dữ liệu.

* **Một lỗi/blocker đã gặp:** **[CẦN ĐIỀN LỖI DAY 13 THỰC TẾ]**

* **Cách tìm nguyên nhân và xử lý:** sử dụng kết quả validator và test để xác nhận từng lớp observability. Với incident, quy trình được thiết kế theo Metrics → Logs → Traces: xác định bất thường từ metrics, tìm request bị ảnh hưởng bằng `correlation_id` trong logs, sau đó kiểm tra trace để xác định observation/span liên quan.

* **Cách hiểu luồng Metrics → Logs → Traces:** Metrics cho biết có bất thường không, ở đâu và từ lúc nào. Logs cho biết request nào bị ảnh hưởng, nhờ `correlation_id`. Traces cho biết span nào (retrieval, generation...) gây ra, nhờ so thời gian và trạng thái các span. Đi đúng thứ tự này thì không phải đoán root cause hay mở trace ngẫu nhiên.

* **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** Prompt version giúp biết thay đổi nào gây ra khác biệt về chất lượng, token và cost, và rollback về version cũ nhanh khi candidate kém hơn. Token/cost cần theo dõi vì một prompt hay lỗi có thể làm output tăng nhiều lần. SLO và error budget cho ngưỡng rõ ràng để quyết định khi nào cảnh báo và khi nào phải dừng thay đổi.

* **Điều quan trọng nhất đã học:** observability không chỉ là ghi log mà cần liên kết được Metrics, Logs và Traces bằng một định danh chung như `correlation_id`. Việc kiểm tra bằng validator và automated tests cũng giúp phát hiện lỗi về schema, enrichment và PII trước khi đưa hệ thống vào vận hành.

* **Hạn chế hoặc phần chưa hoàn thành, nếu có:** một số giá trị runtime và evidence cần được đối chiếu trực tiếp với Langfuse và Dashboard trước khi nộp, gồm trace IDs, prompt versions, latency P95/TTFT P95, retrieval success rate và incident root cause.

## 9. Checklist trước khi nộp

* [ ] Kết quả và evidence thuộc commit SHA cuối.
* [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
* [ ] Incident evidence nối đúng metric → log → trace.
* [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
* [ ] Repository chạy lại được theo README.
* [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
* [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.

### Trạng thái hiện tại

**Đã xác nhận:**

* Log validator: **100/100**
* 106 log records
* 47 unique correlation IDs
* 0 PII leaks
* Dashboard: **6/6 panels hợp lệ**
* Pytest: **25 passed, 2 subtests passed**

**Còn cần lấy trước khi nộp:**

* Commit SHA cuối
* Số traces hợp lệ
* P95 / TTFT P95
* Retrieval success rate
* Prompt name/version/label
* Baseline/candidate trace IDs
* Incident metric → log → trace → root cause
* Một blocker thực tế của Day 13
* Tên file evidence thực tế nếu khác các đường dẫn đang ghi
