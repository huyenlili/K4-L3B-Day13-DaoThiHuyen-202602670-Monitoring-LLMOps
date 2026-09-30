# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** **[ĐIỀN: họ tên]**
- **MSSV:** 202602670 **[KIỂM TRA: suy ra từ owner trong alert_rules.yaml]**
- **Lớp:** K4-L3B
- **Repository URL:** **[ĐIỀN: link repo]**
- **Commit SHA cuối:** **[ĐIỀN: chạy `git rev-parse HEAD` sau commit cuối]**
- **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`
- **Tên project Langfuse cá nhân:** `day13-k4-l3b-202602670`

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
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | **[ĐIỀN]** | **[ĐIỀN]** | **[ĐIỀN]** |
| `validate_dashboard.py` | **[ĐIỀN]** | **[ĐIỀN]** | **[ĐIỀN]** |
| `pytest` | **[ĐIỀN]** | **[ĐIỀN]** | **[ĐIỀN]** |
| Số traces hợp lệ | **[ĐIỀN]** | **[ĐIỀN]** | **[ĐIỀN]** |
| Số PII leak | **[ĐIỀN]** | **[ĐIỀN]** | **[ĐIỀN]** |
| Latency P95 / TTFT P95 | **[ĐIỀN: ms / ms]** | **[ĐIỀN: ms / ms]** | **[ĐIỀN]** |
| Retrieval success rate | **[ĐIỀN: %]** | **[ĐIỀN: %]** | **[ĐIỀN]** |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** **[ĐIỀN: theo code của bạn. Gợi ý: middleware nhận header `x-request-id` hoặc sinh mới, gắn vào contextvars/log, trả lại trong response header, và đưa vào metadata/tags của trace Langfuse]**
- **Các metadata được ghi vào structured log:** **[ĐIỀN: liệt kê các trường thực tế trong `data/logs.jsonl`, ví dụ `ts`, `event`, `correlation_id`, `latency_ms`, `ttft_ms`, `tokens_in/out`, `cost_usd`, `error_type`]**
- **Cách bảo đảm PII được scrub trước khi ghi:** **[ĐIỀN: mô tả bước scrub trong code, ví dụ processor/filter chạy trước khi ghi file, các pattern email/số điện thoại/thẻ đã che]**
- **Cách kiểm chứng kết quả:** chạy `python scripts/validate_logs.py`, kiểm tra số PII leak bằng 0 và xem `evidence/04-structured-log.png`, `evidence/05-pii-redaction.png`. **[KIỂM TRA lại cho khớp thực tế]**

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** trace nằm trong project `day13-k4-l3b-202602670`, dùng key của project này trong `.env`, và trace ID/`correlation_id` khớp với log do máy tôi sinh ra. **[KIỂM TRA]**
- **Cấu trúc root/retrieval/generation observations:** root `lab-agent-run` (agent) chứa hai observation con: `retrieval` (`@observe` trên `retrieve()` trong `app/mock_rag.py`, type span) và `generation` (`@observe` trên `FakeLLM.generate()` trong `app/mock_llm.py`, type generation, có `model` và `usage_details` input/output). Prompt managed được truyền cho generation qua `propagate_attributes(prompt=...)`.
- **Cách nối trace với log:** **[ĐIỀN: ví dụ `correlation_id` trong log = metadata/tag/session của trace, dùng để tìm trace tương ứng]**
- **Prompt name:** **[ĐIỀN]**
- **Version/label baseline:** **[ĐIỀN]**
- **Version/label candidate:** **[ĐIỀN]**
- **Trace ID của mỗi version:** baseline **[ĐIỀN]**; candidate **[ĐIỀN]**
- **Cách promote và rollback `production`:** **[ĐIỀN: gắn label `production` cho version candidate để promote; rollback bằng cách gắn lại label cho version baseline. Ghi đúng thao tác bạn đã làm]**

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Streamlit (`scripts/dashboard.py`, chạy bằng `streamlit run scripts/dashboard.py`) đọc trực tiếp `data/logs.jsonl`, time range 60 phút, tự refresh 30 giây, đúng sáu panel trong `config/dashboard.yaml`: Latency (P50/P95/P99 + TTFT P95, ms, threshold P95 ≤ 3000), Traffic (request/phút, ≥ 1), Errors (error rate %, breakdown theo `error_type`, retrieval success %, ≤ 2%), Cost (USD, tổng ≤ 2.5), Tokens (in/out, ≤ 50000), Quality (mean, ≥ 0.75). Mỗi panel có đơn vị và đường/nhãn threshold. Phần tính toán tách riêng và có test (`tests/test_dashboard_panels.py`).
- **SLO và lý do chọn:** giữ SLO `fast_successful_requests`: 99.5% request `response_sent` có `latency_ms <= 3000` trong 28 ngày. Ngưỡng 3000 ms cách xa baseline (P95 baseline của tôi: **[ĐIỀN: P95 baseline từ dashboard]** ms), nên chỉ bị vi phạm khi có bất thường thật như `rag_slow` (retrieval thêm 2.5 giây).
- **Cách tính error budget:** SLO 99.5% nghĩa là error budget 0.5%. Ví dụ 10,000 request trong 28 ngày thì tối đa 50 request được phép lỗi hoặc chậm hơn 3000 ms. Khi P95 vượt ngưỡng kéo dài, budget bị tiêu nhanh nên alert `HighLatencyP95` cảnh báo sớm.
- **Ba alert và runbook tương ứng:** `config/alert_rules.yaml` và `docs/alerts.md`, gửi Slack `#k4-l3b-alerts`, owner `student-202602670`: (1) `HighLatencyP95` warning, P95 > 3000 ms trong 5 phút; (2) `HighErrorRate` critical, error rate > 2% trong 5 phút; (3) `DailyCostOverBudget` warning, cost 24 giờ > 2.5 USD trong 15 phút. Mỗi alert có ảnh hưởng tới người dùng, ba bước kiểm tra Metrics → Logs → Traces và mitigation.

