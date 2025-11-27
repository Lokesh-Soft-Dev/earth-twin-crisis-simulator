# agents/evaluation_agent.py
"""
EvaluationAgent:
- Primary job: evaluate a produced plan and return structured metrics.
- Uses tools.gemini_wrapper.judge_plan() when available (offline-safe wrapper).
- Keeps deterministic fallback behavior for Kaggle.
"""

from typing import List, Dict, Any
from tools.gemini_wrapper import judge_plan

def simple_plan_score(plan: List[Dict[str, Any]]) -> float:
    """
    Very small heuristic: score = average severity normalized to [0,100].
    If plan empty -> score 0.
    """
    if not plan:
        return 0.0
    total = 0.0
    count = 0
    for p in plan:
        try:
            total += float(p.get("severity", 0.0))
            count += 1
        except Exception:
            continue
    avg = (total / count) if count else 0.0
    # normalize by assumed max severity 20 -> scale to 100
    score = min((avg / 20.0) * 100.0, 100.0)
    return round(score, 2)

class EvaluationAgent:
    def __init__(self, use_gemini: bool = True):
        """
        use_gemini: when True, will attempt to call tools.gemini_wrapper.judge_plan()
                    which itself is offline-safe if no API key present.
        """
        self.use_gemini = use_gemini

    def evaluate_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Returns a dict:
          { score: float | None, verdict: str, notes: str, raw: Any }
        If Gemini/real judge available, attempt to use it; otherwise fallback to heuristic.
        """
        # First, try the gemini wrapper if configured
        if self.use_gemini:
            try:
                res = judge_plan(plan)
                # Ensure keys exist and normalize if possible
                score = res.get("score") if isinstance(res, dict) else None
                verdict = res.get("verdict") if isinstance(res, dict) else str(res)
                explanation = res.get("explanation") if isinstance(res, dict) else "Model returned textual verdict."
                # If score is None, compute heuristic to attach a numeric baseline
                if score is None:
                    score = simple_plan_score(plan)
                    explanation = f"Gemini returned no numeric score; heuristic fallback score={score}. " + str(explanation)
                return {
                    "score": score,
                    "verdict": verdict,
                    "notes": "Primary evaluation via gemini_wrapper (offline-safe).",
                    "explanation": explanation,
                    "raw": res
                }
            except Exception as e:
                # If gemini_wrapper fails, fall through to heuristic
                fallback_score = simple_plan_score(plan)
                return {
                    "score": fallback_score,
                    "verdict": "Fallback heuristic",
                    "notes": f"Gemini wrapper failed: {e}. Used heuristic.",
                    "explanation": "Heuristic: average severity -> scaled score",
                    "raw": None
                }

        # If not using Gemini or it failed, use heuristic
        score = simple_plan_score(plan)
        verdict = "High-quality plan" if score > 60 else ("Medium-quality plan" if score > 30 else "Low-quality plan")
        return {
            "score": score,
            "verdict": verdict,
            "notes": "Heuristic evaluation (offline).",
            "explanation": f"Average severity based heuristic -> score={score}",
            "raw": None
        }
