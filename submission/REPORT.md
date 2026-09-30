# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

* **Họ và tên:** **Đào Thị Huyền**
* **MSSV:** **202602670**
* **Lớp:** K4-L3B
* **Repository URL:** **https://github.com/huyenlili/K4-L3B-2A20260267-DaoThiHuyen**
* **Commit SHA cuối:** **`9b037711df700115b169a7ec6d8f1916aefd9fcb`**
* **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`
* **Tên project Langfuse cá nhân:** `day13-k4-l3b-202602670`

---

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế.

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
| Prompt rollback | submission\evidence\image-14.png
![alt text](image.png)|
| Dashboard runtime | submission\evidence\image-15.png |
| Incident metric | submission\evidence\image-16.png |
| Incident log | submission\evidence\image-17.png |
| Incident trace | `evidence/14-incident-trace.png` |   

> Lưu ý: nếu tên file evidence thực tế khác các tên trên thì thay bằng đúng tên file trong repository trước khi nộp.

---

## 3. Kết quả kỹ thuật

| Nội dung                | Baseline               | Kết quả cuối                     | Nhận xét                                                                                                                                                                                                                      |
| ----------------------- | ---------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validate_logs.py`      | Chưa có baseline riêng | **100/100**                      | 106 log records được phân tích; 0 record thiếu required fields; 0 record thiếu enrichment/context; 47 correlation IDs; 0 PII leak. Basic JSON schema, correlation ID propagation, log enrichment và PII scrubbing đều PASSED. |
| `validate_dashboard.py` | Chưa có baseline riêng | **HỢP LỆ: 6/6 panel**            | Dashboard contract có đầy đủ 6/6 panel yêu cầu.                                                                                                                                                                               |
| `pytest`                | Chưa có baseline riêng | **25 passed, 2 subtests passed** | Toàn bộ test cuối đều pass, thời gian chạy 3.98 giây.                                                                                                                                                                         |
| Số traces hợp lệ        | Chưa có baseline riêng | **27**                           | Langfuse project cá nhân ghi nhận 27 traces.                                                                                                                                                                                  |
| Số observations         | Chưa có baseline riêng | **56**                           | Langfuse ghi nhận 56 observations.                                                                                                                                                                                            |
| Số PII leak             | Chưa có baseline riêng | **0**                            | `validate_logs.py` xác nhận không phát hiện potential PII leak.                                                                                                                                                               |
| Latency P95 / TTFT P95  | Chưa có baseline riêng | **661 ms / 51 ms**               | Dashboard runtime ghi nhận P95 latency 661 ms và TTFT P95 51 ms.                                                                                                                                                              |
| Retrieval success rate  | Chưa có baseline riêng | **100.0%**                       | Dashboard runtime ghi nhận retrieval success 100%.                                                                                                                                                                            |
| Langfuse trace P95      | Chưa có baseline riêng | **3.31 s**                       | Trace `day13-agent-request` có P95 3.31 s.                                                                                                                                                                                    |
| Langfuse model cost     | Chưa có baseline riêng | **$0.03**                        | Model `claude-sonnet-4-5`, tổng cost Langfuse $0.03.                                                                                                                                                                          |

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

### Langfuse

Langfuse project `day13-k4-l3b-202602670` ghi nhận:

* Total traces: **27**
* Total observations: **56**
* Total model cost: **$0.03**
* Model: **`claude-sonnet-4-5`**
* Scores tracked: **0**

Trace latency của `day13-agent-request`:

| Percentile |    Latency |
| ---------- | ---------: |
| P50        | **0.17 s** |
| P90        | **2.32 s** |
| P95        | **3.31 s** |
| P99        | **4.98 s** |

Generation latency:

| Generation      |   P50 |   P90 |       P95 |   P99 |
| --------------- | ----: | ----: | --------: | ----: |
| `lab-agent-run` | 0.46s | 1.71s | **2.34s** | 4.62s |
| `generation`    | 0.16s | 0.17s | **0.17s** | 0.18s |

Observation latency:

| Observation           |   P50 |   P90 |       P95 |   P99 |
| --------------------- | ----: | ----: | --------: | ----: |
| AGENT `lab-agent-run` | 0.46s | 1.71s | **2.34s** | 4.62s |
| SPAN `retrieval`      | 0.00s | 0.00s | **0.00s** | 0.00s |

---

## 4. Logging và PII

