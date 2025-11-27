# scripts/run_demo.py
# Ensure repository root is on sys.path so local packages (core, agents, memory) import cleanly
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.message_bus import MessageBus
from agents.coordinator_agent import Coordinator
import json
import pathlib

def main():
    bus = MessageBus()
    # attach a simple subscriber to log published messages to console
    def printer(msg):
        try:
            print(f"[BUS] topic={msg.topic} sender={msg.sender} payload_keys={list(msg.payload.keys())}")
        except Exception:
            print("[BUS] subscriber error printing message")

    bus.subscribe("signals.raw", printer)
    bus.subscribe("signals.scored", printer)
    bus.subscribe("plans.created", printer)

    coord = Coordinator(bus=bus)
    out = coord.run()
    print("\n=== COORDINATOR OUTPUT ===")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    # run main when executed as a script
    main()
