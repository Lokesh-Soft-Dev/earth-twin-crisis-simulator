# memory/memory_store.py
"""Simple JSON-backed memory store for long-term memory persistence."""

import json
from pathlib import Path
import time
from typing import Any, Dict

MEM_PATH = Path(__file__).resolve().parent / "memory.json"

def _ensure_file():
    if not MEM_PATH.exists():
        MEM_PATH.write_text(json.dumps({"sessions": []}, indent=2), encoding="utf8")

def read_memory() -> Dict[str, Any]:
    _ensure_file()
    data = json.loads(MEM_PATH.read_text(encoding="utf8"))
    return data

def append_memory(entry: Dict[str, Any]) -> None:
    _ensure_file()
    data = read_memory()
    entry["_ts"] = int(time.time())
    data.get("sessions", []).append(entry)
    MEM_PATH.write_text(json.dumps(data, indent=2), encoding="utf8")

def clear_memory() -> None:
    MEM_PATH.write_text(json.dumps({"sessions": []}, indent=2), encoding="utf8")