* **Cách tạo/nhận và truyền correlation ID:** correlation ID được sử dụng làm định danh xuyên suốt request, log và Langfuse trace. Giá trị correlation ID được truyền vào agent và đưa vào metadata của trace, giúp liên kết request giữa các lớp observability.

* **Các metadata được ghi vào structured log:** các trường thực tế quan sát được trong `data/logs.jsonl` gồm:

  * `service`
  * `event`
  * `feature`
  * `correlation_id`
  * `user_id_hash`
  * `session_id`
  * `env`
  * `model`
  * `level`
  * `ts`
  * `latency_ms`
  * `ttft_ms`
  * `tokens_in`
  * `tokens_out`
  * `cost_usd`
  * `quality_score`
  * `tool_name`
  * `tool_success`
  * `payload`

* **Cách bảo đảm PII được scrub trước khi ghi:** hệ thống có cơ chế PII scrubbing trước khi log được ghi. User ID được lưu dưới dạng `user_id_hash` thay vì raw identifier. Dữ liệu nhạy cảm trong payload được redact.

  Ví dụ:

  * Số điện thoại → `[REDACTED_PHONE_VN]`
  * Số thẻ → `[REDACTED_CREDIT_CARD]`

* **Cách kiểm chứng kết quả:** chạy:

```powershell
python scripts/validate_logs.py
```

Kết quả cuối xác nhận:

* **0 potential PII leaks**
* **0 missing required fields**
* **0 missing enrichment/context**
* **PII scrubbing = PASSED**
* **Correlation ID propagation = PASSED**
* **Log enrichment = PASSED**

Evidence tương ứng:

* `evidence/04-structured-log.png`
* `evidence/05-pii-redaction.png`

---

## 5. Tracing và prompt versioning

* **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** trace được kiểm tra trong project Langfuse cá nhân `day13-k4-l3b-202602670`. Langfuse dashboard hiện ghi nhận **27 traces** và **56 observations**.

* **Trace name:** `day13-agent-request`.

* **Cấu trúc root/retrieval/generation observations:** root `lab-agent-run` là agent observation. Bên trong có:

  * `retrieval`: observation type span, tương ứng với `retrieve()` trong `app/mock_rag.py`.
  * `generation`: observation type generation, tương ứng với `FakeLLM.generate()` trong `app/mock_llm.py`, có model và usage details input/output.

* **Cách nối trace với log:** `correlation_id` trong structured log được sử dụng để liên kết request với trace tương ứng trong Langfuse. Có thể dùng correlation ID để đối chiếu log của request với metadata/attributes của trace.

* **Model:** `claude-sonnet-4-5`.

* **Prompt name:** cần đối chiếu trực tiếp với Langfuse Prompt Management/evidence; dashboard tổng hợp hiện tại chưa hiển thị prompt name cụ thể.

* **Version/label baseline:** cần đối chiếu với `evidence/13-prompt-versions.png`.

* **Version/label candidate:** cần đối chiếu với `evidence/13-prompt-versions.png`.

* **Trace ID của mỗi version:** cần lấy trực tiếp từ Trace List/Trace Metadata tương ứng; không suy diễn từ dashboard tổng hợp.

* **Cách promote và rollback `production`:** prompt candidate được quản lý thông qua version/label trong prompt management. Rollback cần đối chiếu với evidence thao tác thực tế trong `submission/evidence/image-14.png`.

* **Scores:** Langfuse hiện hiển thị **0 scores tracked**, do đó chưa sử dụng Langfuse score analytics làm nguồn đánh giá quality trong snapshot này.

---

## 6. Dashboard, SLO và alerts

* **Dashboard và sáu panel:** Streamlit (`scripts/dashboard.py`, chạy bằng `streamlit run scripts/dashboard.py`) đọc trực tiếp `data/logs.jsonl`, time range 60 phút và tự refresh 30 giây.

  Sáu panel trong `config/dashboard.yaml` gồm:

  1. **Latency** — P50/P95/P99 + TTFT P95, đơn vị ms, threshold P95 ≤ 3000.
  2. **Traffic** — request/phút, threshold ≥ 1.
  3. **Errors** — error rate %, breakdown theo `error_type`, retrieval success %, threshold ≤ 2%.
  4. **Cost** — USD, threshold tổng ≤ 2.5.
  5. **Tokens** — input/output tokens, threshold ≤ 50000.
  6. **Quality** — mean quality, threshold ≥ 0.75.

