# agents/planner_agent.py
"""
PlannerAgent: given scored signals, create a simple response plan (tasks with time slots).
Returns a list of planned actions (events).
"""

from typing import List, Dict, Any
import datetime

DEFAULT_SLOTS = ["09:00", "12:00", "15:00", "18:00"]

class PlannerAgent:
    def __init__(self):
        pass

    def plan_responses(self, signals_scored: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create response tasks for each signal (top-first) and assign a time slot."""
        today = datetime.date.today().isoformat()
        plan = []
        for i, s in enumerate(signals_scored):
            slot = DEFAULT_SLOTS[i % len(DEFAULT_SLOTS)]
            event = {
                "signal_id": s.get("id"),
                "type": s.get("type"),
                "location": s.get("location"),
                "severity": s.get("severity"),
                "scheduled_time": f"{today}T{slot}",
                "action": self._default_action_for_type(s.get("type"))
            }
            plan.append(event)
        return plan

    def _default_action_for_type(self, type_: str) -> str:
        t = (type_ or "").lower()
        if "earth" in t or "quake" in t:
            return "Alert local emergency services; prepare shelter logistics"
        if "flood" in t:
            return "Issue flood advisory; mobilize water rescue teams"
        if "heat" in t or "heatwave" in t:
            return "Issue heat warning; open cooling centers"
        if "wild" in t or "fire" in t:
            return "Issue evacuation advisory; alert firefighting units"
        if "outbreak" in t:
            return "Notify public health; prepare testing and isolation"
        return "Monitor & notify stakeholders"