> Ví dụ cách viết error budget: "SLO 99.5% trong 28 ngày nghĩa là error budget 0.5%. Nếu workload có 10,000 request thì tối đa 50 request được phép lỗi hoặc chậm hơn ngưỡng SLO."

## 7. Điều tra challenge

- **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1`
- **Khoảng thời gian điều tra:** **[ĐIỀN: từ hh:mm đến hh:mm, ngày]**
- **Triệu chứng từ metrics:** **[ĐIỀN: panel nào bất thường, giá trị lúc lỗi so với baseline, lúc mấy giờ; dùng `latency_ms` từ log/dashboard]** (`evidence/12-incident-metric.png`)
- **Log line và correlation ID liên quan:** **[ĐIỀN: dán một dòng log bất thường, ghi `correlation_id=...`]** (`evidence/13-incident-log.png`)
- **Trace ID và span gây ảnh hưởng:** **[ĐIỀN: trace ID, tên span, thời gian/trạng thái so với bình thường]** (`evidence/14-incident-trace.png`)
- **Root cause:** **[ĐIỀN: suy ra từ ba bằng chứng trên, không đoán]**
- **Fix action:** **[ĐIỀN: hành động khôi phục, ví dụ tắt incident bằng `python scripts/inject_incident.py --scenario <tên> --disable` và xác nhận `/health`]**
- **Preventive measure:** **[ĐIỀN: alert/runbook/test/guardrail. Có thể dẫn `HighLatencyP95`, `HighErrorRate` hoặc `DailyCostOverBudget` trong `config/alert_rules.yaml` nếu khớp]**

> Gợi ý cách viết ngắn, không thay cho evidence thực tế: "Metric cho thấy `[latency/error/cost/quality]` bất thường trong `[khoảng thời gian]`. Log line `[event]` có `correlation_id=[...]` đại diện cho request bị ảnh hưởng. Trace cùng `correlation_id` cho thấy span `[retrieval/generation/prompt/tool]` có dấu hiệu `[chậm/lỗi/token tăng]`. Root cause là `[nguyên nhân suy ra từ evidence]`. Fix action là `[hành động khôi phục]`; preventive measure là `[alert/runbook/test/guardrail để ngăn tái diễn]`."

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** **[ĐIỀN: quyết định của bạn và vì sao]**
- **Một lỗi/blocker đã gặp:** **[ĐIỀN: lỗi thực tế bạn gặp]**
- **Cách tìm nguyên nhân và xử lý:** **[ĐIỀN]**
- **Cách hiểu luồng Metrics → Logs → Traces:** Metrics cho biết có bất thường không, ở đâu và từ lúc nào. Logs cho biết request nào bị ảnh hưởng, nhờ `correlation_id`. Traces cho biết span nào (retrieval, generation...) gây ra, nhờ so thời gian và trạng thái các span. Đi đúng thứ tự này thì không phải đoán root cause hay mở trace ngẫu nhiên.
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** Prompt version giúp biết thay đổi nào gây ra khác biệt về chất lượng, token và cost, và rollback về version cũ nhanh khi candidate kém hơn. Token/cost cần theo dõi vì một prompt hay lỗi có thể làm output tăng nhiều lần. SLO và error budget cho ngưỡng rõ ràng để quyết định khi nào cảnh báo và khi nào phải dừng thay đổi.
- **Điều quan trọng nhất đã học:** **[ĐIỀN: viết theo trải nghiệm của bạn]**
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** **[ĐIỀN hoặc ghi "Không có"]**

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.