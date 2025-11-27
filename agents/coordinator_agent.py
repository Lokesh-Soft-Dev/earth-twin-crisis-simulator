# agents/coordinator_agent.py
"""
Coordinator (upgraded):
- Orchestrates SignalAgent -> (optionally RealDataTools augmentation) -> RiskAgent -> PlannerAgent
- Calls HumanApprovalAgent (long-running op simulation)
- Persists to memory and logs events
- Evaluates plan via EvaluationAgent (which uses gemini_wrapper with offline fallback)
- All tool calls are logged with schema info from tools.tool_schemas.TOOL_SCHEMAS if available
"""

from core.message_bus import MessageBus
from core.logger import log_event
from memory.memory_store import append_memory
from typing import Dict, Any, List
from agents.signal_agent import SignalAgent
from agents.risk_agent import RiskAgent
from agents.planner_agent import PlannerAgent
from agents.human_approval_agent import HumanApprovalAgent
from agents.evaluation_agent import EvaluationAgent
import time, json

# tool schema registry
try:
    from tools.tool_schemas import TOOL_SCHEMAS
except Exception:
    TOOL_SCHEMAS = {}

# optional real-data tool imports (only used if use_real_tools=True)
try:
    from tools.real_data_tools import earthquake_tool, flood_tool, wildfire_tool, heatwave_tool, weather_tool
    _HAS_REAL_TOOLS = True
except Exception:
    _HAS_REAL_TOOLS = False

def _get_tool_schema(tool_name: str) -> Dict[str, Any]:
    return TOOL_SCHEMAS.get(tool_name, {"name": tool_name, "description": "unknown", "input_schema": {}, "output_schema": {}, "usage_hint": ""})

