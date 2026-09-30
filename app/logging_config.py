from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import structlog
from structlog.contextvars import merge_contextvars

from .pii import scrub_text


LOG_PATH = Path(os.getenv("LOG_PATH", "data/logs.jsonl"))


class JsonlFileProcessor:
    def __call__(
        self,
        logger: Any,
        method_name: str,
        event_dict: dict[str, Any],
    ) -> dict[str, Any]:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        rendered = structlog.processors.JSONRenderer()(
            logger,
            method_name,
            event_dict,
        )

        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(rendered + "\n")

        return event_dict


def scrub_event(
    _: Any,
    __: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    payload = event_dict.get("payload")

    if isinstance(payload, dict):
        event_dict["payload"] = {
            k: scrub_text(v) if isinstance(v, str) else v
            for k, v in payload.items()
        }

    if "event" in event_dict and isinstance(event_dict["event"], str):
        event_dict["event"] = scrub_text(event_dict["event"])

    return event_dict


def configure_logging() -> None:
    logging.basicConfig(
        format="%(message)s",
        level=getattr(
            logging,
            os.getenv("LOG_LEVEL", "INFO").upper(),
        ),
    )

    structlog.configure(
        processors=[
            # Merge contextvars such as:
            # correlation_id, user_id_hash, session_id, feature, model, env
            merge_contextvars,

            # Add log level
            structlog.processors.add_log_level,

            # Add UTC timestamp
            structlog.processors.TimeStamper(
                fmt="iso",
                utc=True,
                key="ts",
            ),

            # Scrub PII before writing logs
            scrub_event,

            # Stack trace information
            structlog.processors.StackInfoRenderer(),

            # Format exception information
            structlog.processors.format_exc_info,

            # Write JSONL file
            JsonlFileProcessor(),

            # Render final output as JSON
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO
        ),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.typing.FilteringBoundLogger:
    return structlog.get_logger()