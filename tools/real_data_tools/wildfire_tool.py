# tools/real_data_tools/wildfire_tool.py
"""
WildfireTool (offline dummy)
Function: fetch_wildfire_signatures(region: str, limit: int) -> list[dict]
Each item: {latitude, longitude, intensity}
"""

def fetch_wildfire_signatures(region: str = "global", limit: int = 5):
    # pseudo-random but deterministic pattern based on region string
    base = sum(ord(c) for c in region) % 90
    out = []
    for i in range(limit):
        out.append({
            "latitude": round(-10 + ((base + i) % 80) * 0.5, 4),
            "longitude": round(20 + ((base + i) % 120) * 0.6, 4),
            "intensity": round(1.0 + ((i + base) % 10) * 0.9, 2)
        })
    return out
