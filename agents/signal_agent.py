# agents/signal_agent.py
"""
SignalAgent: collects signals from demo fixtures (assets/demo_signals.json).
If the file is missing or empty, returns built-in sample signals.
Each signal is a dict: { "id", "type", "location", "magnitude", "source_ts" }
"""

import json
from pathlib import Path
import time
import uuid
from typing import List, Dict, Any

ASSETS = Path(__file__).resolve().parents[1] / "assets"
DEMO_SIGNALS = ASSETS / "demo_signals.json"

SAMPLE_SIGNALS = [
    {"id": "sig-1", "type": "earthquake", "location": "Chile", "magnitude": 6.8, "source_ts": int(time.time()) - 3600},
    {"id": "sig-2", "type": "flood", "location": "Bangladesh", "magnitude": 3, "source_ts": int(time.time()) - 1800},
    {"id": "sig-3", "type": "heatwave", "location": "Spain", "magnitude": 2, "source_ts": int(time.time()) - 7200},
]

class SignalAgent:
    def __init__(self):
        self._assets = ASSETS

    def get_signals(self) -> List[Dict[str, Any]]:
        """Return a list of recent signals. Prefer demo file, else fallback to sample."""
        try:
            if DEMO_SIGNALS.exists():
                text = DEMO_SIGNALS.read_text(encoding="utf8").strip()
                if text:
                    data = json.loads(text)
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict) and "signals" in data:
                        return data["signals"]
            # fallback
            return SAMPLE_SIGNALS
        except Exception:
            return SAMPLE_SIGNALS

    def generate_signal(self, type_: str, location: str, magnitude: float) -> Dict[str, Any]:
        s = {
            "id": f"sig-{uuid.uuid4().hex[:8]}",
            "type": type_,
            "location": location,
            "magnitude": magnitude,
            "source_ts": int(time.time())
        }
        return s
