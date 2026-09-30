"""Dashboard 6 panel đọc từ data/logs.jsonl, theo contract config/dashboard.yaml.

Chạy:  streamlit run scripts/dashboard.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "dashboard.yaml"


def load_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["dashboard"]


def load_logs(path: Path, window_minutes: int, now: pd.Timestamp | None = None) -> pd.DataFrame:
    """Đọc JSONL, bỏ dòng hỏng, chỉ giữ cửa sổ `window_minutes` gần nhất."""
    rows = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    df = pd.DataFrame(rows)
    if df.empty or "ts" not in df:
        return pd.DataFrame(columns=["ts", "event"])
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["ts"])
    now = now or pd.Timestamp.now(tz="UTC")
    return df[df["ts"] >= now - pd.Timedelta(minutes=window_minutes)].copy()


def _pct(values: pd.Series, p: int) -> float:
    return float(values.quantile(p / 100)) if len(values.dropna()) else 0.0


def compute_panels(df: pd.DataFrame) -> dict:
    """Tính giá trị các panel theo đúng query trong dashboard.yaml."""
    for col in ("latency_ms", "ttft_ms", "cost_usd", "tokens_in", "tokens_out",
                "quality_score", "error_type", "tool_success"):
        if col not in df:
            df[col] = pd.NA
    sent = df[df["event"] == "response_sent"]
    received = df[df["event"] == "request_received"]
    failed = df[df["event"] == "request_failed"]

    n_recv, n_fail = len(received), len(failed)
    tool = df["tool_success"].dropna()

    per_min = received.set_index("ts").resample("1min").size() if n_recv else pd.Series(dtype=int)
    cost_min = (
        sent.set_index("ts")["cost_usd"].astype(float).resample("1min").sum()
        if len(sent) else pd.Series(dtype=float)
    )
    lat = sent["latency_ms"].astype(float)
    return {
        "latency": {
            "p50": _pct(lat, 50), "p95": _pct(lat, 95), "p99": _pct(lat, 99),
            "ttft_p95": _pct(sent["ttft_ms"].astype(float), 95),
            "series": sent.set_index("ts")["latency_ms"].astype(float) if len(sent) else pd.Series(dtype=float),
        },
        "traffic": {
            "count": n_recv,
            "rate_per_minute": float(per_min.mean()) if len(per_min) else 0.0,
            "series": per_min,
        },
        "errors": {
            "error_rate_pct": (n_fail / n_recv * 100) if n_recv else 0.0,
            "by_type": failed["error_type"].value_counts().to_dict(),
            "tool_success_rate_pct": (float((tool.astype(bool)).mean()) * 100) if len(tool) else 100.0,
        },
        "cost": {"total": float(sent["cost_usd"].astype(float).sum()), "series": cost_min},
        "tokens": {
            "tokens_in": int(sent["tokens_in"].astype(float).sum()),
            "tokens_out": int(sent["tokens_out"].astype(float).sum()),
        },
        "quality": {"mean": float(sent["quality_score"].astype(float).mean()) if len(sent) else 0.0},
    }


def check(value: float, threshold: dict) -> bool:
    return value <= threshold["value"] if threshold["operator"] == "lte" else value >= threshold["value"]


def main() -> None:  # pragma: no cover - giao diện
    import plotly.graph_objects as go
    import streamlit as st

    cfg = load_config()
    panels = {p["id"]: p for p in cfg["panels"]}
    st.set_page_config(page_title=cfg["title"], layout="wide")
    st.title(cfg["title"])

    @st.fragment(run_every=cfg["refresh_seconds"])
    def render() -> None:
        window = cfg["time_range_minutes"]
        df = load_logs(REPO_ROOT / "data" / "logs.jsonl", window)
        m = compute_panels(df)
        st.caption(
            f"Time range: {window} phút gần nhất | refresh {cfg['refresh_seconds']}s | "
            f"nguồn: data/logs.jsonl | {len(df)} dòng log"
        )

        def line(series, title, unit, thr=None, kind="scatter"):
            fig = go.Figure()
            if len(series):
                fig.add_trace(go.Scatter(x=series.index, y=series.values, mode="lines+markers", name=title))
            if thr is not None:
                fig.add_hline(y=thr["value"], line_dash="dash", line_color="red",
                              annotation_text=f"Threshold {thr['operator']} {thr['value']} {unit}")
            fig.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), yaxis_title=unit)
            st.plotly_chart(fig, use_container_width=True)

        row1 = st.columns(3)
        row2 = st.columns(3)

        with row1[0]:
            p = panels["latency"]; lat = m["latency"]
            st.subheader(f"{p['title']} ({p['unit']})")
            c = st.columns(4)
            c[0].metric("P50", f"{lat['p50']:.0f} ms")
            c[1].metric("P95", f"{lat['p95']:.0f} ms", "OK" if check(lat["p95"], p["threshold"]) else "VƯỢT")
            c[2].metric("P99", f"{lat['p99']:.0f} ms")
            c[3].metric("TTFT P95", f"{lat['ttft_p95']:.0f} ms")
            line(lat["series"], "latency_ms", "ms", p["threshold"])

        with row1[1]:
            p = panels["traffic"]; t = m["traffic"]
            st.subheader(f"{p['title']} ({p['unit']})")
            st.metric("Tổng request", t["count"])
            st.metric("Trung bình / phút", f"{t['rate_per_minute']:.1f}",
                      "OK" if check(t["rate_per_minute"], p["threshold"]) else "THẤP")
            line(t["series"], "request/phút", "req/min", p["threshold"])

        with row1[2]:
            p = panels["errors"]; e = m["errors"]
            st.subheader(f"{p['title']} ({p['unit']})")
            c = st.columns(2)
            c[0].metric("Error rate", f"{e['error_rate_pct']:.2f} %",
                        "OK" if check(e["error_rate_pct"], p["threshold"]) else "VƯỢT (>2%)")
            c[1].metric("Retrieval success", f"{e['tool_success_rate_pct']:.1f} %",
                        "OK" if e["tool_success_rate_pct"] >= 90 else "THẤP (<90%)")
            st.write("Breakdown theo error_type:", e["by_type"] or "không có lỗi")

        with row2[0]:
            p = panels["cost"]; c_ = m["cost"]
            st.subheader(f"{p['title']} ({p['unit']})")
            st.metric("Tổng cost", f"${c_['total']:.4f}",
                      "OK" if check(c_["total"], p["threshold"]) else "VƯỢT")
            line(c_["series"], "cost/phút", "USD", p["threshold"])

        with row2[1]:
            p = panels["tokens"]; tk = m["tokens"]
            st.subheader(f"{p['title']} ({p['unit']})")
            fig = go.Figure(go.Bar(x=["tokens_in", "tokens_out"], y=[tk["tokens_in"], tk["tokens_out"]]))
            fig.add_hline(y=p["threshold"]["value"], line_dash="dash", line_color="red",
                          annotation_text=f"Threshold {p['threshold']['value']} tokens")
            fig.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), yaxis_title="tokens")
            st.plotly_chart(fig, use_container_width=True)

        with row2[2]:
            p = panels["quality"]; q = m["quality"]
            st.subheader(f"{p['title']} ({p['unit']})")
            st.metric("Quality trung bình", f"{q['mean']:.2f}",
                      "OK" if check(q["mean"], p["threshold"]) else "THẤP (<0.75)")
            st.progress(min(max(q["mean"], 0.0), 1.0))
            st.caption(f"Threshold: {p['threshold']['operator']} {p['threshold']['value']}")

    render()


if __name__ == "__main__":
    main()
