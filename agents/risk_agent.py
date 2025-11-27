# agents/risk_agent.py
"""
RiskAgent: scores signals for severity and returns a ranked list.
Simple heuristic scoring so runnable offline.
"""

from typing import List, Dict, Any

TYPE_BASE_SCORE = {
    "earthquake": 8.0,
    "flood": 6.0,
    "heatwave": 4.0,
    "wildfire": 7.0,
    "outbreak": 9.0,
}

def _score_signal(sig: Dict[str, Any]) -> float:
    t = sig.get("type", "").lower()
    base = TYPE_BASE_SCORE.get(t, 1.0)
    mag = float(sig.get("magnitude", 1.0) or 1.0)
    # heuristic: severity = base * log-scale of magnitude-like factor
    # keep simple: severity = base * min(1.0 + mag/10, 3.0)
    severity = base * min(1.0 + (mag / 10.0), 3.0)
    # small location risk multiplier (simulate population/density factor by string length)
    loc = sig.get("location", "")
    loc_factor = 1.0 + min(len(loc) / 50.0, 0.5)
    return round(severity * loc_factor, 3)

class RiskAgent:
    def __init__(self):
        pass

    def score_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return signals augmented with severity score, sorted descending."""
        out = []
        for s in signals:
            score = _score_signal(s)
            s2 = dict(s)
            s2["severity"] = score
            out.append(s2)
        out_sorted = sorted(out, key=lambda x: x["severity"], reverse=True)
        return out_sorted

    def top_k(self, signals_scored: List[Dict[str, Any]], k: int = 3):
        return signals_scored[:k]