* **Kết quả kiểm tra dashboard contract:** `validate_dashboard.py` xác nhận **6/6 panel hợp lệ**.

### Dashboard runtime

| Metric            |     Kết quả |
| ----------------- | ----------: |
| P50 latency       |  **158 ms** |
| P95 latency       |  **661 ms** |
| P99 latency       |  **976 ms** |
| TTFT P95          |   **51 ms** |
| Total requests    |      **10** |
| Average/minute    |    **10.0** |
| Error rate        |   **0.00%** |
| Retrieval success |  **100.0%** |
| Total cost        | **$0.0229** |
| Quality average   |    **0.88** |

* **SLO và lý do chọn:** sử dụng SLO `fast_successful_requests`: **99.5%** request `response_sent` có `latency_ms <= 3000` trong 28 ngày. Ngưỡng 3000 ms được dùng làm ngưỡng SLO.

* **Error budget:** SLO 99.5% tương ứng error budget **0.5%**. Ví dụ, với 10,000 request thì error budget tương ứng là 50 request.

### Ba alert

`config/alert_rules.yaml` và `docs/alerts.md`, gửi Slack `#k4-l3b-alerts`, owner `student-202602670`.

1. `HighLatencyP95` — warning, P95 > 3000 ms trong 5 phút.
2. `HighErrorRate` — critical, error rate > 2% trong 5 phút.
3. `DailyCostOverBudget` — warning, cost 24 giờ > 2.5 USD trong 15 phút.

Mỗi alert có hướng điều tra theo:

**Metrics → Logs → Traces**

---

## 7. Điều tra challenge

