# tools/gemini_wrapper.py
"""
Gemini wrapper (offline-safe).

Usage:
- Call judge_plan(plan: list[dict]) -> dict with keys: score, verdict, explanation
- If GEMINI_API_KEY found in env, you can swap the _call_gemini() stub to use your client.
- Otherwise an offline deterministic judge runs (based on average severity).
"""

import os
import json
from typing import List, Dict, Any

# ENV key name you can add to Kaggle Secrets or environment when ready
GEMINI_ENV_KEY = "GEMINI_API_KEY"

def _call_gemini(prompt: str) -> str:
    """
    Stub for real Gemini/API call.
    Replace the contents of this function with actual client call when you have a key.
    Return a textual judgement string (could be JSON).
    """
    # Example placeholder — DO NOT send keys here.
    raise RuntimeError("No Gemini client implemented. Add your client call here if you have an API key.")

def _offline_judge(plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministic offline judge:
    - computes average severity and returns structured verdict + explanation
    """
    if not plan:
        return {"score": 0.0, "verdict": "No plan", "explanation": "Plan is empty."}
    total = 0.0
    count = 0
    for p in plan:
        try:
            total += float(p.get("severity", 0.0))
            count += 1
        except Exception:
            continue
    avg = (total / count) if count else 0.0
    # map avg severity to 0-100 scale (assume max severity ~20)
    score = round(min((avg / 20.0) * 100.0, 100.0), 2)
    if score >= 75:
        verdict = "Excellent plan"
    elif score >= 50:
        verdict = "Good plan"
    elif score >= 25:
        verdict = "Needs improvement"
    else:
        verdict = "Low quality plan"

    explanation = (
        f"Offline judge: avg severity={avg:.3f} => score={score}. "
        "This heuristic estimates readiness; replace with Gemini for richer feedback."
    )
    return {"score": score, "verdict": verdict, "explanation": explanation}

def judge_plan(plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main entrypoint. Returns a dict:
      {"score": float, "verdict": str, "explanation": str}
    Behavior:
      - If GEMINI_API_KEY in env, try to call `_call_gemini` (you must implement actual client)
      - Otherwise use deterministic offline judge.
    """
    key = os.environ.get(GEMINI_ENV_KEY) or os.environ.get("OPENAI_API_KEY")
    if key:
        # If you add a real client, implement _call_gemini and parse result to dict
        try:
            prompt = f"Judge this plan and return JSON with score/verdict/explanation:\n\n{json.dumps(plan, indent=2)}"
            txt = _call_gemini(prompt)
            # Attempt to parse JSON from model response; fallback to textual verdict
            try:
                parsed = json.loads(txt)
                return parsed
            except Exception:
                return {"score": None, "verdict": txt[:200], "explanation": "Raw model text returned."}
        except Exception as e:
            # If Gemini call fails for any reason, fallback to offline judge
            return {"score": None, "verdict": "Gemini call failed", "explanation": str(e)}
    else:
        return _offline_judge(plan)

# quick CLI test when run directly
if __name__ == "__main__":
    import sys
    example = [{"severity": 12.0}, {"severity": 8.0}, {"severity": 15.0}]
    print("Example judge:", judge_plan(example))
