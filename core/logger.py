# core/logger.py
"""Structured logger writing traces to assets/logs.json"""

import json
from pathlib import Path
from datetime import datetime
from threading import Lock

LOG_PATH = Path(__file__).resolve().parents[1] / "assets" / "logs.json"
_lock = Lock()

def _ensure_file():
    if not LOG_PATH.exists():
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(json.dumps({"logs": []}, indent=2), encoding="utf8")

def log_event(event: dict):
    _ensure_file()
    with _lock:
        data = json.loads(LOG_PATH.read_text(encoding="utf8"))
        event["_ts"] = datetime.utcnow().isoformat() + "Z"
        data.get("logs", []).append(event)
        LOG_PATH.write_text(json.dumps(data, indent=2), encoding="utf8")

def tail_recent(n: int = 10):
    _ensure_file()
    data = json.loads(LOG_PATH.read_text(encoding="utf8"))
    return data.get("logs", [])[-n:]
