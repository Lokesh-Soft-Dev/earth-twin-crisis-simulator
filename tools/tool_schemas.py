# tools/tool_schemas.py
"""
Central registry of tool schemas used by agents.
Each entry describes:
- name: tool id
- description: short text
- input_schema: expected input keys + types (informal)
- output_schema: expected output keys + types (informal)
- usage_hint: when/why the coordinator uses this tool
"""

TOOL_SCHEMAS = {
    "signal_agent.get_signals": {
        "name": "signal_agent.get_signals",
        "description": "Return recent signals from demo fixtures or live connectors",
        "input_schema": {"none": "no args; reads demo_signals.json or APIs"},
        "output_schema": {"list": [{"id":"str","type":"str","location":"str","magnitude":"number","source_ts":"int"}]},
        "usage_hint": "Use to fetch raw environmental / event signals for analysis."
    },
    "risk_agent.score_signals": {
        "name": "risk_agent.score_signals",
        "description": "Scores signals with a severity numeric value",
        "input_schema": {"signals": "list of signal dicts"},
        "output_schema": {"signals": [{"id":"str","severity":"float","...":"..."}]},
        "usage_hint": "Use to rank and prioritize signals by predicted severity."
    },
    "planner_agent.plan_responses": {
        "name": "planner_agent.plan_responses",
        "description": "Generate scheduled response actions for top signals",
        "input_schema": {"signals_scored": "list of scored signals"},
        "output_schema": {"plan": [{"signal_id":"str","scheduled_time":"str","action":"str"}]},
        "usage_hint": "Use to create actionable response steps and timings."
    },
    "human_approval_agent.request_approval": {
        "name": "human_approval_agent.request_approval",
        "description": "Request human approval (long-running op pattern)",
        "input_schema": {"plan": "list of planned actions"},
        "output_schema": {"approved":"bool","review_notes":"str","review_ts":"int"},
        "usage_hint": "Use to pause and obtain human sign-off before executing critical actions."
    },
    "evaluation_agent.evaluate_plan": {
        "name": "evaluation_agent.evaluate_plan",
        "description": "Score and produce a verdict for a generated plan",
        "input_schema": {"plan": "list of planned actions"},
        "output_schema": {"score":"float","verdict":"str","notes":"str"},
        "usage_hint": "Use to compute quality metrics and short textual verdicts for the plan."
    }
}

"""
This file defines the schema/metadata for all tools used across the project.
These schemas are recorded inside reasoning_log for transparency.
"""

def make_schema(name, description, input_schema, output_schema):
    return {
        "name": name,
        "description": description,
        "input_schema": input_schema,
        "output_schema": output_schema
    }

# ------------------------------
# Real-World Dummy Connectors
# ------------------------------

EARTHQUAKE_TOOL_SCHEMA = make_schema(
    name="EarthquakeTool",
    description="Returns recent earthquake events (dummy offline-safe data).",
    input_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"}
        },
        "required": ["region"]
    },
    output_schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "magnitude": {"type": "number"},
                "location": {"type": "string"},
                "timestamp": {"type": "string"}
            }
        }
    }
)

FLOOD_TOOL_SCHEMA = make_schema(
    name="FloodRiskTool",
    description="Returns dummy flood severity based on region.",
    input_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"}
        },
        "required": ["region"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"},
            "risk_level": {"type": "string"},
            "severity": {"type": "number"}
        }
    }
)

WILDFIRE_TOOL_SCHEMA = make_schema(
    name="WildfireTool",
    description="Returns wildfire heat signatures (dummy NASA-style).",
    input_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"}
        },
        "required": ["region"]
    },
    output_schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "intensity": {"type": "number"}
            }
        }
    }
)

HEATWAVE_TOOL_SCHEMA = make_schema(
    name="HeatwaveRiskTool",
    description="Returns dangerous temperature conditions for a region (offline-safe).",
    input_schema={
        "type": "object",
        "properties": {"region": {"type": "string"}}
    },
    output_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"},
            "temperature_c": {"type": "number"},
            "humidity": {"type": "number"},
            "heat_index": {"type": "number"}
        }
    }
)

WEATHER_TOOL_SCHEMA = make_schema(
    name="WeatherTool",
    description="Returns offline-safe general weather info.",
    input_schema={
        "type": "object",
        "properties": {"region": {"type": "string"}}
    },
    output_schema={
        "type": "object",
        "properties": {
            "region": {"type": "string"},
            "condition": {"type": "string"},
            "temp_c": {"type": "number"},
            "wind_kph": {"type": "number"}
        }
    }
)

# -------------------------
# Real-data connector schemas
# -------------------------
TOOL_SCHEMAS.update({
    "real_data_tools.earthquake.fetch_earthquakes": {
        "name": "real_data_tools.earthquake.fetch_earthquakes",
        "description": "Return offline-safe dummy earthquake events for a region.",
        "input_schema": {"region": "str", "limit": "int"},
        "output_schema": [{"id":"str","magnitude":"float","location":"str","timestamp":"str"}],
        "usage_hint": "Use to augment signals with earthquake events."
    },
    "real_data_tools.flood.fetch_flood_risk": {
        "name": "real_data_tools.flood.fetch_flood_risk",
        "description": "Return dummy flood risk for a region.",
        "input_schema": {"region": "str"},
        "output_schema": {"region":"str","risk_level":"str","severity":"float"},
        "usage_hint": "Use to surface flood risk in context."
    },
    "real_data_tools.wildfire.fetch_wildfire_signatures": {
        "name": "real_data_tools.wildfire.fetch_wildfire_signatures",
        "description": "Return dummy wildfire heat signatures (lat,long,intensity).",
        "input_schema": {"region":"str","limit":"int"},
        "output_schema": [{"latitude":"float","longitude":"float","intensity":"float"}],
        "usage_hint": "Use to detect wildfire hotspots for planning."
    },
    "real_data_tools.heatwave.fetch_heatwave_stats": {
        "name": "real_data_tools.heatwave.fetch_heatwave_stats",
        "description": "Return dummy heatwave / temperature statistics.",
        "input_schema": {"region":"str"},
        "output_schema": {"region":"str","temperature_c":"float","humidity":"float","heat_index":"float"},
        "usage_hint": "Use to add heatwave signals."
    },
    "real_data_tools.weather.fetch_weather": {
        "name": "real_data_tools.weather.fetch_weather",
        "description": "Return offline weather info for a region.",
        "input_schema": {"region":"str"},
        "output_schema": {"region":"str","condition":"str","temp_c":"float","wind_kph":"float"},
        "usage_hint": "Use as auxiliary context for scoring and planning."
    }
})
