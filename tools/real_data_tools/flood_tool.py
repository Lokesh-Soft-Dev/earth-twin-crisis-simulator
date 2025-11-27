# tools/real_data_tools/flood_tool.py
"""
FloodRiskTool (offline dummy)
Function: fetch_flood_risk(region: str) -> dict
Returns: {region, risk_level, severity (0-10)}
"""

def fetch_flood_risk(region: str = "global"):
    # simple deterministic mapping by region name hash
    score = (sum(ord(c) for c in region) % 10) + 1
    if score >= 8:
        lvl = "High"
    elif score >= 5:
        lvl = "Moderate"
    else:
        lvl = "Low"
    return {"region": region, "risk_level": lvl, "severity": float(score)}
