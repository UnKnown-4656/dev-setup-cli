"""Dual logging for users (text) and machines (JSONL)."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import os
import uuid

_RUN_ID = uuid.uuid4().hex[:12]


def _log_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        p = Path(appdata) / "DevSetup"
        p.mkdir(parents=True, exist_ok=True)
        return p
    return Path(".")


def _text_log_file() -> Path:
    return _log_dir() / "devsetup-log.txt"


def _jsonl_log_file() -> Path:
    return _log_dir() / "devsetup-log.jsonl"


def get_run_id() -> str:
    return _RUN_ID


def log_event(message: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{_RUN_ID}] {message}\n"
    try:
        _text_log_file().open("a", encoding="utf-8").write(line)
    except Exception:
        pass

    event = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "run_id": _RUN_ID,
        "message": message,
    }
    try:
        _jsonl_log_file().open("a", encoding="utf-8").write(json.dumps(event) + "\n")
    except Exception:
        pass


def log_structured(action: str, **fields) -> None:
    payload = {"action": action, **fields}
    text = " ".join(f"{k}={v}" for k, v in payload.items())
    log_event(text)
