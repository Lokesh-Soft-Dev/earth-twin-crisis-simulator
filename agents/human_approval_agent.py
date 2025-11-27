# agents/human_approval_agent.py
"""
HumanApprovalAgent:
Simulates a human-in-the-loop approval flow. Supports pause/resume semantics.
For this demo it responds automatically after a simulated delay, but structure
matches long-running operation pattern (request -> wait -> respond).
"""

import time
from typing import Dict, Any

class HumanApprovalAgent:
    def __init__(self, auto_approve: bool = True, response_delay_s: float = 0.5):
        self.auto_approve = auto_approve
        self.response_delay_s = response_delay_s

    def request_approval(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request approval for a plan. In a real deployment, this would pause and
        notify humans via UI/email and wait for an explicit response.
        Here we simulate with a short delay and auto-approval toggle.
        Returns approval result dict.
        """
        # simulate notification (would be a tool call in real system)
        time.sleep(self.response_delay_s)
        result = {
            "approved": bool(self.auto_approve),
            "review_notes": "Auto-approved in demo mode." if self.auto_approve else "Please review.",
            "review_ts": int(time.time())
        }
        return result
