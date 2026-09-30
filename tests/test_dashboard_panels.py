from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import dashboard  # noqa: E402


def _row(ts, event, **kw):
    return {"ts": ts, "event": event, **kw}


def test_compute_panels_basic():
    df = pd.DataFrame([
        _row("2026-01-01T00:00:00Z", "request_received"),
        _row("2026-01-01T00:00:01Z", "response_sent", latency_ms=200, ttft_ms=50,
             tokens_in=10, tokens_out=20, cost_usd=0.01, quality_score=0.9, tool_success=True),
        _row("2026-01-01T00:00:02Z", "request_received"),
        _row("2026-01-01T00:00:03Z", "request_failed", error_type="RuntimeError", tool_success=False),
    ])
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    m = dashboard.compute_panels(df)
    assert m["errors"]["error_rate_pct"] == 50.0
    assert m["errors"]["by_type"] == {"RuntimeError": 1}
    assert m["errors"]["tool_success_rate_pct"] == 50.0
    assert m["tokens"] == {"tokens_in": 10, "tokens_out": 20}
    assert m["latency"]["p95"] == 200.0


def test_empty_logs_do_not_crash():
    m = dashboard.compute_panels(pd.DataFrame(columns=["ts", "event"]))
    assert m["traffic"]["count"] == 0 and m["quality"]["mean"] == 0.0


def test_threshold_operators():
    assert dashboard.check(2000, {"operator": "lte", "value": 3000})
    assert not dashboard.check(0.5, {"operator": "gte", "value": 0.75})
