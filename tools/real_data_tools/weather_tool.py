# tools/real_data_tools/weather_tool.py
"""
WeatherTool (offline fallback)
Function: fetch_weather(region: str) -> dict
Returns: {region, condition, temp_c, wind_kph}
"""

def fetch_weather(region: str = "global"):
    conditions = ["Clear", "Cloudy", "Rain", "Thunder", "Windy"]
    idx = sum(ord(c) for c in region) % len(conditions)
    condition = conditions[idx]
    temp_c = 20 + (sum(ord(c) for c in region) % 15)
    wind = 5 + (sum(ord(c) for c in region) % 30)
    return {"region": region, "condition": condition, "temp_c": float(temp_c), "wind_kph": float(wind)}
