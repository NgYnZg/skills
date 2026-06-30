"""Append dated entries to docs/app/log.md."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .paths import log_path


def append(message: str, cwd: Path = Path(".")) -> None:
    log = log_path(cwd)
    log.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"- {datetime.now(timezone.utc).isoformat()} {message}\n"

    if log.exists():
        text = log.read_text(encoding="utf-8")
    else:
        text = "# Log\n\n"

    header = f"## {today}\n\n"
    if header not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += header

    if not text.endswith("\n"):
        text += "\n"
    text += entry
    log.write_text(text, encoding="utf-8")
