"""Tạo và quản lý prompt `day13-chat` trên Langfuse.

Cách dùng (chạy ở thư mục gốc repo):
    python scripts/manage_prompts.py create     # tạo v1 (baseline, production) và v2 (candidate)
    python scripts/manage_prompts.py status     # xem nhãn của từng version
    python scripts/manage_prompts.py promote    # chuyển nhãn production sang v2
    python scripts/manage_prompts.py rollback   # chuyển nhãn production về v1

Cần LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST trong .env
(của project cá nhân day13-k4-l3b-<MSSV>).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROMPT_NAME = "day13-chat"

BASELINE_TEXT = (
    "You are a support assistant for a monitoring lab.\n"
    "Use the retrieved context to answer the question.\n"
    "Keep the answer short and never include personal data."
)

CANDIDATE_TEXT = (
    "You are a support assistant for a monitoring lab.\n"
    "Use only the retrieved context to answer the question.\n"
    "Answer in at most three sentences, be specific, and cite the policy when it applies.\n"
    "Never repeat personal data such as emails, phone numbers or card numbers; use sanitized summaries only."
)


def load_env() -> None:
    env_path = Path(".env")
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
        return
    except ImportError:
        pass
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_client():
    from langfuse import Langfuse

    for var in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"):
        if not os.getenv(var):
            sys.exit(f"Thiếu {var} trong .env")
    return Langfuse()


def prompt_exists(lf) -> bool:
    try:
        lf.get_prompt(PROMPT_NAME, label="latest", cache_ttl_seconds=0)
        return True
    except Exception:
        return False


def cmd_create(lf) -> None:
    if prompt_exists(lf):
        print(f"Prompt '{PROMPT_NAME}' đã tồn tại, không tạo lại để tránh trùng version.")
        print("Dùng `status` để xem, hoặc xóa prompt trên Langfuse nếu muốn làm lại.")
        return
    lf.create_prompt(name=PROMPT_NAME, prompt=BASELINE_TEXT, labels=["baseline", "production"], type="text")
    lf.create_prompt(name=PROMPT_NAME, prompt=CANDIDATE_TEXT, labels=["candidate"], type="text")
    lf.flush()
    print("Đã tạo v1 (baseline, production) và v2 (candidate).")
    cmd_status(lf)


def cmd_status(lf) -> None:
    for version in (1, 2):
        try:
            p = lf.get_prompt(PROMPT_NAME, version=version, cache_ttl_seconds=0)
            print(f"v{p.version}: labels={p.labels}")
        except Exception as exc:  # noqa: BLE001
            print(f"v{version}: không đọc được ({exc})")


def cmd_promote(lf) -> None:
    lf.update_prompt(name=PROMPT_NAME, version=2, new_labels=["candidate", "production"])
    print("Đã promote: production -> v2.")
    cmd_status(lf)


def cmd_rollback(lf) -> None:
    lf.update_prompt(name=PROMPT_NAME, version=1, new_labels=["baseline", "production"])
    print("Đã rollback: production -> v1.")
    cmd_status(lf)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["create", "status", "promote", "rollback"])
    args = parser.parse_args()
    load_env()
    lf = get_client()
    {"create": cmd_create, "status": cmd_status, "promote": cmd_promote, "rollback": cmd_rollback}[args.command](lf)


if __name__ == "__main__":
    main()