* **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`

* **Khoảng thời gian điều tra:** chưa xác định từ evidence incident được cung cấp trong report.

* **Triệu chứng từ metrics:** chưa có đủ evidence để kết luận scenario incident cụ thể.

* **Log line và correlation ID liên quan:** cần đối chiếu trực tiếp với `evidence/17-incident-log.png` hoặc file incident log thực tế.

* **Trace ID và span gây ảnh hưởng:** cần đối chiếu trực tiếp với `evidence/14-incident-trace.png`.

* **Root cause:** chỉ kết luận sau khi đối chiếu đầy đủ **metric → log → trace**; không suy diễn root cause khi chưa có incident evidence.

* **Fix action:** cần ghi theo thao tác khôi phục thực tế đã thực hiện đối với scenario incident.

* **Preventive measure:** sử dụng alert và runbook trong `config/alert_rules.yaml` và `docs/alerts.md`. Các alert chính gồm `HighLatencyP95`, `HighErrorRate` và `DailyCostOverBudget`.

### Incident investigation workflow

Quy trình điều tra được thiết kế như sau:

**Metrics → Logs → Traces**

1. Metrics phát hiện bất thường về latency, error rate hoặc cost.
2. Logs sử dụng `correlation_id` để xác định request bị ảnh hưởng.
3. Langfuse trace được sử dụng để xác định observation/span liên quan.
4. So sánh latency và trạng thái của `retrieval`, `generation` và agent observation.
5. Xác định root cause dựa trên evidence thay vì chỉ dựa trên triệu chứng metrics.
6. Áp dụng mitigation/fix và kiểm tra lại metrics sau khi khôi phục.

---

## 8. Giải thích và tự đánh giá

* **Một quyết định kỹ thuật quan trọng và lý do:** sử dụng structured logging kết hợp `correlation_id` để có thể liên kết một request xuyên suốt Metrics → Logs → Traces. Cách này giúp quá trình điều tra incident có một định danh chung thay vì phải tìm kiếm thủ công giữa nhiều nguồn dữ liệu.

* **Một lỗi/blocker đã gặp:** trong quá trình triển khai Day 13, việc hoàn thiện evidence tracing/prompt versioning yêu cầu kiểm tra cả application logs và Langfuse thay vì chỉ kiểm tra dashboard runtime. Một trace được tạo thành công chưa đồng nghĩa với việc tất cả metadata prompt/version đã được chứng minh.

* **Cách tìm nguyên nhân và xử lý:** sử dụng kết quả validator và automated tests để xác nhận từng lớp observability. Với incident, quy trình được thiết kế theo Metrics → Logs → Traces: xác định bất thường từ metrics, tìm request bị ảnh hưởng bằng `correlation_id` trong logs, sau đó kiểm tra trace để xác định observation/span liên quan.

* **Cách hiểu luồng Metrics → Logs → Traces:** Metrics cho biết có bất thường hay không, ở đâu và từ lúc nào. Logs cho biết request nào bị ảnh hưởng, nhờ `correlation_id`. Traces cho biết span nào (`retrieval`, `generation`, agent...) liên quan đến vấn đề bằng cách đối chiếu thời gian và trạng thái các observation.

* **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** prompt version giúp xác định phiên bản prompt được sử dụng khi response được tạo ra. Token/cost cần theo dõi vì thay đổi prompt hoặc output length có thể làm thay đổi chi phí. SLO và error budget cung cấp ngưỡng định lượng để phát hiện degradation. Rollback giúp đưa hệ thống về version đã được xác nhận trước đó khi một thay đổi gây ra vấn đề.

* **Điều quan trọng nhất đã học:** observability không chỉ là ghi log mà cần liên kết được Metrics, Logs và Traces bằng một định danh chung như `correlation_id`. Việc kiểm tra bằng validator và automated tests cũng giúp phát hiện lỗi về schema, enrichment và PII trước khi vận hành.

* **Hạn chế:** Langfuse hiện ghi nhận 27 traces và 56 observations nhưng **0 scores tracked**. Một số thông tin prompt management như prompt name, version/label và trace ID tương ứng cần lấy từ màn hình Prompt/Trace detail thay vì suy luận từ dashboard tổng hợp. Incident root cause cũng cần được xác nhận bằng metric → log → trace evidence.

---

## 9. Checklist trước khi nộp

* [x] Kết quả validator đã được kiểm tra.
* [x] `validate_logs.py` đạt **100/100**.
* [x] `validate_dashboard.py` đạt **6/6 panel**.
* [x] `pytest` đạt **25 passed, 2 subtests passed**.
* [x] Có **106 log records** được phân tích.
* [x] Có **47 unique correlation IDs**.
* [x] Có **0 potential PII leaks**.
* [x] Có **27 Langfuse traces**.
* [x] Có **56 Langfuse observations**.
* [x] Langfuse model cost được ghi nhận **$0.03**.
* [x] Dashboard runtime có P95 latency **661 ms**.
* [x] Dashboard runtime có TTFT P95 **51 ms**.
* [x] Retrieval success rate **100.0%**.
* [x] Error rate **0.00%** trong runtime snapshot.
* [ ] Kiểm tra lại tên file evidence thực tế và đường dẫn tương đối.
* [ ] Xác nhận prompt name/version/label từ Langfuse Prompt Management.
* [ ] Xác nhận baseline/candidate trace ID nếu assignment yêu cầu.
* [ ] Hoàn thiện incident metric → log → trace → root cause bằng evidence thực tế.
* [ ] Kiểm tra tất cả ảnh/output mở được.
* [ ] Đảm bảo trace/prompt evidence thuộc project Langfuse cá nhân.
* [ ] Không có secret, API key hoặc PII thô trong repository/evidence.
* [x] Commit SHA cuối: `9b037711df700115b169a7ec6d8f1916aefd9fcb`.
* [ ] Push commit cuối lên repository trước khi nộp LMS.

---

## Tóm tắt kết quả cuối

**Logging & validation**

* `validate_logs.py`: **100/100**
* 106 log records
* 47 unique correlation IDs
* 0 PII leaks
* JSON schema: PASSED
* Correlation ID propagation: PASSED
* Log enrichment: PASSED
* PII scrubbing: PASSED

**Testing**

* **25 passed**
* **2 subtests passed**
* **3.98s**

**Dashboard**

* **6/6 panels valid**
* P95 latency: **661 ms**
* TTFT P95: **51 ms**
* Error rate: **0.00%**
* Retrieval success: **100.0%**
* Quality average: **0.88**
* Runtime cost: **$0.0229**

**Langfuse**

* **27 traces**
* **56 observations**
* Model: `claude-sonnet-4-5`
* Cost: **$0.03**
* Trace `day13-agent-request` P95: **3.31s**
* `lab-agent-run` P95: **2.34s**
* Scores tracked: **0**

**SLO**

* Target: **99.5%**
* Error budget: **0.5%**
* SLO latency threshold: **3000 ms**
* Evaluation window: **28 days**

**Final commit**

* `9b037711df700115b169a7ec6d8f1916aefd9fcb`
