# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert mẫu để tham khảo

Ví dụ dưới đây minh họa mức độ cụ thể cần có. Học viên không cần copy nguyên, nhưng ba alert trong bài nộp nên rõ ràng tương tự: điều kiện là gì, kéo dài bao lâu, ảnh hưởng tới user ra sao và người trực cần kiểm tra gì trước.

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: latency P95 của `response_sent.latency_ms`
- Điều kiện và thời gian duy trì: `p95(latency_ms) > 3000ms` trong 5 phút
- Ảnh hưởng tới người dùng: người dùng phải chờ lâu hơn trước khi nhận câu trả lời
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard latency để xác nhận P95/P99 và khoảng thời gian tăng.
  2. Lọc `data/logs.jsonl` trong khoảng đó, lấy một `correlation_id` có `latency_ms` cao.
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh các span chính để xác định bước nào bất thường.
- Mitigation tạm thời: dựa trên evidence thực tế để rollback prompt, khôi phục cấu hình liên quan, tắt practice scenario hoặc giảm tải khi demo.
- Owner: `student-<MSSV>`

## Alert 1

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: `fast_successful_requests` (`latency_ms <= 3000`, mục tiêu 99.5%)
- Điều kiện và thời gian duy trì: `p95(response_sent.latency_ms) > 3000ms` liên tục 5 phút
- Ảnh hưởng tới người dùng: người dùng chờ lâu hơn 3 giây mới nhận được câu trả lời, error budget bị tiêu nhanh
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Latency trên dashboard, xác nhận P95/P99 và mốc giờ bắt đầu tăng.
  2. Lọc `data/logs.jsonl` trong khoảng đó, lấy một `correlation_id` có `latency_ms` cao.
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh thời gian span `retrieval` và `generation` để biết bước nào chậm.
- Mitigation tạm thời: tắt practice scenario nếu đang bật (`python scripts/inject_incident.py --scenario <tên> --disable`), khôi phục cấu hình retrieval, giảm tải khi demo.
- Owner: `student-202602670`

## Alert 2

- Tên: `HighErrorRate`
- Severity: `critical`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: guardrail `error_rate_pct_max: 2` và `retrieval_success_rate_pct_min: 90`
- Điều kiện và thời gian duy trì: `count(request_failed) / count(request_received) * 100 > 2` liên tục 5 phút
- Ảnh hưởng tới người dùng: request trả HTTP 500, người dùng không nhận được câu trả lời
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Errors, xem `error_type` nào chiếm phần lớn và retrieval success còn bao nhiêu phần trăm.
  2. Lọc log `event == "request_failed"`, lấy `correlation_id` và đọc `payload.detail`.
  3. Mở trace cùng `correlation_id`, kiểm tra span nào có trạng thái ERROR (retrieval hay generation).
- Mitigation tạm thời: khôi phục dependency lỗi (vector store), tắt practice scenario `tool_fail`, chuyển sang câu trả lời fallback nếu có.
- Owner: `student-202602670`

## Alert 3

- Tên: `DailyCostOverBudget`
- Severity: `warning`
- Duration: `15m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: guardrail `daily_cost_usd_max: 2.5`
- Điều kiện và thời gian duy trì: `sum(response_sent.cost_usd)` trong 24 giờ `> 2.5 USD`, duy trì 15 phút
- Ảnh hưởng tới người dùng: chưa ảnh hưởng trực tiếp, nhưng chi phí vượt ngân sách có thể buộc phải giới hạn dịch vụ
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Cost và Tokens, xác nhận thời điểm cost/phút tăng và `tokens_out` có tăng theo không.
  2. Lọc log `response_sent` trong khoảng đó, lấy `correlation_id` có `tokens_out` và `cost_usd` cao.
  3. Mở trace cùng `correlation_id`, xem `usage_details` của span `generation` và version prompt đang dùng.
- Mitigation tạm thời: rollback label `production` về prompt version trước, giới hạn độ dài output, tắt practice scenario `cost_spike`.
- Owner: `student-202602670`
