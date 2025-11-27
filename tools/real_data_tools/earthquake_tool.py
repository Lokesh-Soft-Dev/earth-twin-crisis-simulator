# tools/real_data_tools/earthquake_tool.py
"""
EarthquakeTool (offline dummy)
Function: fetch_earthquakes(region: str) -> list[dict]
Each event: {id, magnitude, location, timestamp_iso}
"""

from datetime import datetime, timedelta
import uuid

def fetch_earthquakes(region: str = "global", limit: int = 5):
    """Return a list of dummy earthquake events for the region."""
    base_time = datetime.utcnow()
    events = []
    mags = [6.9, 5.4, 4.8, 7.1, 5.9]
    locs = [
        f"{region} coast",
        f"{region} inland",
        f"{region} valley",
        f"{region} mountains",
        f"{region} plains",
    ]
    for i in range(min(limit, len(mags))):
        events.append({
            "id": f"eq-{uuid.uuid4().hex[:8]}",
            "magnitude": mags[i],
            "location": locs[i],
            "timestamp": (base_time - timedelta(minutes=10*(i+1))).isoformat() + "Z"
        })
    return events