class Coordinator:
    def __init__(self, bus: MessageBus = None, auto_approve: bool = True, use_real_tools: bool = False):
        """
        use_real_tools: when True, Coordinator will augment signals with outputs from real_data_tools.* (offline-safe dummy tools).
        """
        self.bus = bus or MessageBus()
        self.signal_agent = SignalAgent()
        self.risk_agent = RiskAgent()
        self.planner = PlannerAgent()
        self.approver = HumanApprovalAgent(auto_approve=auto_approve)
        self.evaluator = EvaluationAgent(use_gemini=True)
        self.use_real_tools = use_real_tools and _HAS_REAL_TOOLS

    def _augment_with_real_tools(self, signals: List[Dict[str, Any]], region_hint: str = "global") -> List[Dict[str, Any]]:
        """
        Optionally call real-data tools to augment the signals list with additional events.
        This is additive — it does not replace your signals, just enriches.
        """
        augmented = list(signals)
        try:
            # Earthquake events -> transform to same signal shape
            eqs = earthquake_tool.fetch_earthquakes(region=region_hint, limit=3)
            for e in eqs:
                augmented.append({
                    "id": e.get("id"),
                    "type": "earthquake",
                    "location": e.get("location"),
                    "magnitude": float(e.get("magnitude", 0.0)),
                    "source_ts": e.get("timestamp")
                })
            # Flood risk -> convert to small 'flood' signal based on severity
            fr = flood_tool.fetch_flood_risk(region=region_hint)
            if fr and fr.get("severity", 0) >= 7:
                augmented.append({
                    "id": f"flood-{region_hint}-{int(time.time())}",
                    "type": "flood",
                    "location": region_hint,
                    "magnitude": float(fr.get("severity", 1.0)),
                    "source_ts": int(time.time())
                })
            # Wildfire hotspots -> create 'wildfire' signals scaled by intensity
            wf = wildfire_tool.fetch_wildfire_signatures(region=region_hint, limit=2)
            for idx, w in enumerate(wf):
                augmented.append({
                    "id": f"wf-{region_hint}-{idx}-{int(time.time())}",
                    "type": "wildfire",
                    "location": f"{region_hint} (lat:{w.get('latitude')})",
                    "magnitude": float(w.get("intensity", 1.0)),
                    "source_ts": int(time.time())
                })
            # Heatwave stats -> convert into 'heatwave' signal when heat_index above threshold
            hw = heatwave_tool.fetch_heatwave_stats(region=region_hint)
            if hw and float(hw.get("heat_index", 0.0)) >= 35.0:
                augmented.append({
                    "id": f"hw-{region_hint}-{int(time.time())}",
                    "type": "heatwave",
                    "location": region_hint,
                    "magnitude": float(hw.get("heat_index", 0.0)) / 10.0,
                    "source_ts": int(time.time())
                })
        except Exception:
            # If any real tool fails unexpectedly, ignore (we keep offline safety)
            pass
        return augmented

    def run(self, mode: str = "demo", region_hint: str = "global") -> Dict[str, Any]:
        ts = int(time.time())
        reasoning_log: List[Dict[str, Any]] = []

        # STEP 1: collect signals (tool call)
        tool_name = "signal_agent.get_signals"
        schema = _get_tool_schema(tool_name)
        reasoning_log.append({"step": 1, "action": "call_tool", "tool": tool_name, "tool_schema": schema})
        log_event({"event": "call_tool", "tool": tool_name})
        signals = self.signal_agent.get_signals()

        # Optional augmentation with real-data tools
        if self.use_real_tools:
            tool_name = "real_data_tools.earthquake.fetch_earthquakes"
            reasoning_log.append({"step": 1.1, "action": "augment_with_real_tools", "tool": tool_name, "tool_schema": _get_tool_schema(tool_name), "info": {"region": region_hint}})
            log_event({"event": "augment_with_real_tools", "tool": tool_name, "region": region_hint})
            signals = self._augment_with_real_tools(signals, region_hint=region_hint)

        # publish raw signals
        for s in signals:
            self.bus.publish(topic="signals.raw", sender="signal_agent", payload=s)

        # STEP 2: score signals (tool call)
        tool_name = "risk_agent.score_signals"
        schema = _get_tool_schema(tool_name)
        reasoning_log.append({"step": 2, "action": "call_tool", "tool": tool_name, "tool_schema": schema, "info": {"input_count": len(signals)}})
        log_event({"event": "call_tool", "tool": tool_name})
        scored = self.risk_agent.score_signals(signals)
        for s in scored:
            self.bus.publish(topic="signals.scored", sender="risk_agent", payload=s)

        # STEP 3: plan responses (tool call)
        tool_name = "planner_agent.plan_responses"
        schema = _get_tool_schema(tool_name)
        topk = self.risk_agent.top_k(scored, k=3)
        reasoning_log.append({"step": 3, "action": "call_tool", "tool": tool_name, "tool_schema": schema, "info": {"topk": [s["id"] for s in topk]}})
        log_event({"event": "call_tool", "tool": tool_name})
        plan = self.planner.plan_responses(topk)
        for e in plan:
            self.bus.publish(topic="plans.created", sender="planner_agent", payload=e)

        # STEP 4: human approval (long-running op simulation)
        tool_name = "human_approval_agent.request_approval"
        reasoning_log.append({"step": 4, "action": "call_tool", "tool": tool_name, "tool_schema": _get_tool_schema(tool_name), "info": {"plan_count": len(plan)}})
        log_event({"event": "call_tool", "tool": tool_name})
        approval_result = self.approver.request_approval(plan)
        reasoning_log.append({"step": 4.1, "action": "publish_approval", "result": approval_result})
        self.bus.publish(topic="plans.approval", sender="human_approval_agent", payload=approval_result)

        # STEP 5: persist episode to memory
        episode = {
            "ts": ts,
            "signals_count": len(signals),
            "top_signals": [{"id": s["id"], "severity": s["severity"]} for s in topk],
            "plan": plan,
            "approval": approval_result,
            "use_real_tools": self.use_real_tools
        }
        append_memory({"episode": episode})
        reasoning_log.append({"step": 5, "action": "persist_memory", "memory_entry": {"signals_count": len(signals)}})
        log_event({"event": "persist_memory", "signals_count": len(signals)})

        # STEP 6: evaluate plan
        tool_name = "evaluation_agent.evaluate_plan"
        reasoning_log.append({"step": 6, "action": "call_tool", "tool": tool_name, "tool_schema": _get_tool_schema(tool_name)})
        log_event({"event": "call_tool", "tool": tool_name})
        eval_result = self.evaluator.evaluate_plan(plan)
        self.bus.publish(topic="plans.evaluated", sender="evaluation_agent", payload=eval_result)
        reasoning_log.append({"step": 7, "action": "finished", "summary": {"plan_count": len(plan), "eval_score": eval_result.get("score")}})
        log_event({"event": "finished", "summary": {"plan_count": len(plan), "eval_score": eval_result.get("score")}})

        out = {
            "ts": ts,
            "reasoning_log": reasoning_log,
            "plan": plan,
            "scored_signals": scored,
            "approval": approval_result,
            "evaluation": eval_result
        }
        return out

if __name__ == "__main__":
    c = Coordinator()
    r = c.run()
    import json, sys
    print(json.dumps(r, indent=2))
