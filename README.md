# Earth Twin — Global Crisis Simulation

**One-line pitch:** A multi-agent "digital twin" that collects global signals (earthquakes, floods, wildfires, heatwaves), scores severity, generates response plans, requests human approval, persists memory, and evaluates plan quality — with transparent tool schemas recorded in the reasoning log.

---

## Quick status
- Demo pipeline runs locally and on Kaggle (offline-safe).
- Features implemented: multi-agent orchestration, tool schemas, long-running ops (human approval), memory persistence, observability (logs), offline real-data connectors (dummy), and LLM-as-judge stub (offline-safe).
- Tests: `pytest` passes.

---

## How to run (local)
1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1   # PowerShell (Windows)
   source .venv/bin/activate    # macOS / Linux

Install requirements:
pip install -r requirements.txt

Run tests:
pytest -q

Run demo (offline):
python -u .\scripts\run_demo.py

(Optional) Run demo with real-tools augmentation:
python -c "from agents.coordinator_agent import Coordinator; import json; print(json.dumps(Coordinator(use_real_tools=True).run(region_hint='Chile'), indent=2))"
