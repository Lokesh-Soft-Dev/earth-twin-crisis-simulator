# tools/real_data_tools/heatwave_tool.py
"""
HeatwaveRiskTool (offline dummy)
Function: fetch_heatwave_stats(region: str) -> dict
Returns: {region, temperature_c, humidity, heat_index}
"""

def fetch_heatwave_stats(region: str = "global"):
    base = (sum(ord(c) for c in region) % 30) + 25  # base temp 25..54
    temp_c = float(base)
    humidity = float(30 + (sum(ord(c) for c in region) % 60))  # 30..89
    heat_index = round(temp_c + humidity * 0.1, 2)
    return {"region": region, "temperature_c": temp_c, "humidity": humidity, "heat_index": heat_index}
