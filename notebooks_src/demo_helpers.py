# notebooks_src/demo_helpers.py
import json
from typing import Any, Dict
from IPython.display import display, JSON

def pretty_print(out: Dict[str, Any]):
    print("=== REASONING LOG ===")
    for step in out.get("reasoning_log", []):
        print(f"- step {step.get('step')}: {step.get('action')}")
    print("\n=== PLAN ===")
    print(json.dumps(out.get("plan", []), indent=2))
    print("\n=== TOP SCORED SIGNALS (top 5) ===")
    for s in out.get("scored_signals", [])[:5]:
        print(f"- {s.get('id')}: {s.get('type')} at {s.get('location')} (severity={s.get('severity')})")

def show_logs(logs):
    print("=== RECENT LOGS ===")
    for l in logs[-10:]:
        print(f"{l.get('_ts')}: {l.get('event', l)}")
